"""Create user table

Revision ID: 5676992fef6a
Revises: 
Create Date: 2024-09-18 15:10:08.114800

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5676992fef6a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dbproject',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('price', sa.String(length=50), nullable=True),
    sa.Column('location', sa.String(length=255), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.Column('source', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('url')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=150),
               existing_nullable=False)
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=150),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=150),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.alter_column('username',
               existing_type=sa.String(length=150),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)

    op.drop_table('dbproject')
    # ### end Alembic commands ###