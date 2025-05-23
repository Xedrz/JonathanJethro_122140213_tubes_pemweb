from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

revision = '821a9d83db40'
down_revision = None
branch_labels = None
depends_on = None

book_status_enum = pg.ENUM('Want to Read', 'Reading', 'Finished', name='bookstatus')

def upgrade():
    # Tidak perlu create enum manual
    op.create_table(
        'books',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('openlibrary_id', sa.String(length=255), nullable=False, unique=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('author', sa.String(length=255), nullable=True),
        sa.Column('published_date', sa.Date(), nullable=True),
        sa.Column('cover_url', sa.String(length=512), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('pages', sa.Integer(), nullable=True),
        sa.Column('status', book_status_enum, nullable=True, server_default='Want to Read'),
        sa.Column('rating', sa.Float(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.Date(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.Date(), onupdate=sa.func.now())
    )

def downgrade():
    op.drop_table('books')
    # Enum otomatis di-drop oleh PostgreSQL jika tidak dipakai lagi,
    # atau kamu bisa drop manual kalau perlu
    book_status_enum.drop(op.get_bind(), checkfirst=True)
