"""relations

Revision ID: de9de7fa3192
Revises: 980626dfe77c
Create Date: 2023-04-30 12:23:50.273643

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "de9de7fa3192"
down_revision = "980626dfe77c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("guardian", sa.Column("student_id", sa.BigInteger(), nullable=False))
    op.create_index(
        "idx__guardian_student_id", "guardian", ["student_id"], unique=False
    )
    op.create_foreign_key(None, "guardian", "auth_user", ["student_id"], ["id"])
    op.add_column("outpass", sa.Column("student_id", sa.BigInteger(), nullable=False))
    op.add_column("outpass", sa.Column("warden_id", sa.BigInteger(), nullable=True))
    op.create_foreign_key(None, "outpass", "auth_user", ["student_id"], ["id"])
    op.create_foreign_key(None, "outpass", "auth_user", ["warden_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "outpass", type_="foreignkey")
    op.drop_constraint(None, "outpass", type_="foreignkey")
    op.drop_column("outpass", "warden_id")
    op.drop_column("outpass", "student_id")
    op.drop_constraint(None, "guardian", type_="foreignkey")
    op.drop_index("idx__guardian_student_id", table_name="guardian")
    op.drop_column("guardian", "student_id")
    # ### end Alembic commands ###
