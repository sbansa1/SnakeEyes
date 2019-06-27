"""empty message

Revision ID: e6ff1556d6c7
Revises: 0253d01cbef9
Create Date: 2019-06-22 15:32:52.607233

"""
from alembic import op
import sqlalchemy as sa

import app

# revision identifiers, used by Alembic.
revision = 'e6ff1556d6c7'
down_revision = '0253d01cbef9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('credit_cards',
    sa.Column('created', app.lib.utility_sqlalchemy.AwareDateTime(), nullable=True),
    sa.Column('updated', app.lib.utility_sqlalchemy.AwareDateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('brand', sa.String(length=128), nullable=True),
    sa.Column('last4', sa.Integer(), nullable=True),
    sa.Column('expiry_date', sa.Date(), nullable=True),
    sa.Column('is_expiring', sa.Boolean(), server_default='0', nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_credit_cards_expiry_date'), 'credit_cards', ['expiry_date'], unique=False)
    op.create_index(op.f('ix_credit_cards_id'), 'credit_cards', ['id'], unique=False)
    op.create_index(op.f('ix_credit_cards_user_id'), 'credit_cards', ['user_id'], unique=False)
    op.add_column('users', sa.Column('cancelled_subscription_on', app.lib.utility_sqlalchemy.AwareDateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'cancelled_subscription_on')
    op.drop_index(op.f('ix_credit_cards_user_id'), table_name='credit_cards')
    op.drop_index(op.f('ix_credit_cards_id'), table_name='credit_cards')
    op.drop_index(op.f('ix_credit_cards_expiry_date'), table_name='credit_cards')
    op.drop_table('credit_cards')
    # ### end Alembic commands ###