"""change column name of name_county to city

Revision ID: 9e5d33ff6cfa
Revises: f294c3951812
Create Date: 2022-05-02 17:16:23.649594

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9e5d33ff6cfa"
down_revision = "f294c3951812"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('spatial_ref_sys')
    op.add_column("cities", sa.Column("city", sa.String(), nullable=True))
    op.drop_index("idx_cities_geom", table_name="cities")
    op.drop_column("cities", "name_county")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "cities",
        sa.Column("name_county", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.create_index("idx_cities_geom", "cities", ["geom"], unique=False)
    op.drop_column("cities", "city")
    op.create_table(
        "spatial_ref_sys",
        sa.Column("srid", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(
            "auth_name", sa.VARCHAR(length=256), autoincrement=False, nullable=True
        ),
        sa.Column("auth_srid", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column(
            "srtext", sa.VARCHAR(length=2048), autoincrement=False, nullable=True
        ),
        sa.Column(
            "proj4text", sa.VARCHAR(length=2048), autoincrement=False, nullable=True
        ),
        sa.CheckConstraint(
            "(srid > 0) AND (srid <= 998999)", name="spatial_ref_sys_srid_check"
        ),
        sa.PrimaryKeyConstraint("srid", name="spatial_ref_sys_pkey"),
    )
    # ### end Alembic commands ###
