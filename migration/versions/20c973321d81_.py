"""empty message

Revision ID: 20c973321d81
Revises: 83388c4bb872
Create Date: 2024-04-01 14:30:19.777657

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20c973321d81'
down_revision: Union[str, None] = '83388c4bb872'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'tday', ['date'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tday', type_='unique')
    # ### end Alembic commands ###