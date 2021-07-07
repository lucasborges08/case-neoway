"""create error_logs table

Revision ID: 75ea488c4b5c
Revises: d9ca3d6935df
Create Date: 2021-07-06 18:33:01.120800

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75ea488c4b5c'
down_revision = 'd9ca3d6935df'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'error_logs',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('file_id', sa.BigInteger, nullable=False),
        sa.Column('touple_content', sa.String(200), nullable=False),
        sa.Column('message', sa.String(100), nullable=False),
        sa.Column('occured_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['file_id'], ['files.id'])
    )


def downgrade():
    op.drop_table('error_logs')
