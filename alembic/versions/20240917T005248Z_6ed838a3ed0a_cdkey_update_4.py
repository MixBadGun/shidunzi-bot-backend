"""CDKEY UPDATE 4

Revision ID: 6ed838a3ed0a
Revises: 0bcb0e074213
Create Date: 2024-09-17 00:52:48.214775

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6ed838a3ed0a"
down_revision: Union[str, None] = "0bcb0e074213"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "catch_cdk_attempt",
        sa.Column("uid", sa.Integer(), nullable=True),
        sa.Column("cdkey", sa.String(), nullable=False),
        sa.Column("data_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["uid"], ["catch_user_data.data_id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("data_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("catch_cdk_attempt")
    # ### end Alembic commands ###
