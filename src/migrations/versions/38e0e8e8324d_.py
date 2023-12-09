"""empty message

Revision ID: 38e0e8e8324d
Revises: abcdc8208809
Create Date: 2023-05-30 01:19:27.313588

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38e0e8e8324d'
down_revision = 'abcdc8208809'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_dev_environment_test_logs')
    with op.batch_alter_table('dev_environment_test_logs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_information_retrieved_valid', sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column('is_query_within_domain', sa.Boolean(), nullable=False))
        batch_op.drop_column('is_reply_correct')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('dev_environment_test_logs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_reply_correct', sa.BOOLEAN(), nullable=False))
        batch_op.drop_column('is_query_within_domain')
        batch_op.drop_column('is_information_retrieved_valid')

    op.create_table('_alembic_tmp_dev_environment_test_logs',
    sa.Column('no', sa.INTEGER(), nullable=False),
    sa.Column('user_message', sa.VARCHAR(), nullable=False),
    sa.Column('reply', sa.VARCHAR(), nullable=False),
    sa.Column('predicted_language', sa.VARCHAR(), nullable=False),
    sa.Column('predicted_dimension_number', sa.INTEGER(), nullable=False),
    sa.Column('predicted_dimension_label', sa.VARCHAR(), nullable=False),
    sa.Column('pattern_found', sa.VARCHAR(), nullable=False),
    sa.Column('pattern_matching_method', sa.VARCHAR(), nullable=False),
    sa.Column('created_at', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('is_lang_correct', sa.BOOLEAN(), nullable=False),
    sa.Column('test_number', sa.INTEGER(), nullable=True),
    sa.Column('predicted_score', sa.NUMERIC(precision=3, scale=15), nullable=True),
    sa.Column('reconstructed_message', sa.VARCHAR(), nullable=True),
    sa.Column('is_information_retrieved_valid', sa.BOOLEAN(), nullable=False),
    sa.Column('is_query_within_domain', sa.BOOLEAN(), nullable=False),
    sa.PrimaryKeyConstraint('no')
    )
    # ### end Alembic commands ###
