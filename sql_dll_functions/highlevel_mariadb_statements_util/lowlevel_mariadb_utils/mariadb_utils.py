import logging
import mysql.connector
from mysql.connector.abstracts import MySQLConnectionAbstract
import time

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Log to console
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

# Also log to a file
file_handler = logging.FileHandler("./logs/mariadb-utils.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class MariaDbUtils:
    def connect_to_mysql(self, config, attempts=3, delay=2):
        """
        Try to connect to our MariaDb, include retry logic and with a delay between retries

        :param config: DB configuration parameters
        :param attempts: number of
        :param delay: time delay to wait between attempts
        :return: None if failed. else the valid connection object
        """
        attempt = 1
        # Implement a reconnection routine
        while attempt < attempts + 1:
            try:
                return mysql.connector.connect(**config)
            except (mysql.connector.Error, IOError) as err:
                if (attempts is attempt):
                    # Attempts to reconnect failed; returning None
                    logger.info("Failed to connect, exiting without a connection: %s", err)
                    return None
                logger.info(
                "Connection failed: %s. Retrying (%d/%d)...",
                err,
                attempt,
                attempts-1,
                )
                # progressive reconnect delay
                time.sleep(delay ** attempt)
                attempt += 1
        return None

    def does_table_exist_already(self, cursor: MySQLConnectionAbstract, tableName: str) -> bool | None:
        """
        Before we execute a create table command, check that the table does not exist.
        Before we execute a regular command, check that the table exists

        :param cursor: valid cursor to be able to execute this check table exists statement
        :param tableName: table name for which to check prior existence
        :return: None if failed. else True,False
        """
        if cursor is None or tableName is None:
            return None
        else:
            try:
                show_tables_like = "SHOW TABLES LIKE '{tableName}'".format(tableName=tableName)
                cursor.execute(show_tables_like)
                does_exist_table = cursor.rowcount
                return does_exist_table > 0
            except (mysql.connector.Error, IOError) as err:
                logger.info(
                "Connection failed: %s. ...",
                err,
                )
                return None
