import os

import uvicorn

from src.consts import DB_DIR, ACTORS_FILE
from src.data_accessors.json_db_accessor import JsonDBAccessor
from src.fastapi_app import create_app

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, DB_DIR, ACTORS_FILE)

db_accessor = JsonDBAccessor(DB_PATH)
app = create_app(db_accessor)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
