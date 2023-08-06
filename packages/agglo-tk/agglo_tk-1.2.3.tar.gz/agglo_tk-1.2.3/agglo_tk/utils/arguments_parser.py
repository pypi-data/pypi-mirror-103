# @file 
# @brief 
# @copyright Copyright PA.COTTE 2016

from argparse import ArgumentParser
from re import match


__all__ = ["AtkArgumentParser"]

class AtkArgumentParser(ArgumentParser):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.__option_flag = None
        self.__options = {}

    args = parser.parse_args()


    @property
    def options(self):
      return self.__options


    def add_option_argument(self, *args, **kwargs):
        result = None

        # Options are stored in a list
        kwargs["default"] = []
        kwargs["action"] ="append"

        # Add argument to parser
        result = self.add_argument(*args, **kwargs)

        # Retrieve options flags
        self.__option_flag = result.dest

        return result
    

    def parse_args(self, *args, **kwargs):
        result = None

        # Parse arguments
        result = super().parse_args(*args, **kwargs)

        # Build options dict
        self.__options = {}
        options = getattr(self, self.__option_flag)
        for option in options:
            if match("(.*)[ ]*=", option):
                groups = match("(.*)[ ]*=[ ]*(.*)", option)
                self.__options[groups.group(1)] = groups.group(2)
            else:
                self.__options[option] = None

        return result
