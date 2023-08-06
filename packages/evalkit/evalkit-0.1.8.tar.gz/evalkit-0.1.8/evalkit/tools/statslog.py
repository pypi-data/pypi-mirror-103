import numpy as np
from functools import reduce



class StatsLog:
    def __init__(self, funcs:list, spaces="  ", viznt_funcs=[]):
        """
        Arguments:
        :funcs = <list>
            List of functions for statistical information.
        :spaces = <str>
            Margins in a row, between columns of statistical information that the write function returns.
        :non_viz_funcs = <list>
            Contains a list of functions whose results are recorded in log, but not displayed on the screen.
        #TODO
        :format = "json" or "csv"
        :path = <str>
        Path for writing statistical information to a csv or json file.
        """
        self.funcs = funcs
        self.non_viz_funcs = viznt_funcs
        self.spaces = spaces
        self.headers = self.__create_headers()
        self.log = {}
        self.__gen = 1


    def write(self, pop) -> str:
        """
        Calculating and storing statistical information.
        Arguments:
        :pop = <Population>
            Return
        :<str>
            A string of statistical information.
        """
        self.log[self.__gen] = {}
        for func in self.funcs:
            self.log[self.__gen][f"{func.__name__}"] = func( pop )

        ret_str = f"{self.__gen}"+"|"+self.spaces
        for key in self.log[self.__gen]:
            if key not in [ func.__name__ for func in self.non_viz_funcs ]:
                ret_str += str(self.log[self.__gen][key])+"|"+self.spaces
            
        self.__gen += 1
        return ret_str
        
    def __create_headers(self):
        str_headers = "gen" + "|" + self.spaces
        for func in self.funcs:
            if func.__name__ not in [ func.__name__ for func in self.non_viz_funcs ]:
                str_headers += func.__name__ + "|" + self.spaces
        return str_headers