"""votes_new

Revision ID: 6bfcd3cb283a
Revises: da97b9878266
Create Date: 2020-11-15 21:22:09.413077

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6bfcd3cb283a'
down_revision = 'da97b9878266'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vote',
    sa.Column('choice_id', sa.Integer(), nullable=False),
    sa.Column('profile', sa.Integer(), nullable=False),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['choice_id'], ['choice.id'], ),
    sa.ForeignKeyConstraint(['profile'], ['profile.id'], ),
    sa.PrimaryKeyConstraint('choice_id', 'profile')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vote')
    # ### end Alembic commands ###
