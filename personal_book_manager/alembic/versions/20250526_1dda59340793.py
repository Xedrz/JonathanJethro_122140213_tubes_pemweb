"""update models book user

Revision ID: 1dda59340793
Revises: a28dfa955563
Create Date: 2025-05-26 10:25:56.714244

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1dda59340793'
down_revision = 'a28dfa955563'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('revoked_tokens', 'jti',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(length=64),
               nullable=False)
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('users', 'password_hash',
               existing_type=sa.TEXT(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password_hash',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('revoked_tokens', 'jti',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###
