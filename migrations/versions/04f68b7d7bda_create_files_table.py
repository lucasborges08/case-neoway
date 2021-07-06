"""create files table

Revision ID: 04f68b7d7bda
Revises: 
Create Date: 2021-07-04 22:00:00.772616

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04f68b7d7bda'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'files',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('content', sa.Binary, nullable=False),
        sa.Column('type', sa.String(30), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('processed_at', sa.DateTime(timezone=True), nullable=True)
    )


def downgrade():
    op.drop_table('files')
