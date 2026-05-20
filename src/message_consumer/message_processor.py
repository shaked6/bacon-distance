import json

from src.bacon_distance_service import BaconDistanceService
from src.data_accessors.base_db_accessor import BaseDBAccessor
from src.data_accessors.db_writer import DBWriter
from src.data_structures.actor import Actor


class MessageProcessor:
    def __init__(self, rabbit_host: str,
                 db_accessor: BaseDBAccessor,
                 db_writer: DBWriter,
                 bacon_service: BaconDistanceService):
        self.rabbit_host = rabbit_host
        self.db_accessor = db_accessor
        self.db_writer = db_writer
        self.bacon_service = bacon_service

    def start(self):
        while True:
            try:
                def connect_with_retry(host):
                    import time
                    import pika

                    while True:
                        try:
                            print(f"[worker] Trying to connect to RabbitMQ at {host}...")
                            return pika.BlockingConnection(
                                pika.ConnectionParameters(host=host)
                            )
                        except Exception as e:
                            print(f"[worker] RabbitMQ not ready ({e}), retrying in 2s")
                            time.sleep(2)

                connection = connect_with_retry(self.rabbit_host)
                channel = connection.channel()

                channel.queue_declare(queue="new_movies", durable=True)

                print("[worker] Listening for new movies...")

                channel.basic_consume(
                    queue="new_movies",
                    on_message_callback=self.process_message
                )

                channel.start_consuming()

            except Exception as e:
                print(f"[worker] Fatal error in consumer loop: {e}. Restarting...")
                continue

    def process_message(self, ch, method, properties, body):
        try:
            data = json.loads(body)
        except Exception as e:
            print(f"[worker] Failed to decode message: {body} ({e})")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        movie_name = data["Name"]
        actors = data["Actors"]

        print(f"[worker] Received movie: {movie_name} with actors {actors}")

        for actor_name in actors:
            self.db_writer.upsert_actor(Actor(actor_name))
            self.db_writer.upsert_actor_movie(actor_name, movie_name)

        self.bacon_service.recompute()

        print(f"[worker] Updated DB and Bacon distances for '{movie_name}'")

        ch.basic_ack(delivery_tag=method.delivery_tag)
