"""empty message

Revision ID: 96342916f2cf
Revises: 219ad6c027dd
Create Date: 2022-09-03 10:54:14.294547

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96342916f2cf'
down_revision = '219ad6c027dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('tag_x_post',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.PrimaryKeyConstraint('tag_id', 'post_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tag_x_post')
    op.drop_table('tag')
    # ### end Alembic commands ###
