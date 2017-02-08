"""Create bills

Revision ID: 352d41dc748c
Revises: 6fbf47b106f0
Create Date: 2016-12-25 11:48:16.604274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '352d41dc748c'
down_revision = '6fbf47b106f0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
            'bills',
            sa.Column('id', sa.String(128), nullable=False, primary_key=True, unique=True),
            sa.Column('accountId', sa.String(128),nullable=False),
            sa.Column('title', sa.Unicode(1024), nullable=False),
            sa.Column('amount', sa.Float(), nullable=False),
            sa.Column('currency_code', sa.String(16), nullable=False),
            sa.Column('date', sa.Date, nullable=False),
            sa.Column('day', sa.Integer, nullable=False),
            sa.Column('month', sa.Integer, nullable=False),
            sa.Column('year', sa.Integer, nullable=False),

            sa.Column('notes', sa.UnicodeText()),
            sa.Column('createdAt', sa.DateTime),
            sa.Column('tagsHashString', sa.Unicode(256))
            )


def downgrade():
    op.drop_table('bills')
