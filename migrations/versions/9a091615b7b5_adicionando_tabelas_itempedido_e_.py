"""Adicionando tabelas ItemPedido e Pagamento

Revision ID: 9a091615b7b5
Revises: 5fc094902aee
Create Date: 2024-11-26 19:50:21.668907

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a091615b7b5'
down_revision = '5fc094902aee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('itens_pedido',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pedido_id', sa.Integer(), nullable=False),
    sa.Column('produtos_id', sa.Integer(), nullable=False),
    sa.Column('quantidade', sa.Integer(), nullable=False),
    sa.Column('preco', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.ForeignKeyConstraint(['pedido_id'], ['pedidos.id'], ),
    sa.ForeignKeyConstraint(['produtos_id'], ['produtos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pagamentos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pedido_id', sa.Integer(), nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('data_pagamento', sa.DateTime(), nullable=False),
    sa.Column('metodo_pagamento', sa.String(length=50), nullable=False),
    sa.Column('valor_pagamento', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('status_pagamento', sa.String(length=20), nullable=False),
    sa.Column('data_confirmacao', sa.DateTime(), nullable=True),
    sa.Column('detalhes_pagamento', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['pedido_id'], ['pedidos.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pagamentos')
    op.drop_table('itens_pedido')
    # ### end Alembic commands ###
