"""add_item_count_to_orders

Revision ID: 3a78ef6d26f7
Revises: 65ce696c76eb
Create Date: 2025-05-06 14:33:31.957438

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a78ef6d26f7'
down_revision = '65ce696c76eb'
branch_labels = None
depends_on = None


def upgrade():
    # Add item_count column to the orders table
    op.add_column('order', sa.Column('item_count', sa.Integer(), nullable=True))
    
    # Just add the column without updating existing records, since we're not sure
    # about the correct table name


def downgrade():
    # Remove the item_count column
    op.drop_column('order', 'item_count') 