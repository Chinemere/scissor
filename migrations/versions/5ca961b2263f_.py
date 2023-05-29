"""empty message

Revision ID: 5ca961b2263f
Revises: 
Create Date: 2023-05-27 12:16:05.399515

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ca961b2263f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('urls', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('urls', schema=None) as batch_op:
        batch_op.drop_column('created_at')

    # ### end Alembic commands ###
