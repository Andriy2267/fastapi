"""auto_vote

Revision ID: 1cbe5d1fef28
Revises: 3badecd2b1e0
Create Date: 2025-04-01 20:07:22.122912

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1cbe5d1fef28'
down_revision: Union[str, None] = '3badecd2b1e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("votes",
                    sa.Column("user_id", sa.Integer(), nullable=False),
                    sa.Column("post_id", sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(["post_id"], ["posts.id"], ondelete="CASCADE"),
                    sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
                    sa.PrimaryKeyConstraint("user_id", "post_id")
                    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("votes")
    pass
