import os
import requests
from typing import (
    Any,
    AsyncGenerator,
    Generator,
    Mapping,
    MutableMapping,
    Optional,
    TYPE_CHECKING,
    Tuple,
    Union,
)
from pprint import pformat
from contextlib import contextmanager
from sqlalchemy.orm.session import Session
from sqlalchemy.engine.base import Transaction
from starlette.testclient import (
    TestClient as StarletteTestClient,
    ASGI2App,
    ASGI3App,
    Cookies,
    Params,
    DataType,
    TimeOut,
    FileType,
)
from sqlalchemy.orm import sessionmaker
from graphene import Schema as GrapheneSchema
from graphene.test import Client as GrapheneClient


if TYPE_CHECKING:
    from promise import Promise
    from rx import Observable
    from graphql.execution import ExecutionResult

    GraphQLResult = Union[ExecutionResult, Observable, Promise[ExecutionResult]]


class ClientError(RuntimeError):
    pass


class _TestClient:
    __test__ = False  # Pytest should ignore this class

    def __init__(
        self,
        app: Union[ASGI2App, ASGI3App],
        session: sessionmaker,
        gql_schema: GrapheneSchema,
        base_url: str = "http://testserver",
        raise_server_exceptions: bool = True,
        root_path: str = "",
    ) -> None:
        self.http_client = StarletteTestClient(
            app, base_url, raise_server_exceptions, root_path
        )
        self.gql_client = GrapheneClient(gql_schema)
        self.session = session

    def get(
        self,
        url: str,
        params: Params = None,
        headers: MutableMapping[str, str] = None,
        cookies: Cookies = None,
        files: FileType = None,
        timeout: TimeOut = None,
        allow_redirects: bool = None,
        stream: bool = None,
        check_status_code: Optional[int] = 200,
    ) -> requests.Response:
        resp = self.http_client.get(
            url,
            params=params,
            headers=headers,
            cookies=cookies,
            files=files,
            timeout=timeout,
            allow_redirects=allow_redirects,
            stream=stream,
        )
        _check(check_status_code, resp)
        return resp

    def post(
        self,
        url: str,
        params: Params = None,
        data: DataType = None,
        headers: MutableMapping[str, str] = None,
        cookies: Cookies = None,
        files: FileType = None,
        timeout: TimeOut = None,
        allow_redirects: bool = None,
        stream: bool = None,
        json: Any = None,
        check_status_code: Optional[int] = 200,
    ) -> requests.Response:
        resp = self.http_client.post(
            url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            timeout=timeout,
            allow_redirects=allow_redirects,
            stream=stream,
            json=json,
        )
        _check(check_status_code, resp)
        return resp

    def put(
        self,
        url: str,
        params: Params = None,
        data: DataType = None,
        headers: MutableMapping[str, str] = None,
        cookies: Cookies = None,
        files: FileType = None,
        timeout: TimeOut = None,
        allow_redirects: bool = None,
        stream: bool = None,
        json: Any = None,
        check_status_code: Optional[int] = 200,
    ) -> requests.Response:
        resp = self.http_client.put(
            url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            timeout=timeout,
            allow_redirects=allow_redirects,
            stream=stream,
            json=json,
        )
        _check(check_status_code, resp)
        return resp

    def patch(
        self,
        url: str,
        params: Params = None,
        data: DataType = None,
        headers: MutableMapping[str, str] = None,
        cookies: Cookies = None,
        files: FileType = None,
        timeout: TimeOut = None,
        allow_redirects: bool = None,
        stream: bool = None,
        json: Any = None,
        check_status_code: Optional[int] = 200,
    ) -> requests.Response:
        resp = self.http_client.patch(
            url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            timeout=timeout,
            allow_redirects=allow_redirects,
            stream=stream,
            json=json,
        )
        _check(check_status_code, resp)
        return resp

    def delete(
        self,
        url: str,
        params: Params = None,
        headers: MutableMapping[str, str] = None,
        cookies: Cookies = None,
        timeout: TimeOut = None,
        allow_redirects: bool = None,
        check_status_code: Optional[int] = 200,
    ) -> requests.Response:
        resp = self.http_client.delete(
            url,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            allow_redirects=allow_redirects,
        )
        _check(check_status_code, resp)
        return resp

    def gql_execute(
        self,
        request_string: str,
        variable_values: Optional[Mapping[str, Any]] = None,
        check: bool = True,
    ) -> dict:
        doc = self.gql_client.execute(request_string, variable_values=variable_values)
        if check and "errors" in doc:
            raise ClientError(f"GraphQL query returned an error:\n{pformat(doc)}")

        return doc


@contextmanager
def testclient_factory() -> Generator[_TestClient, None, None]:
    if "ERT_STORAGE_DATABASE_URL" not in os.environ:
        os.environ["ERT_STORAGE_DATABASE_URL"] = "sqlite:///:memory:"
        print("Using in-memory SQLite database for tests")

    from ert_storage.app import app
    from ert_storage.graphql import schema

    session, transaction, connection = _begin_transaction()
    schema.override_session = session

    yield _TestClient(app, session=session, gql_schema=schema)

    schema.override_session = None
    _end_transaction(transaction, connection)


_TransactionInfo = Tuple[sessionmaker, Transaction, Any]


def _override_get_db(session: sessionmaker) -> None:
    from ert_storage.app import app
    from ert_storage.database import (
        get_db,
        IS_POSTGRES,
    )

    async def override_get_db() -> AsyncGenerator[Session, None]:
        db = session()

        # Make PostgreSQL return float8 columns with highest precision. If we don't
        # do this, we may lose up to 3 of the least significant digits.
        if IS_POSTGRES:
            db.execute("SET extra_float_digits=3")
        try:
            yield db
            db.commit()
            db.close()
        except:
            db.rollback()
            db.close()
            raise

    app.dependency_overrides[get_db] = override_get_db


def _begin_transaction() -> _TransactionInfo:
    from ert_storage.database import (
        engine,
        IS_SQLITE,
        HAS_AZURE_BLOB_STORAGE,
    )
    from ert_storage.database_schema import Base

    if IS_SQLITE:
        Base.metadata.create_all(bind=engine)
    if HAS_AZURE_BLOB_STORAGE:
        import asyncio
        from ert_storage.database import create_container_if_not_exist

        loop = asyncio.get_event_loop()
        loop.run_until_complete(create_container_if_not_exist())

    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(autocommit=False, autoflush=False, bind=connection)

    _override_get_db(session)

    return session, transaction, connection


def _end_transaction(transaction: Transaction, connection: Any) -> None:
    # teardown: rollback database to before the test.
    # For debugging change rollback to commit.
    transaction.rollback()
    connection.close()


def _check(check_status_code: Optional[int], response: requests.Response) -> None:
    if check_status_code is not None and response.status_code != check_status_code:
        try:
            doc = response.json()
        except:
            doc = response.content
        raise ClientError(
            f"Status code was {response.status_code}, expected {check_status_code}:\n{doc}"
        )
