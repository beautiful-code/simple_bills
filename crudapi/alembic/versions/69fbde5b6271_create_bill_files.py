"""Create bill_files

Revision ID: 69fbde5b6271
Revises: 352d41dc748c
Create Date: 2016-12-26 22:22:18.038352

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69fbde5b6271'
down_revision = '352d41dc748c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
            'bill_files',
            sa.Column('id', sa.String(128), nullable=False, primary_key=True, unique=True),
            sa.Column('billId', sa.String(128),nullable=False),
            sa.Column('name', sa.Unicode(256), nullable=False),
            sa.Column('path', sa.String(256), nullable=False),
            sa.Column('file_type', sa.String(128)),
            sa.Column('createdAt', sa.DateTime),
            )


def downgrade():
    pass
