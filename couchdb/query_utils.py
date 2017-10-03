try:
    from functools import reduce
except ImportError:
    pass

'''
maybe overwrite
'''

class Q:
    """
        Q-object need for creating mango_query in filter function
    """
    OR = '$or'
    AND = '$and'

    def __init__(self, **kwarg):
        """
        :param kwarg: field__subfield1__...__mango_operator = value
                      separate by double underscore - '__'
        """
        self.field_cond = list(kwarg.keys())[0]
        self.val = list(kwarg.values())[0]

    @property
    def P(self):
        """
        P - parser
        :return: dict for query
        """
        field_cond_list = self.field_cond.split('__')
        field = field_cond_list[:-1]
        for i, subf in enumerate(field):
            if '_L_' in subf:
                subf_list = subf.split('_L_')
                field.insert(i + 1, '$' + subf_list[1])
                field[i] = subf_list[0]

        cond = '$' + field_cond_list[-1]
        parsed_field_cond = reduce(lambda x, y: {y: x},
                                   reversed(field + [cond, self.val]))
        return parsed_field_cond

    def _combine(self, other, cond):
        """
        :param other: Q or _FQ objects
        :param cond: or, and
        :return:  _FQ object
        """
        query = dict()
        query[cond] = [self.P, other.P]
        return _FQ(query)

    def __or__(self, other):
        return self._combine(other, self.OR)

    def __and__(self, other):
        return self._combine(other, self.AND)


class _FQ(Q):
    '''
        subobject need for _combine method in Q
    '''
    def __init__(self, val):
        self.val = val

    @property
    def P(self):
        return self.val