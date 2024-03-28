"""empty message

Revision ID: 83388c4bb872
Revises: 69b770463d6e
Create Date: 2024-03-28 16:44:14.822986

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '83388c4bb872'
down_revision: Union[str, None] = '69b770463d6e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tevent', 'time',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               type_=sa.Time(timezone=True),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tevent', 'time',
               existing_type=sa.Time(timezone=True),
               type_=postgresql.TIMESTAMP(timezone=True),
               existing_nullable=False)
    # ### end Alembic commands ###
