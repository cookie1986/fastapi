"""add foreign key to post table

Revision ID: 167fb3a5b254
Revises: fbb2cf8df554
Create Date: 2022-09-16 11:52:35.091274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '167fb3a5b254'
down_revision = 'fbb2cf8df554'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer, nullable=False))
    op.create_foreign_key(
        'posts_users_fk', source_table='posts', 
        referent_table='users', 
        local_cols=['owner_id'], 
        remote_cols=['id'], 
        ondelete='CASCADE'
        )
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
