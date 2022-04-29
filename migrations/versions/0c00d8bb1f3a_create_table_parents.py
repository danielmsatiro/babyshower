"""create table parents

Revision ID: 0c00d8bb1f3a
Revises: f967c2acb1d8
Create Date: 2022-04-26 10:13:51.308754

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0c00d8bb1f3a"
down_revision = "f967c2acb1d8"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "parents",
        sa.Column("cpf", sa.Integer(), nullable=False, unique=True),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("phone", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_foreign_key(None, "products", "parents", ["parent_id"], ["cpf"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "products", type_="foreignkey")
    op.drop_table("parents")
    # ### end Alembic commands ###
