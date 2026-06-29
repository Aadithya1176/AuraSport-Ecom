try:
    from .database import engine
except ImportError:
    from database import engine

try:
    connection = engine.connect()
    print("Connected Successfully")
    connection.close()

except Exception as e:
    print(e)
