from ._contants import status


class Group:
    """Group of 9 cells; Group must have cells with value 1-9"""
    def __init__(self, cells_list):
        self.cells = cells_list
        self.options = {str(i) for i in range(1, 10)} - {c.val for c in self.cells if c}

    def update_options(self, val):
        """

        :param val:
        :return:
        """
        try:
            self.options.remove(val)
            return status.group_updated
        except KeyError:
            return status.puzzle_error_found
