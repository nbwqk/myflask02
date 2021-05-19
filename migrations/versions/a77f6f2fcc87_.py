"""empty message

Revision ID: a77f6f2fcc87
Revises: f6948d20bfa2
Create Date: 2021-05-12 08:19:26.469196

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a77f6f2fcc87'
down_revision = 'f6948d20bfa2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('messageboard',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('content', sa.String(length=255), nullable=False),
    sa.Column('mdatetime', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_foreign_key(None, 'aboutme', 'user', ['user_id'], ['id'])
    op.create_foreign_key(None, 'article', 'article_type', ['type_id'], ['id'])
    op.create_foreign_key(None, 'article', 'user', ['user_id'], ['id'])
    op.create_foreign_key(None, 'comment', 'article', ['article_id'], ['id'])
    op.create_foreign_key(None, 'comment', 'user', ['user_id'], ['id'])
    op.create_foreign_key(None, 'photo', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'photo', type_='foreignkey')
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.drop_constraint(None, 'article', type_='foreignkey')
    op.drop_constraint(None, 'article', type_='foreignkey')
    op.drop_constraint(None, 'aboutme', type_='foreignkey')
    op.drop_table('messageboard')
    # ### end Alembic commands ###