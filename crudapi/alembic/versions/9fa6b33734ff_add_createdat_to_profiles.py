"""Add createdAt to profiles

Revision ID: 9fa6b33734ff
Revises: f53992654ae9
Create Date: 2016-12-31 22:26:25.657458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9fa6b33734ff'
down_revision = 'f53992654ae9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('profiles', sa.Column('createdAt',sa.DateTime))


def downgrade():
    op.drop_column('profiles', 'createdAt')
