import uvicorn

from src.data_accessors.sql_db_accessor import SQLDBAccessor
from src.api.fastapi_app import create_app

db_accessor = SQLDBAccessor()  # todo init path outside?
app = create_app(db_accessor)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
