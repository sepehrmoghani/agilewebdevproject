"""profile_pic

Revision ID: 84935853443e
Revises: 46ade310e0f8
Create Date: 2025-05-14 12:34:53.365935

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84935853443e'
down_revision = '46ade310e0f8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_pic', sa.String(length=128), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('profile_pic')

    # ### end Alembic commands ###
