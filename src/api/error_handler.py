from fastapi import HTTPException, status
from fastapi import Request

from src.exceptions.actor_not_found_exception import ActorNotFoundException


def register_exception_handlers(app):
    @app.exception_handler(ActorNotFoundException)
    async def actor_not_found_handler(request: Request, error: ActorNotFoundException):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )
