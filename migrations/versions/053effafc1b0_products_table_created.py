"""products table created

Revision ID: 053effafc1b0
Revises: 
Create Date: 2022-04-25 17:16:51.541884

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '053effafc1b0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=128), nullable=False),
    sa.Column('price', sa.Numeric(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.VARCHAR(), nullable=True),
    sa.Column('image', sa.VARCHAR(), nullable=True),
    sa.Column('sold', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('products')
    # ### end Alembic commands ###
