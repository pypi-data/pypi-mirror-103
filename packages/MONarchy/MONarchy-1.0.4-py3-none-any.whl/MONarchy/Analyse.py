import pandas as pd
import json
from .MONarchy import MONarchy
from .MONarchy import NotEnoughValue

class Analyse:

    """ Analyse data from a CSV file using
    descriptive statistics and various MON estimators
    """

    def __init__(self, path):
        """ 
        constructor with a CSV file path
        """
        self.data = pd.read_csv(path)

    def head(self):
        """
        return the data head
        """
        return self.data.head()   


    def describe(self, column):
        """ 
        Return a dictionnary with statistics indicator
        and various MON estimators (for the selected column)
        """

        # variables to return
        mean = self.data[column].mean()
        median = self.data[column].median()

        stat = MONarchy(self.data[column])
        MoN = stat.MoN()
        
        try :
            GMON = stat.GMoN()
            Bin_GMON = stat.Bin_GMoN()
        except NotEnoughValue :
            GMON = "not enough values"
            Bin_GMON = "not enough values"

        # dictionnary
        value = {
            "mean": mean,
            "median": median,
            "MoN": MoN,
            "GMoN" : GMON,
            "Bin_GMoN" : Bin_GMON
        }

        return value

    def infos(self):
        """
        Return a JSON file with statistics indicator
        and various MON estimators for all columns
        """

        l = []
        for col in self.data.columns :
            val= self.describe(col)
            
            l.append([col,val])      
        return json.dumps(l)      


    def info(self, column):

        value = self.describe(column)
        # return the dictionnary as a JSON object
        return json.dumps(value)
