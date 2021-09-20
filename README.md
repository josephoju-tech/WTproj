 Web App
--------
An online store web application project.

dbschema.py
-----------
This provides the schema for the database. The codes creates the database.
The database is populated with sample data from 'apparel.csv' file.

With Bottle sqlite plugin, @route handlers will take the first 'db' argument
that will be the valid database connection. All functions will access the database
by taking a database connection to be an argument.

The configuration of the database connection is set up to return Row objects.
The field name is the key used for accessing the Row objects, just like dictionaries.

model.py
--------

This will provide the interface for the database, using 'product_get' and 'product_list'
functions to get the 'products' table data.

session.py
----------
This will provide the interface to session data.

main.py
-------

This is the core web application module, provides the various route handlers for the app.


**COOKIES** Requests to the pages in the app would result in creating a new session on first visit.
This means, all requests will have a valid session in the database. This session can either
be newly created or an identified session from the cookie; achieved by 'session.get_or_create_session(db)'.
