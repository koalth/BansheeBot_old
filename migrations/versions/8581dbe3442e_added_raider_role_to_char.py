"""added raider role to char

Revision ID: 8581dbe3442e
Revises: 456da342209b
Create Date: 2024-09-03 18:31:14.102606

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8581dbe3442e'
down_revision: Union[str, None] = '456da342209b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('characters', sa.Column('on_raid_roster', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('characters', 'on_raid_roster')
    # ### end Alembic commands ###