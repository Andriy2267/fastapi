"""add content column to posts table

Revision ID: 87c6ac9c10a2
Revises: adece16b5c7f
Create Date: 2025-04-01 19:41:40.438078

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '87c6ac9c10a2'
down_revision: Union[str, None] = 'adece16b5c7f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
    pass
