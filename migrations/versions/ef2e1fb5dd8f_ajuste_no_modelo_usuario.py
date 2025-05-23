"""Ajuste no modelo Usuario

Revision ID: ef2e1fb5dd8f
Revises: 223dfa381880
Create Date: 2024-12-03 21:20:47.758606

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ef2e1fb5dd8f'
down_revision = '223dfa381880'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('produtos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nome', sa.String(length=50), nullable=False))
        batch_op.drop_column('nome_produto')

    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nome', sa.String(length=50), nullable=False))
        batch_op.drop_index('nome_usuario')
        batch_op.create_unique_constraint(None, ['nome'])
        batch_op.drop_column('nome_usuario')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nome_usuario', mysql.VARCHAR(length=50), nullable=False))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.create_index('nome_usuario', ['nome_usuario'], unique=True)
        batch_op.drop_column('nome')

    with op.batch_alter_table('produtos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nome_produto', mysql.VARCHAR(length=50), nullable=False))
        batch_op.drop_column('nome')

    # ### end Alembic commands ###
