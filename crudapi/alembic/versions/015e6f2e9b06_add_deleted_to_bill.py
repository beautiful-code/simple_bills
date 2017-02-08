"""add deleted to bill

Revision ID: 015e6f2e9b06
Revises: 9fa6b33734ff
Create Date: 2017-01-12 07:12:52.458818

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '015e6f2e9b06'
down_revision = '9fa6b33734ff'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('bills', sa.Column('deleted',sa.Boolean, nullable=False, default=True))


def downgrade():
    op.drop_column('bills', 'deleted')
