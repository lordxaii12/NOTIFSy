"""empty message

Revision ID: e3e4c97b0243
Revises: ef4b365c0868
Create Date: 2025-05-14 09:41:13.587093

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3e4c97b0243'
down_revision = 'ef4b365c0868'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('msg_log', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_ip', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('public_ip', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('msg_log', schema=None) as batch_op:
        batch_op.drop_column('public_ip')
        batch_op.drop_column('user_ip')

    # ### end Alembic commands ###
