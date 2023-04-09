from fastapi import Query as QueryParam
from sqlalchemy.orm import Query
from sqlalchemy.orm.attributes import InstrumentedAttribute


class PaginationParams:
    def __init__(
        self,
        page: int = QueryParam(default=1, ge=1),
        size: int = QueryParam(default=10, ge=1, le=50)
    ):
        self.page = page
        self.size = size

    def paginate(self, query: Query, order_by: InstrumentedAttribute) -> Query:
        return query.order_by(order_by).offset(self.size * (self.page - 1)).limit(self.size)
