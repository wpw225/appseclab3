"""empty message

Revision ID: bafe821f3d8a
Revises: b691c95ecb21
Create Date: 2019-11-04 00:43:13.944365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bafe821f3d8a'
down_revision = 'b691c95ecb21'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('result', sa.String(length=1000), nullable=True))
    op.drop_index('ix_user_email', table_name='user')
    op.drop_column('user', 'email')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('email', sa.VARCHAR(length=120), nullable=True))
    op.create_index('ix_user_email', 'user', ['email'], unique=1)
    op.drop_column('post', 'result')
    # ### end Alembic commands ###