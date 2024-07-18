"""Add phone_number Column to users table.

Revision ID: c8e45be2f291
Revises: 
Create Date: 2024-07-17 14:15:49.658931

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c8e45be2f291"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("phone_number", sa.String, nullable=True))


def downgrade() -> None:
    op.drop_column("users", "phone_number")
