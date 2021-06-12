class Query_engine_base:
    _operators = ('=', '>', '>=', '<', '<=', '<>', 'LIKE', 'NOT LIKE')
    _conjunctions = ('AND', 'AND NOT', 'OR', 'OR NOT', 'NOT')
    _directions = ('ASC', 'DESC')
    _qb_values = {}
    _qb_query = ""
    _table = ""
    _action = ""
    _column = ""
    _selector = ""
    _insert_column = ""
    _insert_value = ""
    _update_column = ""

    def _make_conditions(self, key, operator, value):
        if operator in self._operators:
            return "(" + key + " " + operator + " " + self._make_values(value) + ")"
        return False

    def _make_values(self, value: str):
        num = len(self._qb_values) + 1
        self._qb_values["v" + str(num)] = value
        return "%(v" + str(num) + ")s"

    def _set_query(self):
        if self._action == "INSERT INTO":
            self._qb_query = self._action + " " + self._table + " (" + self._insert_column + ") VALUES (" + self._insert_value + ")"
        elif self._action == "SELECT":
            self._qb_query = self._action + " " + self._column + " FROM " + self._table + " " + self._selector
        elif self._action == "UPDATE":
            self._qb_query = self._action + " " + self._table + " SET " + self._update_column + " " + self._selector
        elif self._action == "DELETE":
            self._qb_query = self._action + " FROM " + self._table + " " + self._selector

    def _reset(self):
        self._qb_query = ""
        self._qb_values = {}
