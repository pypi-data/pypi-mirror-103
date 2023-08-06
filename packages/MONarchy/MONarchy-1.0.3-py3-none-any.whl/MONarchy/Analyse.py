import pandas as pd
import json
from .MONarchy import MONarchy

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


    def info(self, column):
        """ 
        Return a JSON file with statistics indicator
        and various MON estimators
        """

        # variables to return
        mean = self.data[column].mean()
        median = self.data[column].median()

        stat = MONarchy(self.data[column])
        MoN = stat.MoN()
        GMON = stat.GMoN()
        Bin_GMON = stat.Bin_GMoN()

        # dictionnary

        value = {
            "mean": mean,
            "median": median,
            "MoN": MoN,
            "GMoN" : GMON,
            "Bin_GMoN" : Bin_GMON
        }

        # return the dictionnary as a JSON object
        return json.dumps(value)
