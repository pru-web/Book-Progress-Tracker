"""Add publish_year column to books and drop extra tables

Revision ID: 2b63cf0890ad
Revises: 
Create Date: 2024-10-23 00:02:15.037601

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b63cf0890ad'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add the new column 'publish_year' to the 'books' table
    op.add_column('books', sa.Column('publish_year', sa.Integer))

    # Drop the unnecessary 'admin_new' and 'books_new' tables if they exist
    op.drop_table('admin_new')
    op.drop_table('books_new')


def downgrade():
    # Reverse the changes
    op.drop_column('books', 'publish_year')

    # Recreate the tables in case of downgrade (optional)
    op.create_table(
        'admin_new',
        sa.Column('admin_id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('password', sa.String, nullable=False),
    )
    op.create_table(
        'books_new',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('author', sa.String, nullable=False),
    )