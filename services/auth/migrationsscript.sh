#!/bin/bash
alembic upgrade head
alembic-autogen-check || (alembic revision --autogenerate && alembic upgrade head)
