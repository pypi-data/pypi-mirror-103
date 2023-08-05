"""Initial schema

Revision ID: a3f7ae51a72b
Revises: 
Create Date: 2021-02-24 14:49:27.508365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a3f7ae51a72b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "ensemble",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "time_created",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column(
            "time_updated",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("num_realizations", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "parameter",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "time_created",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column(
            "time_updated",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("values", sa.ARRAY(sa.FLOAT()), nullable=False),
        sa.Column("ensemble_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["ensemble_id"],
            ["ensemble.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "record",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "time_created",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column(
            "time_updated",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("ensemble_id", sa.Integer(), nullable=False),
        sa.Column("record_type", sa.Integer(), nullable=False),
        sa.Column("data", sa.PickleType(), nullable=False),
        sa.Column("is_response", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["ensemble_id"],
            ["ensemble.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("record")
    op.drop_table("parameter")
    op.drop_table("ensemble")
    # ### end Alembic commands ###
