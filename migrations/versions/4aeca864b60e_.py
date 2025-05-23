"""empty message

Revision ID: 4aeca864b60e
Revises: a85f04fda966
Create Date: 2025-04-24 16:10:16.188910

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4aeca864b60e'
down_revision = 'a85f04fda966'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('divisions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('division_credits', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('divisions', schema=None) as batch_op:
        batch_op.drop_column('division_credits')

    # ### end Alembic commands ###
