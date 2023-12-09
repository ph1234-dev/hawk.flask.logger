"""empty message

Revision ID: a4660a9aa9bc
Revises: 504c6027929e
Create Date: 2023-12-09 02:05:28.180125

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4660a9aa9bc'
down_revision = '504c6027929e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('usability_test_logs')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usability_test_logs',
    sa.Column('no', sa.INTEGER(), nullable=False),
    sa.Column('user_message', sa.VARCHAR(), nullable=False),
    sa.Column('reply', sa.VARCHAR(), nullable=False),
    sa.Column('predicted_language', sa.VARCHAR(), nullable=False),
    sa.Column('predicted_score', sa.NUMERIC(precision=3, scale=15), nullable=True),
    sa.Column('pattern_found', sa.VARCHAR(), nullable=False),
    sa.Column('original_pattern_found', sa.VARCHAR(), nullable=True),
    sa.Column('pattern_matching_method', sa.VARCHAR(), nullable=False),
    sa.Column('created_at', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('is_lang_correct', sa.BOOLEAN(), nullable=True),
    sa.Column('is_information_retrieved_valid', sa.BOOLEAN(), nullable=True),
    sa.Column('is_query_within_domain', sa.BOOLEAN(), nullable=True),
    sa.Column('test_number', sa.INTEGER(), nullable=True),
    sa.Column('reconstructed_message', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('no')
    )
    # ### end Alembic commands ###