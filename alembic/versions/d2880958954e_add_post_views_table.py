"""add post views table

Revision ID: d2880958954e
Revises: b58696e7d034
Create Date: 2025-01-09 19:04:30.181754

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd2880958954e'
down_revision: Union[str, None] = 'b58696e7d034'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('post_views', 'post_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('post_views', 'post_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
