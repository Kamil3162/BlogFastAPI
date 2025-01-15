"""fix relationship between PostCategories and PostCategory

Revision ID: f96706f798de
Revises: 8e39f2324b41
Create Date: 2025-01-15 18:40:27.811488

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f96706f798de'
down_revision: Union[str, None] = '8e39f2324b41'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('posts_categories_category_id_fkey', 'posts_categories', type_='foreignkey')
    op.drop_column('posts_categories', 'category_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts_categories', sa.Column('category_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('posts_categories_category_id_fkey', 'posts_categories', 'categories', ['category_id'], ['id'])
    # ### end Alembic commands ###
