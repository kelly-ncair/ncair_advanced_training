"""merge heads

Revision ID: 50a2171e8d0b
Revises: 3d14dc9c862b, 7a3a45673bab
Create Date: 2025-06-16 22:05:16.921370

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50a2171e8d0b'
down_revision: Union[str, None] = ('3d14dc9c862b', '7a3a45673bab')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
