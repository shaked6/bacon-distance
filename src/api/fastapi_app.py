from fastapi import FastAPI

from src.api.error_handler import register_exception_handlers
from src.data_accessors.base_db_accessor import BaseDBAccessor


def create_app(db_accessor: BaseDBAccessor) -> FastAPI:
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/bacon-distance/{actor_name}")
    def bacon_distance(actor_name: str):
        return {
            "actor": actor_name,
            "distance": db_accessor.get_bacon_distance(actor_name)
        }

    return app
