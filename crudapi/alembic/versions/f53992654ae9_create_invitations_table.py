"""create invitations table

Revision ID: f53992654ae9
Revises: da55e84dff3f
Create Date: 2016-12-31 21:42:29.514543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f53992654ae9'
down_revision = 'da55e84dff3f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
         'invitations',
         sa.Column('id', sa.String(128), nullable=False, primary_key=True, unique=True),
         sa.Column('accountId', sa.String(128), nullable=False),
         sa.Column('senderId', sa.String(128), nullable = False),
         sa.Column('receiverEmail', sa.String(128), nullable=False),
         sa.Column('state', sa.String(128), nullable=False),
         sa.Column('expiresAt', sa.DateTime, nullable=False),
         sa.Column('createdAt', sa.DateTime)
         )


def downgrade():
    op.drop_table('invitations')
