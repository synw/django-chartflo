from dataswim import DataSwim


class ChartFlo(DataSwim):

    def __repr__(self):
        """
        String representation of the object
        """
        rows = str(len(self.df.columns))
        return '<Chartflo object - ' + rows + " >"


cf = ChartFlo()
