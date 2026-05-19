# bacon-distance
An api describing the distance of actors from Kevin Bacon

# Choosing SQLite as the db
SQLite, as its name implies, is a lightweight relational database.
The actor data in this project fits naturally into a relational model, which makes the usual SQL options relevant:
SQLite, PostgreSQL, and MySQL.
Since the service doesn’t need to handle hundreds of concurrent connections, and most operations are read heavy with updates performed in controlled bulk operations, 
SQLite provides the right balance of simplicity, performance, and reliability for this project.
It gives me all the relational structure I need without the operational overhead of running a full database server.