"""add fields to stock

Revision ID: 3d8c45912f04
Revises: 796dda17402b
Create Date: 2021-05-19 22:54:00.495920

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d8c45912f04'
down_revision = '796dda17402b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stock', sa.Column('ticker', sa.Text(), nullable=True))
    op.drop_column('stock', '_ticker')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stock', sa.Column('_ticker', sa.FLOAT(), nullable=True))
    op.drop_column('stock', 'ticker')
    # ### end Alembic commands ###
