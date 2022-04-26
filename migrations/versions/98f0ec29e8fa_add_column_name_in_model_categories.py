"""add column name in model categories

Revision ID: 98f0ec29e8fa
Revises: 54f9fbd967eb
Create Date: 2022-04-26 15:08:32.164267

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98f0ec29e8fa'
down_revision = '54f9fbd967eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('categories', sa.Column('name', sa.String(length=128), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('categories', 'name')
    # ### end Alembic commands ###
