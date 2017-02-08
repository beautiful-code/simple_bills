"""Create accounts

Revision ID: 6fbf47b106f0
Revises: 992d524fc33f
Create Date: 2016-12-25 00:26:20.350398

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6fbf47b106f0'
down_revision = '992d524fc33f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
         'accounts',
         sa.Column('id', sa.String(128), nullable=False, primary_key=True, unique=True),
         sa.Column('profileId', sa.String(128),nullable=False),
         sa.Column('name', sa.String(128), nullable=False),
         sa.Column('tagstr', sa.String(256)),
         sa.Column('defaultCurrencyCode', sa.String(16)),
         sa.Column('createdAt', sa.DateTime)
         )


def downgrade():
    op.drop_table('accounts')
