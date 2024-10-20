"""primera migracion

Revision ID: 4a10654cb2bb
Revises: 
Create Date: 2024-10-18 09:23:01.150916

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4a10654cb2bb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('formulas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(), nullable=True),
    sa.Column('medicamentos', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('estado', sa.Enum('solicitado', 'en_proceso', 'enviado', 'recibido', name='estadoenvio'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_formulas_id'), 'formulas', ['id'], unique=False)
    op.create_table('medicamentos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(), nullable=True),
    sa.Column('existencia', sa.Integer(), nullable=True),
    sa.Column('gramaje', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_medicamentos_id'), 'medicamentos', ['id'], unique=False)
    op.create_index(op.f('ix_medicamentos_nombre'), 'medicamentos', ['nombre'], unique=False)
    op.create_table('pedidos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('solicitante', sa.String(), nullable=True),
    sa.Column('medicamento_id', sa.Integer(), nullable=True),
    sa.Column('cantidad', sa.Integer(), nullable=True),
    sa.Column('estado', sa.Enum('solicitado', 'en_proceso', 'enviado', 'recibido', name='estadoenvio'), nullable=True),
    sa.ForeignKeyConstraint(['medicamento_id'], ['medicamentos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_pedidos_id'), 'pedidos', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_pedidos_id'), table_name='pedidos')
    op.drop_table('pedidos')
    op.drop_index(op.f('ix_medicamentos_nombre'), table_name='medicamentos')
    op.drop_index(op.f('ix_medicamentos_id'), table_name='medicamentos')
    op.drop_table('medicamentos')
    op.drop_index(op.f('ix_formulas_id'), table_name='formulas')
    op.drop_table('formulas')
    # ### end Alembic commands ###
