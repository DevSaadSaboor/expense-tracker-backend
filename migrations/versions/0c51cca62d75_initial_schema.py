"""initial schema

Revision ID: 0c51cca62d75
Revises: 
Create Date: 2026-02-02 14:50:34.243287

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c51cca62d75'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE categories (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (user_id, name),
        CONSTRAINT fk_categories_user
            FOREIGN KEY (user_id)
            REFERENCES users(id)
            ON DELETE CASCADE
    );

    CREATE TABLE expenses (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        category_id INTEGER,
        amount NUMERIC(10,2) NOT NULL,
        note TEXT,
        spend_at DATE NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT fk_expenses_user
            FOREIGN KEY (user_id)
            REFERENCES users(id)
            ON DELETE RESTRICT,
        CONSTRAINT fk_expenses_category
            FOREIGN KEY (category_id)
            REFERENCES categories(id)
            ON DELETE SET NULL
    );

    CREATE TABLE refresh_tokens (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        token TEXT NOT NULL,
        expires_at TIMESTAMP NOT NULL,
        revoked BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT fk_refresh_user
            FOREIGN KEY (user_id)
            REFERENCES users(id)
            ON DELETE CASCADE
    );
    """)

def downgrade():
    op.execute("""
    DROP TABLE IF EXISTS refresh_tokens;
    DROP TABLE IF EXISTS expenses;
    DROP TABLE IF EXISTS categories;
    DROP TABLE IF EXISTS users;
    """)
