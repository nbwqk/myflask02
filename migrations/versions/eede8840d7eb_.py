"""empty message

Revision ID: eede8840d7eb
Revises: 9ba4dc065588
Create Date: 2021-04-20 15:33:45.429956

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eede8840d7eb'
down_revision = '9ba4dc065588'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'article', 'article_type', ['type_id'], ['id'])
    op.create_foreign_key(None, 'article', 'user', ['user_id'], ['id'])
    op.create_foreign_key(None, 'comment', 'article', ['article_id'], ['id'])
    op.create_foreign_key(None, 'comment', 'user', ['user_id'], ['id'])
    op.add_column('user', sa.Column('email', sa.String(length=30), nullable=True))
    op.add_column('user', sa.Column('icon', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'icon')
    op.drop_column('user', 'email')
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.drop_constraint(None, 'article', type_='foreignkey')
    op.drop_constraint(None, 'article', type_='foreignkey')
    # ### end Alembic commands ###
