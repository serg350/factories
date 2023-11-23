"""create inital tables

Revision ID: 2209c1db7b72
Revises: 
Create Date: 2023-11-23 10:54:27.804327

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '2209c1db7b72'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('factories',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_factories_name'), 'factories', ['name'], unique=False)
    op.create_table('reviews',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.Column('satisfaction_level', sa.Enum('Great', 'Normally', 'Badly', name='satisfactionlevelenum'), nullable=True),
    sa.Column('factory_id', postgresql.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['factory_id'], ['factories.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reviews')
    op.drop_index(op.f('ix_factories_name'), table_name='factories')
    op.drop_table('factories')
    # ### end Alembic commands ###
