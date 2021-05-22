"""historical data

Revision ID: a6f3876c3989
Revises: b98c35e3360c
Create Date: 2021-05-22 15:48:34.414093

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6f3876c3989'
down_revision = 'b98c35e3360c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stock_history',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('open', sa.Float(), nullable=False),
    sa.Column('high', sa.Float(), nullable=False),
    sa.Column('low', sa.Float(), nullable=False),
    sa.Column('close', sa.Float(), nullable=False),
    sa.Column('volume', sa.BigInteger(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('last_update_date', sa.Date(), nullable=False),
    sa.Column('stock_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['stock_id'], ['stock.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stock_history')
    # ### end Alembic commands ###