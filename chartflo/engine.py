import pandas as pd
from dataswim import DataSwim
from .widgets import Widget


class ChartFlo(DataSwim, Widget):

    def __repr__(self):
        """
        String representation of the object
        """
        rows = str(len(self.df.columns))
        return '<Chartflo object - ' + rows + " >"

    def new_(self, df=pd.DataFrame(), db=None, quiet=False):
        """
        Returns a new DataSwim instance from a dataframe
        """
        try:
            cf2 = ChartFlo(df, db)
        except Exception as e:
            self.err(e, self.new_, "Can not set new instance")
        if self.autoprint is True and quiet is False:
            self.ok("A new instance was created")
        return cf2


cf = ChartFlo()
