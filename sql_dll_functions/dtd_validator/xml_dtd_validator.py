import logging
from lxml import etree
import io

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Log to console
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

# Also log to a file
file_handler = logging.FileHandler("./logs/xml-with-dtd-validation.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class DtdXmlValidator:

    def __init__(self):
        self.required_encoding = 'utf-8'

    def validate_xml_with_dtd(self, xml_str: str, dtd_str: str) -> bool | None:
        """
        accepts two files as two UTF-8 strings (xml file content and DTD content)
        applies DTD validation of the xml file.
        [The intent is to check that we have DB TABLE name and SQL statements to execute on that table]

        :param xml_str: content of xml file
        :param dtd_str: content of dtd file
        :return: None or False if failed. True if the xml data is valid.
        """
        try:
            # Parse the DTD
            dtd = etree.DTD(io.BytesIO(dtd_str.encode(self.required_encoding)))

            # Parse the XML
            root = etree.fromstring(xml_str.encode(self.required_encoding))

            # Validate
            if dtd.validate(root):
                logging.info("XML is valid according to the DTD.")
                return True
            else:
                logging.error("❌ XML is INVALID.")
                logging.error(dtd.error_log.filter_from_errors())
                return False

        except etree.XMLSyntaxError as e:
            logging.error(f"XML Syntax Error: {e}")
            return None
