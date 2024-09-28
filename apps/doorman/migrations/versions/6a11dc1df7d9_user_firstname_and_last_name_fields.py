"""user firstname and last name fields

Revision ID: 6a11dc1df7d9
Revises: a4ac7f4dfb72
Create Date: 2024-09-21 07:26:11.230232

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6a11dc1df7d9"
down_revision: Union[str, None] = "a4ac7f4dfb72"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column(
        table_name="users",
        column_name="name",
    )
    op.add_column(
        table_name="users",
        column=sa.Column(
            "first_name",
            sqlmodel.sql.sqltypes.AutoString(length=64),
            nullable=False,
        ),
    )
    op.add_column(
        table_name="users",
        column=sa.Column(
            "last_name",
            sqlmodel.sql.sqltypes.AutoString(length=64),
            nullable=False,
        ),
    )


def downgrade() -> None:
    pass
