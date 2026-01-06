"""create car tables

Revision ID: 20241202_02
Revises: 20241202_01
Create Date: 2025-12-02 00:00:01.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20241202_02"
down_revision: Union[str, None] = "20241202_01"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create car_makes table
    op.create_table(
        "car_makes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create car_models table
    op.create_table(
        "car_models",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("make_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["make_id"], ["car_makes.id"], ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create car_years table
    op.create_table(
        "car_years",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("model_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["model_id"], ["car_models.id"], ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("model_id", "year", name="uq_car_year_model_year"),
    )


def downgrade() -> None:
    op.drop_table("car_years")
    op.drop_table("car_models")
    op.drop_table("car_makes")
