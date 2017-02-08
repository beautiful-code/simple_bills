"""Create AccountProfileRoles

Revision ID: da55e84dff3f
Revises: 69fbde5b6271
Create Date: 2016-12-27 20:48:37.463198

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da55e84dff3f'
down_revision = '69fbde5b6271'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
         'account_profile_roles',
         sa.Column('id', sa.Integer, nullable=False, primary_key=True, unique=True, autoincrement=True),
         sa.Column('accountId', sa.String(128), nullable=False),
         sa.Column('profileId', sa.String(128), nullable=False),
         sa.Column('role', sa.String(64))
         )

def downgrade():
    op.drop_table('profiles')
