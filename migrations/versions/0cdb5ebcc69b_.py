"""empty message

Revision ID: 0cdb5ebcc69b
Revises: f2f8500de19c
Create Date: 2021-04-19 10:25:04.774340

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0cdb5ebcc69b'
down_revision = 'f2f8500de19c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('article',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('pdatetime', sa.DateTime(), nullable=True),
    sa.Column('click_num', sa.Integer(), nullable=True),
    sa.Column('save_num', sa.Integer(), nullable=True),
    sa.Column('love_num', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('article')
    # ### end Alembic commands ###
