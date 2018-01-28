"""empty message

Revision ID: 5121645a1da4
Revises: 0e720768c82a
Create Date: 2018-01-28 12:28:26.039619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5121645a1da4'
down_revision = '0e720768c82a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('score', sa.Float(precision=5), nullable=True, server_default="5.0"))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'score')
    # ### end Alembic commands ###