"""Synced with PascalCase columns

Revision ID: 277f3c4df95d
Revises: fa2f83508605
Create Date: 2025-07-10 18:46:19.464433
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision: str = '277f3c4df95d'
down_revision: Union[str, Sequence[str], None] = 'fa2f83508605'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.execute("""
        UPDATE reports SET Rate = NULL WHERE Rate REGEXP '[^0-9\\.]';
    """)
    op.execute("""
        UPDATE reports SET Amount = NULL WHERE Amount REGEXP '[^0-9\\.]';
    """)

    with op.batch_alter_table('reports') as batch_op:
        try:
            batch_op.alter_column('Overall_Quantity', new_column_name='Overall_quantity',
                                  existing_type=mysql.INTEGER())
        except:
            pass
        try:
            batch_op.alter_column('Reported_Quantity', new_column_name='Reported_quantity',
                                  existing_type=mysql.INTEGER())
        except:
            pass

        batch_op.alter_column('Task_id', existing_type=mysql.INTEGER(), nullable=False)
        batch_op.alter_column('Task_name', existing_type=mysql.VARCHAR(length=255), nullable=False)
        batch_op.alter_column('Project_name', existing_type=mysql.VARCHAR(length=255), nullable=False)
        batch_op.alter_column('Reported_by_name', existing_type=mysql.VARCHAR(length=255), nullable=False)
        batch_op.alter_column('User_id', existing_type=mysql.INTEGER(), nullable=False)

        batch_op.alter_column('Rate', existing_type=mysql.VARCHAR(length=20),
                              type_=sa.String(length=255), nullable=True)
        batch_op.alter_column('Amount', existing_type=mysql.VARCHAR(length=20),
                              type_=sa.String(length=255), nullable=True)

        batch_op.alter_column('Status', existing_type=mysql.VARCHAR(length=255), nullable=False)
        batch_op.alter_column('Pending_quantity', existing_type=mysql.INTEGER(),
                              type_=sa.String(length=255), nullable=False)

    op.alter_column('user', 'user_name',
                    existing_type=mysql.VARCHAR(length=255),
                    nullable=False)


def downgrade() -> None:
    with op.batch_alter_table('reports') as batch_op:
        batch_op.alter_column('Overall_quantity', new_column_name='Overall_Quantity',
                              existing_type=mysql.INTEGER())
        batch_op.alter_column('Reported_quantity', new_column_name='Reported_Quantity',
                              existing_type=mysql.INTEGER())

        batch_op.alter_column('Pending_quantity', existing_type=sa.String(length=255),
                              type_=mysql.INTEGER(), nullable=True)
        batch_op.alter_column('Status', existing_type=mysql.VARCHAR(length=255), nullable=True)

        batch_op.alter_column('Amount', existing_type=sa.String(length=255),
                              type_=mysql.FLOAT(), nullable=True)
        batch_op.alter_column('Rate', existing_type=sa.String(length=255),
                              type_=mysql.FLOAT(), nullable=True)

        batch_op.alter_column('User_id', existing_type=mysql.INTEGER(), nullable=True)
        batch_op.alter_column('Reported_by_name', existing_type=mysql.VARCHAR(length=255), nullable=True)
        batch_op.alter_column('Project_name', existing_type=mysql.VARCHAR(length=255), nullable=True)
        batch_op.alter_column('Task_name', existing_type=mysql.VARCHAR(length=255), nullable=True)
        batch_op.alter_column('Task_id', existing_type=mysql.INTEGER(), nullable=True)

    op.alter_column('user', 'user_name',
                    existing_type=mysql.VARCHAR(length=255),
                    nullable=True)
