"""adding keyword table

Revision ID: ac566085cd64
Revises: 
Create Date: 2022-02-08 01:14:23.091016

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac566085cd64'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_keywords')
    op.create_unique_constraint(None, 'keywords', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'keywords', type_='unique')
    op.create_table('post_keywords',
    sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('keywords_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['keywords_id'], ['keywords.id'], name='post_keywords_keywords_id_fkey'),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name='post_keywords_post_id_fkey'),
    sa.PrimaryKeyConstraint('post_id', name='post_keywords_pkey')
    )
    # ### end Alembic commands ###
