"""Adding last member_since column

Revision ID: 371b5fabda8b
Revises: 94dce4534ad6
Create Date: 2022-01-22 22:14:15.881895

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '371b5fabda8b'
down_revision = '94dce4534ad6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('member_since', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'member_since')
    # ### end Alembic commands ###