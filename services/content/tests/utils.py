import contextlib

from sqlalchemy import event


@contextlib.contextmanager
def count_queries(conn):
    queries = []

    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        queries.append(statement)

    event.listen(conn, 'before_cursor_execute', before_cursor_execute)
    try:
        yield queries
    finally:
        event.remove(conn, 'before_cursor_execute', before_cursor_execute)
