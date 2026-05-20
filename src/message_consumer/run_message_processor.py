import os

from src.bacon_distance_service import BaconDistanceService
from src.data_accessors.db_writer import DBWriter
from src.data_accessors.sql_db_accessor import SQLDBAccessor
from src.message_consumer.message_processor import MessageProcessor


def main():
    db_writer = DBWriter()
    db_accessor = SQLDBAccessor()
    bacon_service = BaconDistanceService(
        data_accessor=db_accessor,
        data_writer=db_writer
    )

    rabbit_host = os.getenv("RABBITMQ_HOST", "localhost")

    message_processor = MessageProcessor(
        db_writer=db_writer,
        db_accessor=db_accessor,
        bacon_service=bacon_service,
        rabbit_host=rabbit_host
    )

    message_processor.start()


if __name__ == "__main__":
    main()
