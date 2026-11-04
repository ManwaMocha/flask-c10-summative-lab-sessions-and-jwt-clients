
"""Add Category model and note category relationship

Revision ID: 39de2fbd7e59
Revises: a4991525f300
"""

from alembic import op
import sqlalchemy as sa


revision = '39de2fbd7e59'
down_revision = 'a4991525f300'
branch_labels = None
depends_on = None


def upgrade():
    # Create the categories table
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False, unique=True)
    )

    # Add category_id to the notes table
    with op.batch_alter_table('notes') as batch_op:
        batch_op.add_column(
            sa.Column('category_id', sa.Integer(), nullable=True)
        )

        batch_op.create_foreign_key(
            'fk_notes_category_id',
            'categories',
            ['category_id'],
            ['id']
        )


def downgrade():
    # Remove the foreign key and category_id column
    with op.batch_alter_table('notes') as batch_op:
        batch_op.drop_constraint(
            'fk_notes_category_id',
            type_='foreignkey'
        )

        batch_op.drop_column('category_id')

    # Remove the categories table
    op.drop_table('categories')
