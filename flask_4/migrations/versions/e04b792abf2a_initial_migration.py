"""Initial migration.

Revision ID: e04b792abf2a
Revises: 
Create Date: 2022-09-07 22:32:45.941060

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e04b792abf2a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('books')
    op.drop_table('readers')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('readers',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('subname', sa.VARCHAR(length=50), nullable=True),
    sa.Column('name', sa.VARCHAR(length=50), nullable=True),
    sa.Column('patronymic', sa.VARCHAR(length=50), nullable=True),
    sa.Column('phone', sa.INTEGER(), nullable=True),
    sa.Column('date', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('books',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('tour_package_id', sa.INTEGER(), nullable=True),
    sa.Column('author', sa.VARCHAR(length=50), nullable=True),
    sa.Column('name_book', sa.VARCHAR(length=100), nullable=True),
    sa.ForeignKeyConstraint(['tour_package_id'], ['readers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
