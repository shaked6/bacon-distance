class ActorNotFoundException(Exception):
    def __init__(self, actor_name: str):
        self.actor_name = actor_name
        message = f"Actor '{actor_name}' does not exist in the database."
        super().__init__(message)
