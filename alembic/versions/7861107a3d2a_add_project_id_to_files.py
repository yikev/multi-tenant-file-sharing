"""Add project_id to files

Revision ID: 7861107a3d2a
Revises: 2785cbab2bc6
Create Date: 2025-06-26 23:25:04.703817

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7861107a3d2a'
down_revision: Union[str, Sequence[str], None] = '2785cbab2bc6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('files', sa.Column('project_id', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('files', 'project_id')
    # ### end Alembic commands ###
