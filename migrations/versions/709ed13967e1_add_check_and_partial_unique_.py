"""add check and partial unique constraints manually

Revision ID: 709ed13967e1
Revises: 382b8631c091
Create Date: 2025-08-20 19:11:02.416429

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '709ed13967e1'
down_revision = '382b8631c091'
branch_labels = None
depends_on = None


def upgrade():
   # TravelItem のチェック制約
    op.create_check_constraint(
        "check_travelitems_not_all_null",
        "travel_items",
        "(item_id IS NOT NULL OR custom_item_id IS NOT NULL OR my_set_item_id IS NOT NULL)"
    )

    # MySetItem の部分ユニーク制約（PostgreSQL専用）
    op.create_index(
        "uq_mysetitems_item",
        "my_set_items",
        ["my_set_id", "item_id"],
        unique=True,
        postgresql_where=sa.text("item_id IS NOT NULL")
    )
    op.create_index(
        "uq_mysetitems_custom_item",
        "my_set_items",
        ["my_set_id", "custom_item_id"],
        unique=True,
        postgresql_where=sa.text("custom_item_id IS NOT NULL")
    ) 


def downgrade():
    pass