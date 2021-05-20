"""change text to unicode

Revision ID: 2653b38097cf
Revises: 2a4585981398
Create Date: 2021-05-19 22:56:03.187377

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2653b38097cf'
down_revision = '2a4585981398'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stock', sa.Column('name', sa.Unicode(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('stock', 'name')
    # ### end Alembic commands ###
