"""empty message

Revision ID: 09ad485ea555
Revises: d26e4b912859
Create Date: 2021-05-19 23:06:04.141536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09ad485ea555'
down_revision = 'd26e4b912859'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('stock', 'image')
    op.drop_column('stock', 'ticker')
    op.drop_column('stock', 'segment')
    op.drop_column('stock', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stock', sa.Column('name', sa.VARCHAR(), nullable=False))
    op.add_column('stock', sa.Column('segment', sa.VARCHAR(), nullable=False))
    op.add_column('stock', sa.Column('ticker', sa.VARCHAR(), nullable=False))
    op.add_column('stock', sa.Column('image', sa.VARCHAR(), nullable=False))
    # ### end Alembic commands ###
