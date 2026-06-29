try:
    from .database import Base, engine
    import app.models  # noqa: F401
except ImportError:
    from database import Base, engine
    import models  # noqa: F401


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database tables created successfully.")
