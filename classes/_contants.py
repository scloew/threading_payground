from collections import namedtuple
"""
group of constant statuses used in return of update functions; statuses are:
'no_change', 'options_update', 'value_set', 'group_updated', 'puzzle_error_found', 'solved'
"""
_Status = namedtuple('_Status', ['no_change', 'options_update', 'value_set',
                                 'group_updated', 'puzzle_error_found', 'solved'])

status = _Status('no_change', 'options_update', 'value_set', 'group_updated', 'puzzle_error_found', 'solved')
