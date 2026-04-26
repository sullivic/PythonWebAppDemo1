import logging

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Log to console
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

# Also log to a file
file_handler = logging.FileHandler("./logs/module-file-utils.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class FileUtils:

    def __init__(self):
        self.required_encoding = 'utf-8'

    def read_file_as_string(self, file_path: str) -> str | None:
        """
        Utility to read in an input file (xml, dtd) as UTF-8 and return the file contents as a string

        :param file_path: file path relative to project root (runtime directory)
        :return: None if failed. string if successful
        """
        try:
            with open(file_path, 'r', encoding=self.required_encoding) as file:
                content = file.read()
            return content
        except FileNotFoundError as fnf_error:
            logging.error("The file was not found. {fnf_error}")
            return None
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None
