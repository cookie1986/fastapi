"""create post table

Revision ID: 5de767136a4e
Revises: 
Create Date: 2022-09-16 11:19:31.719113

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5de767136a4e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('title', sa.String(), nullable=False))
    
    pass


def downgrade() -> None:
    op.drop_table('posts')

    pass
