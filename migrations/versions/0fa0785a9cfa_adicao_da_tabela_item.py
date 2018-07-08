"""adicao da tabela Item

Revision ID: 0fa0785a9cfa
Revises: 069f500aca25
Create Date: 2018-07-08 15:20:01.569375

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0fa0785a9cfa'
down_revision = '069f500aca25'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('unit', sa.String(length=8), nullable=True),
    sa.Column('quantity', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_item_name'), 'item', ['name'], unique=True)
    op.create_index(op.f('ix_item_unit'), 'item', ['unit'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_item_unit'), table_name='item')
    op.drop_index(op.f('ix_item_name'), table_name='item')
    op.drop_table('item')
    # ### end Alembic commands ###
