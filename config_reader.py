import logging
from ast import literal_eval
from typing import Dict


class ConfigReader:
    """
    ConfigReader to read config files and return a dict with the content of those files
    Standard syntax for config files is lines of key = values, comments are accepted with #
    Example test_config.txt:

    test_1 = value 1
    test_2 = 14.5 # comment 1
    # comment 2
    test_3 = True

    Example:

    config = ConfigReader('/path/to/test_config.txt')
    a = config.test_1
    b = config.test_2
    c = config.test_3

    """

    def __init__(self, file_path: str):

        self.__file_path__: str = file_path
        data: Dict[str, str] = self.__dict__
        if file_path is not None:

            with open(file_path) as file:

                for line_no, line in enumerate(file.readlines()):

                    # remove comments
                    line: str = line.strip().split("#")[0]

                    if line == '':
                        continue

                    # Continue if valid line exists
                    key_value = [token.strip() for token in line.split("=")]

                    # Ensure the line is in the right structure <key> = <value>
                    assert len(key_value) == 2, "Syntax error : line %d, expected one argument" \
                                                " on either side of the = operator" % line_no

                    key = key_value[0]
                    value = key_value[1]

                    # if value is literal with special type, evaluate it
                    try:
                        value = literal_eval(value)
                    except SyntaxError:
                        pass
                    except ValueError:
                        pass

                    # Add to the map
                    data[key] = value

        # Log config contents
        logging.info("Read config file at : %s" % file_path)
        for key in data:
            logging.info("%s = %s" % (key, data[key]))

    # Override class methods to directly access attributes
    def __getattr__(self, item):
        if item not in self.__dict__:
            raise AttributeError("Cannot find config attribute '%s' @ %s" % (item, self.__file_path__))
        return self.__dict__[item]

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __delattr__(self, item):
        self.__dict__.__delattr__(item)
