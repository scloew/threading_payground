from ._contants import status


class Cell:
    """represents one of the 81 entries in soduku puzzle"""
    def __init__(self, value):
        self.val = value
        self.options = None if value != '0' else {str(i) for i in range(1, 10)}

    def update_options(self, group_options):
        """
        Take the set of options for cell and intersect with options for cell
        as cell options is subset of group options.
        If there is only one option, set the cell's value to it
        :param group_options: the set of options for a group
        :return: status reflecting what has happened with cell value
        """
        if not self.options or self.options.intersection(group_options) == self.options:
            return status.no_change
        self.options = self.options.intersection(group_options)
        if len(self.options) == 1:
            return self.set_val(self.options.pop())
        elif self.options == set():
            return status.puzzle_error_found
        else:
            return status.options_update

    def set_val(self, val):
        """
        set value for cell
        :param val: value for cel to take
        :return: value_set status
        """
        self.val, self.options = val, None
        return status.value_set

