import uvicorn

from src.data_accessors.json_db_accessor import JsonDBAccessor
from src.fastapi_app import create_app

DB_PATH = "db/actors.json"

db_accessor = JsonDBAccessor(DB_PATH)
app = create_app(db_accessor)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
