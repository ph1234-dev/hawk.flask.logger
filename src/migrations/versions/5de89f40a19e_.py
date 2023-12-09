"""empty message

Revision ID: 5de89f40a19e
Revises: 3e336029f471
Create Date: 2023-05-02 04:45:59.698203

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5de89f40a19e'
down_revision = '3e336029f471'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('dev_environment_test_logs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reconstructed_message', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('dev_environment_test_logs', schema=None) as batch_op:
        batch_op.drop_column('reconstructed_message')

    # ### end Alembic commands ###
