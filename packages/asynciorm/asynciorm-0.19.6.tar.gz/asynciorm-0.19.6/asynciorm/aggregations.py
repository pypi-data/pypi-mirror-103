class BaseAggregation(object):

    def __init__(self, column_name):
        self.column_name = column_name
    
    def sql(self):
        return self.__class__.__name__ + f'({self.column_name})'

class MIN(BaseAggregation):
    pass

class MAX(BaseAggregation):
    pass

class AVG(BaseAggregation):
    pass

class COUNT(BaseAggregation):
    pass

class SUM(BaseAggregation):
    pass