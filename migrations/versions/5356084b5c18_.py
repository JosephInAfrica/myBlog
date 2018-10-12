"""empty message

Revision ID: 5356084b5c18
Revises: 
Create Date: 2018-10-12 16:42:06.733852

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5356084b5c18'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_column('users', 'email')
    # ### end Alembic commands ###
