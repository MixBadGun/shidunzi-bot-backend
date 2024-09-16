"""CDKEY UPDATE 3

Revision ID: 0bcb0e074213
Revises: 2e196e0d18ff
Create Date: 2024-09-16 13:03:09.046256

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0bcb0e074213"
down_revision: Union[str, None] = "2e196e0d18ff"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("catch_cdk_batch_award", schema=None) as batch_op:
        batch_op.alter_column("chips", existing_type=sa.INTEGER(), nullable=True)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("catch_cdk_batch_award", schema=None) as batch_op:
        batch_op.alter_column("chips", existing_type=sa.INTEGER(), nullable=False)

    # ### end Alembic commands ###
