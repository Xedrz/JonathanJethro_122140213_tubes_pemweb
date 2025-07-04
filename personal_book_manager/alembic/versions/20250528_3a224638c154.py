"""Menghapus openlibrary_id

Revision ID: 3a224638c154
Revises: 14456d4ec6bc
Create Date: 2025-05-28 07:41:01.418399

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a224638c154'
down_revision = '14456d4ec6bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('revoked_tokens')
    op.alter_column('books', 'isbn',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('books', 'isbn',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.create_table('revoked_tokens',
    sa.Column('jti', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('jti', name='revoked_tokens_pkey')
    )
    # ### end Alembic commands ###
