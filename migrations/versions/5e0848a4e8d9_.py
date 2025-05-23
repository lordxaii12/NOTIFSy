"""empty message

Revision ID: 5e0848a4e8d9
Revises: 1d2070bfafc8
Create Date: 2025-03-26 13:40:10.457765

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e0848a4e8d9'
down_revision = '1d2070bfafc8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sys_setting', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sys_app_itexmo_credits_url', sa.String(length=900), nullable=True))
        batch_op.add_column(sa.Column('sys_app_eprocsys_supplier_url', sa.String(length=900), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sys_setting', schema=None) as batch_op:
        batch_op.drop_column('sys_app_eprocsys_supplier_url')
        batch_op.drop_column('sys_app_itexmo_credits_url')

    # ### end Alembic commands ###
