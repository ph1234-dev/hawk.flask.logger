"""empty message

Revision ID: b617e1951d6b
Revises: 30464ea1f91f
Create Date: 2023-03-12 01:24:23.052204

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b617e1951d6b'
down_revision = '30464ea1f91f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('log', schema=None) as batch_op:
        batch_op.add_column(sa.Column('predicted_message_language', sa.String(), server_default='', nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('log', schema=None) as batch_op:
        batch_op.drop_column('predicted_message_language')

    # ### end Alembic commands ###
