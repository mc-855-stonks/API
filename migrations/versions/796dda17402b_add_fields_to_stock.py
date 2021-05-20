"""add fields to stock

Revision ID: 796dda17402b
Revises: e325b9bc92d4
Create Date: 2021-05-19 22:53:25.314765

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '796dda17402b'
down_revision = 'e325b9bc92d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stock', sa.Column('image', sa.Text(), nullable=True))
    op.add_column('stock', sa.Column('segment', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('stock', 'segment')
    op.drop_column('stock', 'image')
    # ### end Alembic commands ###