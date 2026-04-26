import logging

from .file_utils.read_file_utils import FileUtils
from .dtd_validator.xml_dtd_validator import DtdXmlValidator#validate_xml_with_dtd
from .dictionary_util.ordered_dict_util import PutXmlDataIntoOrderedDictionary#xml_to_ordered_dict
from .highlevel_mariadb_statements_util.mariadb_statements_util import MariaDbStatementsUtil#connect_db_execute_all_sql_statements

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Log to console
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

# Also log to a file
file_handler = logging.FileHandler("./logs/mariadb-operations.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


config = {
"host": "127.0.0.1",
"user": "learnpy",
"password": "mySQL12!\"",
"database": "learnpython1",
'autocommit': False,
}

class XmlAndDatabaseOperations:
    def __init__(self):
        dtdXmlValidator = DtdXmlValidator()
        fileUtils = FileUtils()
        putXmlDataIntoOrderedDictionary = PutXmlDataIntoOrderedDictionary()
        mariaDbStatementsUtil = MariaDbStatementsUtil()
        self.dtdXmlValidator = dtdXmlValidator
        self.fileUtils = fileUtils
        self.putXmlDataIntoOrderedDictionary = putXmlDataIntoOrderedDictionary
        self.mariaDbStatementsUtil = mariaDbStatementsUtil
        self.fileSystemPrefix = "./sql-scripts"
        dtd_content = self.fileUtils.read_file_as_string(self.fileSystemPrefix + "/xmlSqlMapDtd.dtd")
        self.dtd_content = dtd_content

    def read_create_and_validate_with_dtd(self) -> bool:
        """
        FileSystem - read DTD file and CREATE TABLE file and validate the XML file is well-formed;
        then put results into an OrderedDictionary;
        then execute the SQL on MariaDb.

        :return: True,False for overall success of the operation. None if severe error occurred.
        """
#        dtd_content = self.fileUtils.read_file_as_string(self.fileSystemPrefix + "/xmlSqlMapDtd.dtd")
        xml_create = self.fileUtils.read_file_as_string(self.fileSystemPrefix + "/sqlMap-createTables.xml")
        ret_create_validated_ok = self.dtdXmlValidator.validate_xml_with_dtd(xml_create, self.dtd_content)
        if ret_create_validated_ok is None or ret_create_validated_ok is False:
            return False # meaning validation of input data failed
        ord_dict_create_1 = self.putXmlDataIntoOrderedDictionary.xml_to_ordered_dict(xml_create)
        logging.info("len=%d.\n", len(ord_dict_create_1))
        successful_state = self.mariaDbStatementsUtil.connect_db_execute_all_sql_statements(config, ord_dict_create_1, "self.create_table_with_name", "CREATING", None)
        logging.info("CREATED - %r" % ((successful_state is not None and successful_state is not False),))
        return successful_state


    def read_drop_and_validate_with_dtd(self) -> bool:
        """
        FileSystem - read DTD file and DROP TABLE file and validate the XML file is well-formed;
        then put results into an OrderedDictionary;
        then execute the SQL on MariaDb.

        :return: True,False for overall success of the operation. None if severe error occurred.
        """
#        dtd_content = self.fileUtils.read_file_as_string(self.fileSystemPrefix + "/xmlSqlMapDtd.dtd")
        xml_drop = self.fileUtils.read_file_as_string(self.fileSystemPrefix + "/sqlMap-dropTables.xml")
        ret_drop_validated_ok = self.dtdXmlValidator.validate_xml_with_dtd(xml_drop, self.dtd_content)
        if ret_drop_validated_ok is None or ret_drop_validated_ok is False:
            return False # meaning validation of input data failed
        ord_dict_drop_1 = self.putXmlDataIntoOrderedDictionary.xml_to_ordered_dict(xml_drop)
        logging.info("len=%d.\n", len(ord_dict_drop_1))
        successful_state = self.mariaDbStatementsUtil.connect_db_execute_all_sql_statements(config, ord_dict_drop_1, "self.drop_table_with_name","DROPPING", None)
        logging.info("DROPPED - %r" % ((successful_state is not None and successful_state is not False),))
        return successful_state


    def read_insert_and_validate_with_dtd(self) -> bool:
        """
        FileSystem - read DTD file and INSERT INTO TABLE file and validate the XML file is well-formed;
        then put results into an OrderedDictionary;
        then execute the SQL on MariaDb.

        :return: True,False for overall success of the operation. None if severe error occurred.
        """
#        dtd_content = self.fileUtils.read_file_as_string(self.fileSystemPrefix + "/xmlSqlMapDtd.dtd")
        xml_insertInto = self.fileUtils.read_file_as_string(self.fileSystemPrefix + "/sqlMap-insertIntoTables.xml")
        ret_insertInto_validated_ok = self.dtdXmlValidator.validate_xml_with_dtd(xml_insertInto, self.dtd_content)
        if ret_insertInto_validated_ok is None or ret_insertInto_validated_ok is False:
            return False # meaning validation of input data failed
        ord_dict_insertInto_1 = self.putXmlDataIntoOrderedDictionary.xml_to_ordered_dict(xml_insertInto)
        logging.info("len=%d.\n", len(ord_dict_insertInto_1))
        successful_state = self.mariaDbStatementsUtil.connect_db_execute_all_sql_statements(config, ord_dict_insertInto_1, "self.insert_into_table_with_name","INSERTING", None)
        logging.info("INSERTED - %r" % ((successful_state is not None and successful_state is not False),))
        return successful_state


    def read_foreign_key_and_validate_with_dtd(self) -> bool:
        """
        FileSystem - read DTD file and ALTER TABLE ADD CONSTRAINT FOREIGN KEY file and validate the XML file is well-formed;
        then put results into an OrderedDictionary;
        then execute the SQL on MariaDb.

        :return: True,False for overall success of the operation. None if severe error occurred.
        """
#        dtd_content = self.fileUtils.read_file_as_string(self.fileSystemPrefix + "/xmlSqlMapDtd.dtd")
        xml_addForeignKeys = self.fileUtils.read_file_as_string(self.fileSystemPrefix + "/sqlMap-addForeignKeys.xml")
        ret_addForeignKey_validated_ok = self.dtdXmlValidator.validate_xml_with_dtd(xml_addForeignKeys, self.dtd_content)
        if ret_addForeignKey_validated_ok is None or ret_addForeignKey_validated_ok is False:
            return False # meaning validation of input data failed
        ord_dict_addForeignKey_1 = self.putXmlDataIntoOrderedDictionary.xml_to_ordered_dict(xml_addForeignKeys)
        logging.info("len=%d.\n", len(ord_dict_addForeignKey_1))
        successful_state = self.mariaDbStatementsUtil.connect_db_execute_all_sql_statements(config, ord_dict_addForeignKey_1, "self.add_constraint_table_with_name","FOREIGNKEYING", None)
        logging.info("CONSTRAINT ADDED - %r" % ((successful_state is not None and successful_state is not False),))
        return successful_state


    def read_select_and_validate_with_dtd(self) -> list:
        """
        FileSystem - read DTD file and SELECT ALL FROM TABLE file and validate the XML file is well-formed;
        then put results into an OrderedDictionary;
        then execute the SQL on MariaDb.

        :return: list<str> for overall success of the operation. None if severe error occurred.
        """
#        dtd_content = self.fileUtils.read_file_as_string(self.fileSystemPrefix + "/xmlSqlMapDtd.dtd")
        xml_selectFrom = self.fileUtils.read_file_as_string(self.fileSystemPrefix + "/sqlMap-selectFromTables.xml")
        ret_selectFrom_validated_ok = self.dtdXmlValidator.validate_xml_with_dtd(xml_selectFrom, self.dtd_content)
        if ret_selectFrom_validated_ok is None or ret_selectFrom_validated_ok is False:
            return [] # meaning validation of input data failed
        ord_dict_selectFrom_1 = self.putXmlDataIntoOrderedDictionary.xml_to_ordered_dict(xml_selectFrom)
        logging.info("len=%d.\n", len(ord_dict_selectFrom_1))
        returned_data_string = self.mariaDbStatementsUtil.connect_db_execute_all_sql_statements(config, ord_dict_selectFrom_1, "self.select_from_table_with_name","SELECTING", None)
        if returned_data_string is None or len(returned_data_string) == 0:
            logging.info("Null or empty list")
        else:
            logging.info("len(returned_data_string)=[%d]" % (len(returned_data_string),))
        return returned_data_string


    def read_ingest_to_chroma_with_dtd(self) -> list:
        """
        FileSystem - read DTD file and SELECT ALL FROM PRODUCT TABLE (and store in a format for chroma-db embedding to be calculated) file and validate the XML file is well-formed;
        then put results into an OrderedDictionary;
        then execute the SQL on MariaDb.

        :return: list<str> for overall success of the operation. None if severe error occurred.
        """
#        dtd_content = self.fileUtils.read_file_as_string(self.fileSystemPrefix + "/xmlSqlMapDtd.dtd")
        xml_selectFrom = self.fileUtils.read_file_as_string(self.fileSystemPrefix + "/sqlMap-selectProductForIngest-intoChromaDb.xml")
        ret_selectFrom_validated_ok = self.dtdXmlValidator.validate_xml_with_dtd(xml_selectFrom, self.dtd_content)
        if ret_selectFrom_validated_ok is None or ret_selectFrom_validated_ok is False:
            return [] # meaning validation of input data failed
        ord_dict_selectFrom_1 = self.putXmlDataIntoOrderedDictionary.xml_to_ordered_dict(xml_selectFrom)
        logging.info("len=%d.\n", len(ord_dict_selectFrom_1))
        returned_data_string = self.mariaDbStatementsUtil.connect_db_execute_all_sql_statements(config, ord_dict_selectFrom_1, "self.select_ingest_into_chroma","INGESTING", None)
        if returned_data_string is None or len(returned_data_string) == 0:
            logging.info("Null or empty list")
        else:
            logging.info("len(returned_data_string)=[%d]" % (len(returned_data_string),))
        return returned_data_string


    def read_chroma_results_retrieve_and_validate_with_dtd(self, id_ids: list) -> list:
        """
        Input parameters: list<PrimaryKeys>
        FileSystem - read DTD file and SELECT PRODUCT+Related TABLES (where ID IN list provided) file and validate the XML file is well-formed;
        then put results into an OrderedDictionary;
        then execute the SQL on MariaDb.

        :param id_ids: list<str> all PrimaryKeys returned by chroma which are the best matches given the search term received.
        :return: list<object,map> (each element are properties from the PRODUCT and related tables for this id.) (for displaying on the web page results)
        """
#        dtd_content = self.fileUtils.read_file_as_string(self.fileSystemPrefix + "/xmlSqlMapDtd.dtd")
        xml_selectFrom = self.fileUtils.read_file_as_string(self.fileSystemPrefix + "/sqlMap-chromaResults-retrieveFromMysql.xml")
        ret_selectFrom_validated_ok = self.dtdXmlValidator.validate_xml_with_dtd(xml_selectFrom, self.dtd_content)
        if ret_selectFrom_validated_ok is None or ret_selectFrom_validated_ok is False:
            return [] # meaning validation of input data failed
        ord_dict_selectFrom_1 = self.putXmlDataIntoOrderedDictionary.xml_to_ordered_dict(xml_selectFrom)
        logging.info("len=%d.\n", len(ord_dict_selectFrom_1))
        returned_data_string = self.mariaDbStatementsUtil.connect_db_execute_all_sql_statements(config, ord_dict_selectFrom_1, "self.chroma_results_retrieve_from_mariadb","CHROMA_RESULTS_AND_RETRIEVE", id_ids)
        if returned_data_string is None or len(returned_data_string) == 0:
            logging.info("Null or empty list")
        else:
            logging.info("len(returned_data_string)=[%d]" % (len(returned_data_string),))
        return returned_data_string
