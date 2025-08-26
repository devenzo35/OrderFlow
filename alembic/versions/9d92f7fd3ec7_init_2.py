"""init 2

Revision ID: 9d92f7fd3ec7
Revises: e7bca561ff16
Create Date: 2025-08-26 14:13:39.254292

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "9d92f7fd3ec7"
down_revision: Union[str, Sequence[str], None] = "e7bca561ff16"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Cambiar age de VARCHAR a INTEGER
    op.alter_column(
        "users",
        "age",
        existing_type=sa.VARCHAR(),
        type_=sa.Integer(),
        existing_nullable=False,
        postgresql_using="age::integer",
    )

    # Cambiar created_at a timezone-aware
    op.alter_column(
        "users",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=False),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
    )


def downgrade() -> None:
    # Cambiar age de VARCHAR a INTEGER
    op.alter_column(
        "users",
        "age",
        existing_type=sa.Integer(),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )

    # Cambiar created_at a timezone-aware
    op.alter_column(
        "users",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=sa.TIMESTAMP(timezone=False),
        existing_nullable=False,
    )
