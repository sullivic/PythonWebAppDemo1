import logging
from lxml import etree
from collections import OrderedDict

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Log to console
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

# Also log to a file
file_handler = logging.FileHandler("./logs/xml-data-in-ordered-dict.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class PutXmlDataIntoOrderedDictionary:

    def __init__(self):
        self.required_encoding = 'utf-8'
        self.find_all_entry_tag = ".//Entry"
        self.find_all_table_name_tag = ".//TableName"
        self.find_all_table_sql_tag = ".//TableSql"
        self.find_all_tag_containing_comment_string = ".//comment()"

    def xml_to_ordered_dict(self, xml_input: str) -> OrderedDict:
        """
        XML-DOM-parse the XML document,
        find the tags that contain
        the data (TABLE-NAME and SQL-STATEMENTS) and
        extract them and store in
        an OrderedDict to be returned from this function.

        :param xml_input: xml file as string content to be parsed by XML parser
        :return: populated OrderedDict
        """

        # Parse the XML string
        # Create a parser that preserves comments
        parser = etree.XMLParser(remove_comments=False)
    #    root = etree.fromstring(xml_data.encode('utf-8'), parser=parser)
        root = etree.fromstring(xml_input.encode(self.required_encoding), parser=parser)

    #    # Initialize the OrderedDict
        result = OrderedDict()

        entries = root.findall(self.find_all_entry_tag)#(".//Entry")

        # Loop through elements in document order
        for entry in entries:

            # table name is going to be key in the dict
            table_name_tag = entry.find(self.find_all_table_name_tag)#(".//TableName")
            table_name_tag_comment = table_name_tag.xpath(self.find_all_tag_containing_comment_string)#('.//comment()')
            table_name_value = table_name_tag_comment[0].text
            table_name_value = table_name_value[1:(len(table_name_value)-1)]
            logging.info("table_name_value=[%s]" % (table_name_value,))

            # table sql is going to be value in the dict
            table_sql_tags = entry.findall(self.find_all_table_sql_tag)#(".//TableSql")

            list_table_sql_values = []
            for table_sql_tag in table_sql_tags:

                table_sql_tag_comment = table_sql_tag.xpath(self.find_all_tag_containing_comment_string)#('.//comment()')
                table_sql_value = table_sql_tag_comment[0].text
                table_sql_value = table_sql_value[1:(len(table_sql_value) - 1)]
                logging.info("table_sql_value=[%s]" % (table_sql_value,))
                list_table_sql_values.append(table_sql_value)

            result[table_name_value] = list_table_sql_values

        return result
