"""correcao da tabela Item

Revision ID: 67c3bdfc911a
Revises: 0fa0785a9cfa
Create Date: 2018-07-08 16:34:34.080337

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67c3bdfc911a'
down_revision = '0fa0785a9cfa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_item_name', table_name='item')
    op.create_index(op.f('ix_item_name'), 'item', ['name'], unique=False)
    op.drop_index('ix_item_unit', table_name='item')
    op.create_index(op.f('ix_item_unit'), 'item', ['unit'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_item_unit'), table_name='item')
    op.create_index('ix_item_unit', 'item', ['unit'], unique=1)
    op.drop_index(op.f('ix_item_name'), table_name='item')
    op.create_index('ix_item_name', 'item', ['name'], unique=1)
    # ### end Alembic commands ###