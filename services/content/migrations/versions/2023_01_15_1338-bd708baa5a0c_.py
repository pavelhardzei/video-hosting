"""empty message

Revision ID: bd708baa5a0c
Revises: d4f392b66a71
Create Date: 2023-01-15 13:38:12.804370

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'bd708baa5a0c'
down_revision = 'd4f392b66a71'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('playlistitem_object_type_object_id_key', 'playlistitem', type_='unique')
    op.create_unique_constraint(None, 'playlistitem', ['object_type', 'object_id', 'playlist_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'playlistitem', type_='unique')
    op.create_unique_constraint('playlistitem_object_type_object_id_key', 'playlistitem', ['object_type', 'object_id'])
    # ### end Alembic commands ###