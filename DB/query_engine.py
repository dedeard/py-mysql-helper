from DB.query_engine_base import Query_engine_base


class Query_engine(Query_engine_base):
    def set_column(self, columns: tuple):
        self._column = ", ".join(columns)
        return self

    def set_values(self, values: dict):
        if self._action == "INSERT INTO":
            self._insert_column = ", ".join(tuple(values.keys()))
            data = []
            for value in values.values():
                data.append(self._make_values(value))
            self._insert_value = ", ".join(data)
        elif self._action == "UPDATE":
            data = []
            for key, value in values.items():
                data.append(key + " = " + self._make_values(value))
            self._update_column = ", ".join(data)
        return self

    def where(self):
        self._selector = "WHERE"
        return self

    def sub_where(self, sub: str = "OR"):
        sub = sub.upper()
        if sub in self._conjunctions:
            self._selector = self._selector + " " + sub
            return self
        return False

    def order_by(self, keys: tuple, direction: str = "ASC"):
        direction = direction.upper()
        if direction in self._directions:
            self._selector = self._selector + " ORDER BY " + ", ".join(keys) + " " + direction
        return self

    def limit(self, limit: int, offset: int = 0):
        self._selector = self._selector + " LIMIT " + str(limit)
        if offset > 0:
            self._selector = self._selector + " OFFSET " + str(offset)
        return self

    def equal(self, key, value):
        condition = self._make_conditions(key, "=", value)
        self._selector = self._selector + " " + condition
        return self

    def not_equal(self, key, value):
        condition = self._make_conditions(key, "<>", value)
        self._selector = self._selector + " " + condition
        return self

    def less_than(self, key, value):
        condition = self._make_conditions(key, "<", value)
        self._selector = self._selector + " " + condition
        return self

    def less_than_or_equal(self, key, value):
        condition = self._make_conditions(key, "<=", value)
        self._selector = self._selector + " " + condition
        return self

    def greater_than(self, key, value):
        condition = self._make_conditions(key, ">", value)
        self._selector = self._selector + " " + condition
        return self

    def greater_than_or_equal(self, key, value):
        condition = self._make_conditions(key, ">=", value)
        self._selector = self._selector + " " + condition
        return self

    def like(self, key, value):
        condition = self._make_conditions(key, "LIKE", value)
        self._selector = self._selector + " " + condition
        return self

    def not_like(self, key, value):
        condition = self._make_conditions(key, "NOT LIKE", value)
        self._selector = self._selector + " " + condition
        return self
