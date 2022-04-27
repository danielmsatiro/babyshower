"""Consertando table answer

Revision ID: 006b1f759b6b
Revises: 4772d8e2a3e3
Create Date: 2022-04-27 11:31:55.888291

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '006b1f759b6b'
down_revision = '4772d8e2a3e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('answers', 'answer',
               existing_type=sa.VARCHAR(length=150),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('answers', 'answer',
               existing_type=sa.VARCHAR(length=150),
               nullable=True)
    # ### end Alembic commands ###