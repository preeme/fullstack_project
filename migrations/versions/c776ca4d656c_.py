"""empty message

Revision ID: c776ca4d656c
Revises: cc75ad9991ca
Create Date: 2017-09-07 14:49:09.337483

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c776ca4d656c'
down_revision = 'cc75ad9991ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('locations', sa.Column('lng', sa.Float(), nullable=True))
    op.drop_column('locations', 'long')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('locations', sa.Column('long', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.drop_column('locations', 'lng')
    # ### end Alembic commands ###
