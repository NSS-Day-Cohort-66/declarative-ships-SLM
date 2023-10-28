import sqlite3


def db_get_single(sql, pk) -> sqlite3.Row:
    """Retrieve a single row from a database table

    Args:
        sql (string): SQL string
        pk (int): Primary of item to retrieve

    Returns:
        sqlite3.Row: The row object representing the retrieved row
    """
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(sql, (pk,))
        return db_cursor.fetchone()


def db_get_all(sql, param=None) -> list:
    """Retrieve rows from a database table with optional parameters.

    Args:
        sql (string): SQL string
        params (tuple, optional): A tuple of parameters to be passed to the SQL query.

    Returns:
        list: List of dictionaries representing the query results.
    """
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        if param:
            db_cursor.execute(sql, (param,))
        else:
            db_cursor.execute(sql)

        results = db_cursor.fetchall()

        # Convert the results to a list of dictionaries
        result_dicts = [dict(row) for row in results]
        return result_dicts

def db_delete(sql, pk) -> int:
    """Delete a row from the database

    Args:
        sql (string): SQL string
        pk (int): Primary key of item to delete

    Returns:
        int: Number of rows deleted
    """
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(sql, (pk,))
        return db_cursor.rowcount


def db_update(sql, data_tuple) -> int:
    """Update a row in a database table

    Args:
        sql (string): SQL string
        data_tuple (tuple): Tuple containing all data values to be mapped to parameters in the SQL string

    Returns:
        int: Number of rows updated
    """
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(sql, data_tuple)
        return db_cursor.rowcount

def db_create(sql, data_tuple) -> int:
    """Create a row in a database table

    Args:
        sql (string): SQL string
        data_tuple (tuple): Tuple containing all data values to be mapped to parameters in the SQL string

    Returns:
        int: The new id of the created row
    """
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(sql, data_tuple)
        return db_cursor.lastrowid
