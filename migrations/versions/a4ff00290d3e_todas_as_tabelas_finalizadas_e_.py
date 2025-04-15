"""Todas as tabelas finalizadas e atualizadas

Revision ID: a4ff00290d3e
Revises: afc284227f59
Create Date: 2025-04-15 20:13:31.995020

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a4ff00290d3e'
down_revision = 'afc284227f59'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('status_pedido',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.String(length=50), nullable=False),
    sa.Column('descricao', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('categorias', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nome', sa.String(length=50), nullable=False))
        batch_op.add_column(sa.Column('descricao', sa.Text(), nullable=False))
        batch_op.add_column(sa.Column('imagem', sa.String(length=100), nullable=False))
        batch_op.drop_index('nome_categoria')
        batch_op.create_unique_constraint(None, ['nome'])
        batch_op.drop_column('nome_categoria')

    with op.batch_alter_table('estoque', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ingrediente_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('quantidade_disponivel', sa.Integer(), nullable=False))
        batch_op.drop_constraint('estoque_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'ingredientes', ['ingrediente_id'], ['id'])
        batch_op.drop_column('quantidade')
        batch_op.drop_column('produto_id')
        batch_op.drop_column('atualizado_em')

    with op.batch_alter_table('pagamentos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nome', sa.String(length=50), nullable=False))
        batch_op.add_column(sa.Column('descricao', sa.Text(), nullable=False))
        batch_op.drop_constraint('pagamentos_ibfk_2', type_='foreignkey')
        batch_op.drop_constraint('pagamentos_ibfk_1', type_='foreignkey')
        batch_op.drop_column('usuario_id')
        batch_op.drop_column('status_pagamento')
        batch_op.drop_column('pedido_id')
        batch_op.drop_column('metodo_pagamento')
        batch_op.drop_column('data_pagamento')
        batch_op.drop_column('valor_pagamento')
        batch_op.drop_column('data_confirmacao')
        batch_op.drop_column('detalhes_pagamento')

    with op.batch_alter_table('pedidos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('endereco_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('pagamento_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('pedidos_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(None, 'enderecos', ['endereco_id'], ['id'])
        batch_op.create_foreign_key(None, 'status_pedido', ['status_id'], ['id'])
        batch_op.create_foreign_key(None, 'pagamentos', ['pagamento_id'], ['id'])
        batch_op.drop_column('endereço_de_entrega_id')
        batch_op.drop_column('forma_de_pagamento')
        batch_op.drop_column('status_do_pedido')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pedidos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status_do_pedido', mysql.VARCHAR(length=20), nullable=False))
        batch_op.add_column(sa.Column('forma_de_pagamento', mysql.DECIMAL(precision=10, scale=2), nullable=False))
        batch_op.add_column(sa.Column('endereço_de_entrega_id', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('pedidos_ibfk_2', 'enderecos', ['endereço_de_entrega_id'], ['id'])
        batch_op.drop_column('pagamento_id')
        batch_op.drop_column('endereco_id')
        batch_op.drop_column('status_id')

    with op.batch_alter_table('pagamentos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('detalhes_pagamento', mysql.TEXT(), nullable=True))
        batch_op.add_column(sa.Column('data_confirmacao', mysql.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column('valor_pagamento', mysql.DECIMAL(precision=10, scale=2), nullable=False))
        batch_op.add_column(sa.Column('data_pagamento', mysql.DATETIME(), nullable=False))
        batch_op.add_column(sa.Column('metodo_pagamento', mysql.VARCHAR(length=50), nullable=False))
        batch_op.add_column(sa.Column('pedido_id', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('status_pagamento', mysql.VARCHAR(length=20), nullable=False))
        batch_op.add_column(sa.Column('usuario_id', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('pagamentos_ibfk_1', 'pedidos', ['pedido_id'], ['id'])
        batch_op.create_foreign_key('pagamentos_ibfk_2', 'usuarios', ['usuario_id'], ['id'])
        batch_op.drop_column('descricao')
        batch_op.drop_column('nome')

    with op.batch_alter_table('estoque', schema=None) as batch_op:
        batch_op.add_column(sa.Column('atualizado_em', mysql.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column('produto_id', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('quantidade', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('estoque_ibfk_1', 'produtos', ['produto_id'], ['id'])
        batch_op.drop_column('quantidade_disponivel')
        batch_op.drop_column('ingrediente_id')

    with op.batch_alter_table('categorias', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nome_categoria', mysql.VARCHAR(length=50), nullable=False))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.create_index('nome_categoria', ['nome_categoria'], unique=True)
        batch_op.drop_column('imagem')
        batch_op.drop_column('descricao')
        batch_op.drop_column('nome')

    op.drop_table('status_pedido')
    # ### end Alembic commands ###
