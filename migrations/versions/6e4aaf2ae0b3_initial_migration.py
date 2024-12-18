"""Initial migration.

Revision ID: 6e4aaf2ae0b3
Revises: 
Create Date: 2024-12-12 10:52:20.227001

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e4aaf2ae0b3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('package', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_popular', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('package', schema=None) as batch_op:
        batch_op.drop_column('is_popular')

    # ### end Alembic commands ###
