"""model_parents: change type column cpf: Integer to BigInteger

Revision ID: 4aca4bcc4328
Revises: cfd70f846b72
Create Date: 2022-04-26 19:11:17.091427

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4aca4bcc4328"
down_revision = "cfd70f846b72"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "answers",
        "parent_id",
        existing_type=sa.INTEGER(),
        type_=sa.BigInteger(),
        existing_nullable=False,
    )
    op.alter_column(
        "parents",
        "cpf",
        existing_type=sa.INTEGER(),
        type_=sa.BigInteger(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "parents",
        "cpf",
        existing_type=sa.BigInteger(),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.alter_column(
        "answers",
        "parent_id",
        existing_type=sa.BigInteger(),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
