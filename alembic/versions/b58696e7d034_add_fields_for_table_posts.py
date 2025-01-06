"""add fields for table posts

Revision ID: b58696e7d034
Revises: 8a0ecaaafad0
Create Date: 2025-01-04 17:31:51.049967

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b58696e7d034'
down_revision: Union[str, None] = '8a0ecaaafad0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
