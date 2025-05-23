"""Adicionando colunas na tabela itemPedido

Revision ID: fdd03488186b
Revises: bebc191839be
Create Date: 2025-04-15 17:02:21.787599

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fdd03488186b'
down_revision = 'bebc191839be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('itens_pedido', schema=None) as batch_op:
        batch_op.add_column(sa.Column('produto_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('preco_unitario', sa.Numeric(precision=10, scale=2), nullable=False))
        batch_op.add_column(sa.Column('sub_total', sa.Numeric(precision=10, scale=2), nullable=False))
        batch_op.drop_constraint('itens_pedido_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(None, 'produtos', ['produto_id'], ['id'])
        batch_op.drop_column('preco')
        batch_op.drop_column('produtos_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('itens_pedido', schema=None) as batch_op:
        batch_op.add_column(sa.Column('produtos_id', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('preco', mysql.DECIMAL(precision=10, scale=2), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('itens_pedido_ibfk_2', 'produtos', ['produtos_id'], ['id'])
        batch_op.drop_column('sub_total')
        batch_op.drop_column('preco_unitario')
        batch_op.drop_column('produto_id')

    # ### end Alembic commands ###
