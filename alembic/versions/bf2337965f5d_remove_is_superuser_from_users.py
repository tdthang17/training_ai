"""remove is_superuser from users

Revision ID: bf2337965f5d
Revises: 198e280bf64f
Create Date: 2025-07-10 14:10:14.209577

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf2337965f5d'
down_revision: Union[str, Sequence[str], None] = '198e280bf64f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_superuser', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_superuser')
    # ### end Alembic commands ###
