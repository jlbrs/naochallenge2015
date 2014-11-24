from peripheral import Peripheral

class Database(Peripheral):
    """ database class
    This is an abstract class that should not be instantiated, only inherited.
    It provides a dictionary storage with methods to access the content
    """
    def __init__(self):
        # a minimum base storage
        # the internal format should be a dict of dict: 
        # item1:{'single_detail1': 'value', 'list_detail1': ['value1', 'value2', ...], ...}
        self._storage = dict()
        
    def _get_item_detail(self, ref, detail):
        """ get a specific detail of an item """
        # In Python a common idea is to try and apologize...
        # so instead of testing if value exists, try to get it and handle errors
        try:
            return self._storage[ref][detail]
        except KeyError:
            return ""
            
    def _get_list_details(self, detail):
        """ get all the existing values of a given detail """
        # 2 ways of crawling the list, depending on whether the detail is a single or list-detail.
        try:
            return list(set([ self._storage[item][detail] for item in self._storage ]))
        except TypeError:
            return list(set([ value for item in self._storage for value in self._storage[item][detail] ] ))
            
    def _get_items_by_detail(self, detail, value):
        """ find all items with detail=value """
        return [item for item in self._storage if value in self._storage[item][detail]]

     