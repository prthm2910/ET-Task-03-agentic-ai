import inspect
from langgraph.store.postgres import PostgresStore

print(f"PostgresStore init signature: {inspect.signature(PostgresStore.__init__)}")

# Try to initialize with a dummy pool
try:
    store = PostgresStore(None, index={"embed": "foo", "dims": 123})
except Exception as e:
    print(f"Error with flat index: {e}")

try:
    store = PostgresStore(None, index={"": {"embed": "foo", "dims": 123}})
except Exception as e:
    print(f"Error with nested index: {e}")
