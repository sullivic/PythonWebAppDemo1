import logging
from mysql.connector.abstracts import MySQLConnectionAbstract
import mysql.connector
from contextlib import closing
from collections import OrderedDict

from .lowlevel_mariadb_utils import MariaDbUtils

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Log to console
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

# Also log to a file
file_handler = logging.FileHandler("./logs/app-level-db-utils.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class MariaDbStatementsUtil:

    def __init__(self):
        mariaDbUtils = MariaDbUtils()
        self.mariaDbUtils = mariaDbUtils

    def create_table_with_name(self, cursor: MySQLConnectionAbstract, tableName: str, createTableSqls: list) -> bool:
        """
        execute CREATE TABLE if does not exist already

        :param cursor: valid cursor with which to execute db statement
        :param tableName: table-name to check prior existence
        :param createTableSqls: CREATE TABLE statement
        :return: bool True successful, False operation failed
        """
        exists_state = self.mariaDbUtils.does_table_exist_already(cursor, tableName)
        if exists_state is None or exists_state is True:
            return False
        else:
            try:
                my_return_value = True
                for createTableSql in createTableSqls:
                    cursor.execute(createTableSql)
                    if (cursor.rowcount != 0):
                        my_return_value = False
                        logging.debug("cursor.rowcount=[%d] for statement=[%s]" % (cursor.rowcount,createTableSql,))
                return my_return_value
            except (mysql.connector.Error, IOError) as err:
                logger.info(
                "Connection failed: %s. ...",
                err,
                )
                return False

    def drop_table_with_name(self, cursor: MySQLConnectionAbstract, tableName: str, dropTableSqls: list) -> bool:
        """
        execute DROP TABLE if does exist already

        :param cursor: valid cursor with which to execute db statement
        :param tableName: table-name to check prior existence
        :param dropTableSqls: DROP TABLE statement
        :return: bool True successful, False operation failed
        """
        exists_state = self.mariaDbUtils.does_table_exist_already(cursor, tableName)
        if exists_state is None or exists_state is False:
            return False
        else:
            try:
                my_return_value = True
                for dropTableSql in dropTableSqls:
                    cursor.execute(dropTableSql)
                    if (cursor.rowcount != 0):
                        my_return_value = False
                        logging.debug("cursor.rowcount=[%d] for statement=[%s]" % (cursor.rowcount,dropTableSql,))
                return my_return_value
            except (mysql.connector.Error, IOError) as err:
                logger.info(
                "Connection failed: %s. ...",
                err,
                )
                return False


    def insert_into_table_with_name(self, cursor: MySQLConnectionAbstract, tableName: str, insertIntoTableSqls: list) -> bool:
        """
        execute INSERT INTO TABLE if does exist already

        :param cursor: valid cursor with which to execute db statements
        :param tableName: table-name to check prior existence
        :param insertIntoTableSqls: INSERT INTO TABLE statements
        :return: bool True successful, False operation failed
        """
        exists_state = self.mariaDbUtils.does_table_exist_already(cursor, tableName)
        if exists_state is None or exists_state is False:
            return False
        else:
            try:
                my_return_value = True
                for insertIntoTableSql in insertIntoTableSqls:
                    cursor.execute(insertIntoTableSql)
                    if (cursor.rowcount != 1):
                        my_return_value = False
                        logging.debug("cursor.rowcount=[%d] for statement=[%s]" % (cursor.rowcount,insertIntoTableSql,))
                return my_return_value
            except (mysql.connector.Error, IOError) as err:
                logger.info(
                "Connection failed: %s. ...",
                err,
                )
                return False

    def add_constraint_table_with_name(self, cursor: MySQLConnectionAbstract, tableName: str, addConstraintTableSqls: list) -> bool:
        """
        execute ALTER TABLE ADD CONSTRAINT FOREIGN KEY if does exist already

        :param cursor: valid cursor with which to execute db statements
        :param tableName: table-name to check prior existence
        :param addConstraintTableSqls: ALTER TABLE ADD CONSTRAINT FOREIGN KEY statements
        :return: bool True successful, False operation failed
        """
        exists_state = self.mariaDbUtils.does_table_exist_already(cursor, tableName)
        if exists_state is None or exists_state is False:
            return False
        else:
            try:
                for addConstraintTableSql in addConstraintTableSqls:
                    cursor.execute(addConstraintTableSql)
                return True
            except (mysql.connector.Error, IOError) as err:
                logger.info(
                "Connection failed: %s. ...",
                err,
                )
                return False

    def select_from_table_with_name(self, cursor: MySQLConnectionAbstract, tableName: str, selectFromTableSqls: list) -> list:
        """
        courtesy SELECT ALL function. to prove that the MariaDb tables have data in them.

        :param cursor: valid cursor with which to execute db statement
        :param tableName: table-name to check prior existence
        :param selectFromTableSqls: SELECT FROM TABLE statement
        :return: always returns a list of strings. empty list if the operation failed or no data found.
        """
        my_return_data = []
        exists_state = self.mariaDbUtils.does_table_exist_already(cursor, tableName)
        if exists_state is None or exists_state is False:
            return my_return_data
        else:
            try:
                for selectFromTableSql in selectFromTableSqls:
                    cursor.execute(selectFromTableSql)
                    rows = cursor.fetchall()
                    for row in rows:
                        if tableName == "category":
                            my_return_data.append("CATEGORY_ROW.category_id=[{}], ROW.categoryName=[{}]".format(row[0],row[1],))
                            logging.debug("CATEGORY_ROW.category_id=%s, ROW.categoryName=%s" % (row[0], row[1],))
                        elif tableName == "brand":
                            my_return_data.append("BRAND_ROW.brand_id=[{}], ROW.brandName=[{}]".format(row[0],row[1],))
                            logging.debug("BRAND_ROW.brand_id=%s, ROW.brandName=%s" % (row[0], row[1],))
                        elif tableName == "product":
                            my_return_data.append("PRODUCT_ROW.product_id=[{}], ROW.sku=[{}], ROW.productName=[{}], ROW.productDesc=[{}], ROW.categoryId=[{}], ROW.brandId=[{}]".format(row[0],row[1],row[2],row[3],row[4],row[5],))
                            logging.debug("PRODUCT_ROW.product_id=%s, ROW.sku=%s, ROW.productName=%s, ROW.productDesc=%s, ROW.categoryId=%s, ROW.brandId=%s" % (row[0], row[1], row[2], row[3], row[4], row[5],))
                return my_return_data
            except (mysql.connector.Error, IOError) as err:
                logger.info(
                "Connection failed: %s. ...",
                err,
                )
                return my_return_data


    def select_ingest_into_chroma(self, cursor: MySQLConnectionAbstract, tableName: str, selectFromTableSqls: list) -> list:
        """
        SELECT ALL from PRODUCT TABLE (MariaDb) convert to embeddings and store all into ChromaDb-collection.
        this function retrieves from MariaDb PRODUCT table - and returns as a list for the next process to ingest into chroma.

        :param cursor: valid cursor with which to execute db statement
        :param tableName: table-name to check prior existence
        :param selectFromTableSqls: SELECT FROM TABLE statement
        :return: always returns a list of objects(PK, productName, productDescription). empty list if the operation failed or no data found.
        """
        my_return_data = []
        exists_state = self.mariaDbUtils.does_table_exist_already(cursor, tableName)
        if exists_state is None or exists_state is False:
            return my_return_data
        else:
            try:
                for selectFromTableSql in selectFromTableSqls:
                    cursor.execute(selectFromTableSql)
                    rows = cursor.fetchall()
                    for row in rows:
                        my_return_data.append({"pk":"{}".format(row[0],),"sentenceData":"{} {}".format(row[1],row[2],)})
                return my_return_data
            except (mysql.connector.Error, IOError) as err:
                logger.info(
                "Connection failed: %s. ...",
                err,
                )
                return my_return_data

    #   chroma_results_retrieve_from_mariadb
    def chroma_results_retrieve_from_mariadb(self, cursor: MySQLConnectionAbstract, tableName: str, selectFromTableSqls: list, id_ids: list) -> list:
        """
        ChromaDb has returned a list of id(PK) corresponding to the results that most closely match the searchTerm.
        So use this list of PKs to retrieve the data from MariaDb for display.

        :param cursor: valid cursor with which to execute db statement
        :param tableName: table-name to check prior existence
        :param selectFromTableSqls: SELECT FROM TABLE WHERE ID IN (list<ids>) statement
        :param id_ids: list of PKs that chromaDb matched that we now need to retrieve.
        :return: always returns a list of objects(data of our item as object,map). empty list if the operation failed or no data found.
        """
        my_return_data = []
        exists_state = self.mariaDbUtils.does_table_exist_already(cursor, tableName)
        if exists_state is None or exists_state is False:
            return my_return_data
        else:
            try:

                for selectFromTableSql in selectFromTableSqls:
                    placeholders = ", ".join(["%s"] * len(id_ids))
                    logging.debug("placeholders_before=[%s]" % (placeholders,))
                    logging.debug("sql_before_selectFromTableSql=[%s]" % (selectFromTableSql,))
                    sql = selectFromTableSql % (placeholders,)
                    logging.debug("sql=[%s]" % (sql,))
                    logging.debug("id_ids=[%r]" % (id_ids,))
                    cursor.execute(sql, id_ids)
                    rows = cursor.fetchall()
                    for row in rows:
                        my_return_data.append({"productId":"{}".format(row[0],),"sku":"{}".format(row[1],),"productName":"{}".format(row[2]),"productDescription":"{}".format(row[3]),"brandName":"{}".format(row[4]),"categoryName":"{}".format(row[5],)})
                return my_return_data

            except (mysql.connector.Error, IOError) as err:
                logger.info(
                "Connection failed: %s. ...",
                err,
                )
                return my_return_data



    #CREATING,INSERTING,FOREIGNKEYING,SELECTING,DROPPING
    def connect_db_execute_all_sql_statements(self, my_db_config, sql_map_dict: OrderedDict, sql_exec_function_name: str, mode: str, id_ids: list) -> bool | list:
        """
        The above functions on this class are called with parameters via an eval() command.
        Note: all except CHROMA_RESULT have the same method signature in terms of parameters and return value

        :param my_db_config: Configuration parameters for us to connect to MariaDb.
        :param sql_map_dict: OrderedDict of TableName and a list of SqlToExecute on this TableName
        :param sql_exec_function_name: python functionName (need 'self.' prefix)
        :param mode: since CHROMA_RESULT has a different method signature, check and call correct one.
        :param id_ids: Chroma db matched list of ids for the searchTerm.
        :return: bool or list depending upon which function we called.
        """


        logging.info("START sql_exec_function_name=[%s]" % (sql_exec_function_name, ))

        status = False
        with closing(self.mariaDbUtils.connect_to_mysql(my_db_config, attempts=3)) as cnx:
            with closing(cnx.cursor(buffered=True)) as cursor:
                for tableName, tableSql in sql_map_dict.items():  # ord_dict_create_1.items():  # TABLES_CREATE_MAP.items():

                    if mode is None or mode != "CHROMA_RESULTS_AND_RETRIEVE" or id_ids is None:
                        status = eval(sql_exec_function_name)(cursor, tableName, tableSql)
                    else:
                        status = eval(sql_exec_function_name)(cursor, tableName, tableSql, id_ids)
            cnx.commit()

        return status
