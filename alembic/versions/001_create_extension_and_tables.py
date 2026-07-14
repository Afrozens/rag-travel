"""Create vector extension and initial tables

Revision ID: 001
Revises:
Create Date: 2026-07-13

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pgvector.sqlalchemy
from sqlalchemy.dialects.postgresql import UUID, JSON

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "trips",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("destination", sa.String(), nullable=False),
        sa.Column("agency", sa.String(), nullable=False),
        sa.Column("start_date", sa.String(), nullable=False),
        sa.Column("end_date", sa.String(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("currency", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("category", sa.String(), nullable=False),
        sa.Column("tags", JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "trip_embeddings",
        sa.Column("id", UUID(as_uuid=True), nullable=False),
        sa.Column("trip_id", sa.String(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("embedding", pgvector.sqlalchemy.Vector(2048), nullable=True),
        sa.Column("metadata", JSON(), nullable=True),  # column name is "metadata" in DB
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index("idx_trip_embeddings_hnsw", "trip_embeddings", ["embedding"], postgresql_using="hnsw", postgresql_with={"m": "16", "ef_construction": "200"}, postgresql_ops={"embedding": "vector_cosine_ops"})
    op.create_index("idx_trip_embeddings_trip_id", "trip_embeddings", ["trip_id"])

    op.create_table(
        "purchases",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("trip_id", sa.String(), nullable=False),
        sa.Column("trip_title", sa.String(), nullable=False),
        sa.Column("purchased_at", sa.String(), nullable=False),
        sa.Column("destination", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("purchases")
    op.drop_table("trip_embeddings")
    op.drop_table("trips")
    op.execute("DROP EXTENSION IF EXISTS vector")
