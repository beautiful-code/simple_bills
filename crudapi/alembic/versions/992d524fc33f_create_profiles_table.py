"""create profiles table

Revision ID: 992d524fc33f
Revises: 
Create Date: 2016-12-24 23:33:34.604087

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '992d524fc33f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
         'profiles',
         sa.Column('id', sa.String(128), nullable=False, primary_key=True, unique=True),
         sa.Column('email', sa.String(128), nullable=False, primary_key=True),
         sa.Column('userId', sa.String(64)),
         sa.Column('nickname', sa.String(256))
         )

def downgrade():
    op.drop_table('profiles')
