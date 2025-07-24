import os
from utils.logger_utility import logger

try:
    import psycopg2
    from psycopg2 import sql as pg_sql, OperationalError as PgOperationalError
except ImportError:
    psycopg2 = None
    PgOperationalError = Exception

try:
    import ibm_db
    import ibm_db_dbi
except ImportError:
    ibm_db = None
    ibm_db_dbi = None

class DatabaseUtility:
    """
    Utility class for database interactions (PostgreSQL and IBM DB2) with logging.
    """

    def __init__(self, connection_string, db_type="postgres"):
        """
        Initialize DatabaseUtility with a connection string and database type.
        Args:
            connection_string (str): Database connection string.
            db_type (str): Type of database ('postgres' or 'db2').
        """
        self.connection_string = connection_string
        self.db_type = db_type.lower()
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        Establish a connection to the database.
        """
        try:
            logger.info(f"Connecting to the {self.db_type} database.")
            if self.db_type == "postgres":
                if not psycopg2:
                    raise ImportError("psycopg2 is not installed.")
                self.connection = psycopg2.connect(self.connection_string)
                self.cursor = self.connection.cursor()
            elif self.db_type == "db2":
                if not ibm_db or not ibm_db_dbi:
                    raise ImportError("ibm_db and ibm_db_dbi are not installed.")
                self.connection = ibm_db_dbi.connect(self.connection_string, "", "")
                self.cursor = self.connection.cursor()
            else:
                raise ValueError("Unsupported database type. Use 'postgres' or 'db2'.")
            logger.info("Database connection established.")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise

    def disconnect(self):
        """
        Close the database connection.
        """
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            logger.info("Database connection closed.")
        except Exception as e:
            logger.error(f"Error closing database connection: {e}")

    def execute_query(self, query, params=None):
        """
        Execute a SQL query (SELECT).
        Args:
            query (str): SQL query to execute.
            params (tuple, optional): Parameters for the query.
        Returns:
            list: Query results.
        """
        try:
            logger.info(f"Executing query: {query} | Params: {params}")
            if self.db_type == "postgres":
                self.cursor.execute(query, params)
                results = self.cursor.fetchall()
            elif self.db_type == "db2":
                self.cursor.execute(query, params or ())
                results = self.cursor.fetchall()
            else:
                raise ValueError("Unsupported database type.")
            logger.info(f"Query executed successfully. Rows fetched: {len(results)}")
            return results
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise

    def execute_update(self, query, params=None):
        """
        Execute an update/insert/delete SQL statement.
        Args:
            query (str): SQL statement to execute.
            params (tuple, optional): Parameters for the statement.
        Returns:
            int: Number of rows affected.
        """
        try:
            logger.info(f"Executing update: {query} | Params: {params}")
            if self.db_type == "postgres":
                self.cursor.execute(query, params)
                self.connection.commit()
                rowcount = self.cursor.rowcount
            elif self.db_type == "db2":
                self.cursor.execute(query, params or ())
                self.connection.commit()
                rowcount = self.cursor.rowcount
            else:
                raise ValueError("Unsupported database type.")
            logger.info(f"Update executed successfully. Rows affected: {rowcount}")
            return rowcount
        except Exception as e:
            logger.error(f"Update execution failed: {e}")
            if self.connection:
                self.connection.rollback()
            raise

    def fetch_one(self):
        """
        Fetch the next row of a query result set.
        Returns:
            tuple: The next row or None if no more data is available.
        """
        try:
            row = self.cursor.fetchone()
            logger.info(f"Fetched one row: {row}")
            return row
        except Exception as e:
            logger.error(f"Fetch one failed: {e}")
            raise

    def fetch_all(self):
        """
        Fetch all (remaining) rows of a query result set.
        Returns:
            list: All rows.
        """
        try:
            rows = self.cursor.fetchall()
            logger.info(f"Fetched all rows: {rows}")
            return rows
        except Exception as e:
            logger.error(f"Fetch all failed: {e}")
            raise

    def __enter__(self):
        """
        Context manager entry. Connect to the database.
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit. Disconnect from the database.
        """
        self.disconnect()