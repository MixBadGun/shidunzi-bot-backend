"""add and remove a lot of index

迁移 ID: 20fe0d856b29
父迁移: f3040b70c492
创建时间: 2024-06-14 18:12:44.246988

"""
from __future__ import annotations

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = '20fe0d856b29'
down_revision: str | Sequence[str] | None = 'f3040b70c492'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade(name: str = "") -> None:
    if name:
        return
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('catch_award', schema=None) as batch_op:
        batch_op.drop_index('ix_catch_award_updated_at')

    with op.batch_alter_table('catch_award_alt_name', schema=None) as batch_op:
        batch_op.drop_index('ix_catch_award_alt_name_updated_at')

    with op.batch_alter_table('catch_award_counter', schema=None) as batch_op:
        batch_op.drop_index('ix_catch_award_counter_updated_at')

    with op.batch_alter_table('catch_award_stats', schema=None) as batch_op:
        batch_op.drop_index('ix_catch_award_stats_updated_at')

    with op.batch_alter_table('catch_award_tag_relation', schema=None) as batch_op:
        batch_op.drop_index('ix_catch_award_tag_relation_updated_at')

    with op.batch_alter_table('catch_global', schema=None) as batch_op:
        batch_op.drop_index('ix_catch_global_updated_at')

    with op.batch_alter_table('catch_level', schema=None) as batch_op:
        batch_op.drop_index('ix_catch_level_updated_at')

    with op.batch_alter_table('catch_level_alt_name', schema=None) as batch_op:
        batch_op.drop_index('ix_catch_level_alt_name_updated_at')

    with op.batch_alter_table('catch_level_tag_relation', schema=None) as batch_op:
        batch_op.drop_index('ix_catch_level_tag_relation_updated_at')

    with op.batch_alter_table('catch_skin', schema=None) as batch_op:
        batch_op.drop_index('ix_catch_skin_updated_at')

    with op.batch_alter_table('catch_skin_alt_name', schema=None) as batch_op:
        batch_op.drop_index('ix_catch_skin_alt_name_updated_at')

    with op.batch_alter_table('catch_skin_own_record', schema=None) as batch_op:
        batch_op.drop_index('ix_catch_skin_own_record_updated_at')

    with op.batch_alter_table('catch_skin_record', schema=None) as batch_op:
        batch_op.drop_index('ix_catch_skin_record_updated_at')

    with op.batch_alter_table('catch_skin_tag_relation', schema=None) as batch_op:
        batch_op.drop_index('ix_catch_skin_tag_relation_updated_at')

    with op.batch_alter_table('catch_tag', schema=None) as batch_op:
        batch_op.drop_index('ix_catch_tag_updated_at')

    with op.batch_alter_table('catch_user_data', schema=None) as batch_op:
        batch_op.drop_index('ix_catch_user_data_updated_at')
        batch_op.create_index(batch_op.f('ix_catch_user_data_qq_id'), ['qq_id'], unique=True)

    # ### end Alembic commands ###


def downgrade(name: str = "") -> None:
    if name:
        return
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('catch_user_data', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_catch_user_data_qq_id'))
        batch_op.create_index('ix_catch_user_data_updated_at', ['updated_at'], unique=False)

    with op.batch_alter_table('catch_tag', schema=None) as batch_op:
        batch_op.create_index('ix_catch_tag_updated_at', ['updated_at'], unique=False)

    with op.batch_alter_table('catch_skin_tag_relation', schema=None) as batch_op:
        batch_op.create_index('ix_catch_skin_tag_relation_updated_at', ['updated_at'], unique=False)

    with op.batch_alter_table('catch_skin_record', schema=None) as batch_op:
        batch_op.create_index('ix_catch_skin_record_updated_at', ['updated_at'], unique=False)

    with op.batch_alter_table('catch_skin_own_record', schema=None) as batch_op:
        batch_op.create_index('ix_catch_skin_own_record_updated_at', ['updated_at'], unique=False)

    with op.batch_alter_table('catch_skin_alt_name', schema=None) as batch_op:
        batch_op.create_index('ix_catch_skin_alt_name_updated_at', ['updated_at'], unique=False)

    with op.batch_alter_table('catch_skin', schema=None) as batch_op:
        batch_op.create_index('ix_catch_skin_updated_at', ['updated_at'], unique=False)

    with op.batch_alter_table('catch_level_tag_relation', schema=None) as batch_op:
        batch_op.create_index('ix_catch_level_tag_relation_updated_at', ['updated_at'], unique=False)

    with op.batch_alter_table('catch_level_alt_name', schema=None) as batch_op:
        batch_op.create_index('ix_catch_level_alt_name_updated_at', ['updated_at'], unique=False)

    with op.batch_alter_table('catch_level', schema=None) as batch_op:
        batch_op.create_index('ix_catch_level_updated_at', ['updated_at'], unique=False)

    with op.batch_alter_table('catch_global', schema=None) as batch_op:
        batch_op.create_index('ix_catch_global_updated_at', ['updated_at'], unique=False)

    with op.batch_alter_table('catch_award_tag_relation', schema=None) as batch_op:
        batch_op.create_index('ix_catch_award_tag_relation_updated_at', ['updated_at'], unique=False)

    with op.batch_alter_table('catch_award_stats', schema=None) as batch_op:
        batch_op.create_index('ix_catch_award_stats_updated_at', ['updated_at'], unique=False)

    with op.batch_alter_table('catch_award_counter', schema=None) as batch_op:
        batch_op.create_index('ix_catch_award_counter_updated_at', ['updated_at'], unique=False)

    with op.batch_alter_table('catch_award_alt_name', schema=None) as batch_op:
        batch_op.create_index('ix_catch_award_alt_name_updated_at', ['updated_at'], unique=False)

    with op.batch_alter_table('catch_award', schema=None) as batch_op:
        batch_op.create_index('ix_catch_award_updated_at', ['updated_at'], unique=False)

    # ### end Alembic commands ###
