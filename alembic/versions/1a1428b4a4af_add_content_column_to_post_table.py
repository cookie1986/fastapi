"""add content column to post table

Revision ID: 1a1428b4a4af
Revises: 5de767136a4e
Create Date: 2022-09-16 11:25:11.474284

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a1428b4a4af'
down_revision = '5de767136a4e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')

    pass
