import json
import os


def validate_actors_db_exists(db_path: str):
    if not os.path.exists(db_path):
        print("Actors DB not found, init it first")
        raise Exception
    else:
        print("Actors DB found. Continuing...")


def load_db(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_bacon_distance(db: dict, actor_name: str) -> str:
    normalized_actor_name = actor_name.strip().lower()

    for name in db.keys():
        if name.lower() == normalized_actor_name:
            distance = db[name].get("bacon_distance", -1)
            return "infinity" if distance == -1 else str(distance)

    raise ValueError(f"Actor '{actor_name}' does not exist in the database.")


def app_loop(db_path: str):
    actors_db = load_db(db_path)

    print("Type an actor name to get their Bacon distance.")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("> ").strip()
        if user_input.lower() == "exit":
            break
        if not user_input:
            continue

        try:
            result = get_bacon_distance(actors_db, user_input)
            print(f"Bacon distance for '{user_input}': {result}")
        except ValueError as e:
            print(e)


if __name__ == "__main__":
    file_db = "data/actors.json"
    validate_actors_db_exists(file_db)
    app_loop(file_db)

    # THIS FILE BECOMES UNUSED AFTER MILESTONE 1