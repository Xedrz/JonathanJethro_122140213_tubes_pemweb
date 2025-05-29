"""set isbn not null and unique

Revision ID: 14456d4ec6bc
Revises: e5b286578397
Create Date: 2025-05-27 20:13:43.317822

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14456d4ec6bc'
down_revision = 'e5b286578397'
branch_labels = None
depends_on = None



def upgrade():
    op.alter_column('books', 'isbn', nullable=False)
    op.create_unique_constraint('uq_books_isbn', 'books', ['isbn'])


def downgrade():
    op.drop_constraint('uq_books_isbn', 'books', type_='unique')
    op.alter_column('books', 'isbn', nullable=True)

