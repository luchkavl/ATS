"""Create all

Revision ID: 789894c92df0
Revises: 
Create Date: 2022-11-25 17:16:57.479613

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from ats import enums

# revision identifiers, used by Alembic.
revision = '789894c92df0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('candidates',
                    sa.Column('candidate_id', UUID(as_uuid=True), unique=True, primary_key=True),
                    sa.Column('first_name', sa.String(), nullable=False),
                    sa.Column('last_name', sa.String(), nullable=False),
                    sa.Column('email', sa.String(), unique=True),
                    sa.Column('status', sa.Enum(enums.Statuses))
                    )

    op.create_table('jobs',
                    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
                    sa.Column('name', sa.Enum(enums.Vacancies), unique=True, primary_key=True)
                    )

    op.create_table('candidate_feedbacks',
                    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
                    sa.Column('candidate_id', UUID(as_uuid=True), sa.ForeignKey('candidates.candidate_id')),
                    sa.Column('vacancy', sa.Enum(enums.Vacancies), sa.ForeignKey('jobs.name')),
                    sa.Column('stage', sa.Enum(enums.InterviewStages)),
                    sa.Column('feedback_text', sa.Text(), nullable=False)
                    )

    op.create_table('candidate_vacancies',
                    sa.Column('candidate_id', UUID(as_uuid=True), sa.ForeignKey('candidates.candidate_id'), primary_key=True),
                    sa.Column('vacancy', sa.Enum(enums.Vacancies), sa.ForeignKey('jobs.name'), primary_key=True)
                    )

    op.create_table('users',
                    sa.Column('username', sa.String(), unique=True, primary_key=True),
                    sa.Column('full_name', sa.String(), nullable=False),
                    sa.Column('email', sa.String(), unique=True),
                    sa.Column('hashed_password', sa.String, nullable=False),
                    sa.Column('admin', sa.Boolean, nullable=False)
                    )


def downgrade() -> None:
    op.drop_table('candidate_feedbacks')
    op.drop_table('candidate_vacancies')
    op.drop_table('candidates')
    op.drop_table('jobs')
    op.drop_table('users')
