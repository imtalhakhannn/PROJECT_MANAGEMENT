"""Add UserTasks table

Revision ID: 300aed5ef478
Revises: 7a67a4d19a9c
Create Date: 2025-07-09 19:11:15.865986

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '300aed5ef478'
down_revision: Union[str, Sequence[str], None] = '7a67a4d19a9c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
