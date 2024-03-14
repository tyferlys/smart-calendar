"""empty message

Revision ID: 86b663100371
Revises: f3c6468f4c83
Create Date: 2024-03-14 13:39:01.804326

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86b663100371'
down_revision: Union[str, None] = 'f3c6468f4c83'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('toptions_client',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_client', sa.Integer(), nullable=False),
    sa.Column('is_notification', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['id_client'], ['tclient.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('toptions_client')
    # ### end Alembic commands ###