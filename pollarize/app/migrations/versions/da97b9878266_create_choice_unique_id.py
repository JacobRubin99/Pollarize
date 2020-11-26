"""create choice unique id

Revision ID: da97b9878266
Revises: 1aec5328c6b1
Create Date: 2020-11-14 16:17:43.403085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da97b9878266'
down_revision = '1aec5328c6b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('choice',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('poll_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=300), nullable=True),
    sa.Column('date_added', sa.Date(), nullable=True),
    sa.Column('creator_user_id', sa.Integer(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['creator_user_id'], ['profile.id'], ),
    sa.ForeignKeyConstraint(['poll_id'], ['poll.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('choice')
    # ### end Alembic commands ###
