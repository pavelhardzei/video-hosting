"""empty message

Revision ID: 2d6df7390d56
Revises: 46e92ad8d672
Create Date: 2022-11-13 08:08:33.081535

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '2d6df7390d56'
down_revision = '46e92ad8d672'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'userlibrary', ['object_type', 'object_id', 'user_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'userlibrary', type_='unique')
    # ### end Alembic commands ###