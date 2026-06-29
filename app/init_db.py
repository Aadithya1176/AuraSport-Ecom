try:
    from .database import Base, engine
    import app.models  # noqa: F401
except ImportError:
    from database import Base, engine
    import models  # noqa: F401

from sqlalchemy import inspect, text


def ensure_cart_schema() -> None:
    inspector = inspect(engine)

    if not inspector.has_table("cart"):
        return

    existing_columns = {column["name"] for column in inspector.get_columns("cart")}
    statements: list[str] = []

    if "user_id" not in existing_columns:
        statements.append("ALTER TABLE cart ADD COLUMN user_id INTEGER")
    if "product_id" not in existing_columns:
        statements.append("ALTER TABLE cart ADD COLUMN product_id INTEGER")
    if "qty" not in existing_columns:
        statements.append("ALTER TABLE cart ADD COLUMN qty INTEGER")

    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))

        connection.execute(
            text(
                """
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1
                        FROM information_schema.table_constraints
                        WHERE constraint_name = 'cart_user_id_fkey'
                          AND table_name = 'cart'
                    ) THEN
                        ALTER TABLE cart
                        ADD CONSTRAINT cart_user_id_fkey
                        FOREIGN KEY (user_id) REFERENCES users (id);
                    END IF;
                END $$;
                """
            )
        )
        connection.execute(
            text(
                """
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1
                        FROM information_schema.table_constraints
                        WHERE constraint_name = 'cart_product_id_fkey'
                          AND table_name = 'cart'
                    ) THEN
                        ALTER TABLE cart
                        ADD CONSTRAINT cart_product_id_fkey
                        FOREIGN KEY (product_id) REFERENCES products (id);
                    END IF;
                END $$;
                """
            )
        )


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    ensure_cart_schema()


if __name__ == "__main__":
    init_db()
    print("Database tables created successfully.")
