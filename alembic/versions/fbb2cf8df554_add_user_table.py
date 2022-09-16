"""add user table

Revision ID: fbb2cf8df554
Revises: 1a1428b4a4af
Create Date: 2022-09-16 11:27:52.334820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbb2cf8df554'
down_revision = '1a1428b4a4af'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                    server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'), # an alternative way to set the primary key
        sa.UniqueConstraint('email')
    )

    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
