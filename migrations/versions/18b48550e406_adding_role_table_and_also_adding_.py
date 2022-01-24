"""Adding role table and also adding relationship column with user and role model

Revision ID: 18b48550e406
Revises: 371b5fabda8b
Create Date: 2022-01-23 23:20:19.318732

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '18b48550e406'
down_revision = '371b5fabda8b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('default', sa.Boolean(), server_default='false', nullable=True),
    sa.Column('permissions', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_roles_default'), 'roles', ['default'], unique=False)
    op.add_column('users', sa.Column('roles_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'roles', ['roles_id'], ['id'])
    op.drop_column('users', 'last_seen')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('last_seen', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'roles_id')
    op.drop_index(op.f('ix_roles_default'), table_name='roles')
    op.drop_table('roles')
    # ### end Alembic commands ###
