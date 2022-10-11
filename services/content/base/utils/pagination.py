from typing import List

from fastapi import Query as QueryParam
from sqlalchemy.orm import Query


class Params:
    def __init__(self,
                 page: int = QueryParam(default=1, ge=1),
                 size: int = QueryParam(default=10, ge=1)):
        self.page = page
        self.size = size


def paginate(query: Query, params: Params) -> List:
    return query.offset(params.size * (params.page - 1)).limit(params.size).all()
