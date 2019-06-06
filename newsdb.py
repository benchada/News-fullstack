# "Database code" for the DB News.

import datetime
import psycopg2

DBNAME = "news"

def get_query(query_stm):
  """Return all results of the query given as a param"""
  db = psycopg2.connect ( database=DBNAME)
  c = db.cursor()
  c.execute(query_stm)
  RESULT = c.fetchall()
  db.close()
  return RESULT

