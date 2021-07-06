"""create clients table

Revision ID: d9ca3d6935df
Revises: 04f68b7d7bda
Create Date: 2021-07-05 22:57:30.293480

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey


# revision identifiers, used by Alembic.
revision = 'd9ca3d6935df'
down_revision = '04f68b7d7bda'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'clients',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('doc_number', sa.String(14), nullable=False),
        sa.Column('private', sa.Boolean, nullable=False),
        sa.Column('incomplete', sa.Boolean, nullable=False),
        sa.Column('last_purchase_at', sa.DateTime, nullable=True),
        sa.Column('average_ticket', sa.Float, nullable=True),
        sa.Column('last_purchase_ticket', sa.Float, nullable=True),
        sa.Column('most_frequent_store', sa.String(19), nullable=True),
        sa.Column('last_purchase_store', sa.String(19), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('file_id', sa.BigInteger, nullable=False),
        sa.ForeignKeyConstraint(['file_id'], ['files.id'])
    )


def downgrade():
    op.drop_table('clients')
