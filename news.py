#!/usr/bin/env python3
# 
# A buggy web service in need of a database.

from flask import Flask, request, redirect, url_for

from newsdb import get_query

import datetime

app = Flask(__name__)

# HTML template for the project page
HTML_WRAP = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>Project # 1 Chada </title>
    <style>
      h1, form { text-align: center; }
      textarea { width: 400px; height: 100px; }
      div.answer { border: 1px solid #999;
                 padding: 10px 10px;
                 margin: 10px 20%%; }
      hr.postbound { width: 50%%; }
      em.date { color: #999 }
    </style>
  </head>
  <body>
    <h1>Project #1 - Chada </h1> 
    <br>
    <h3><em> 1. What are the most popular three articles of all time? </em></h3>
    <!-- post content will go here -->
    %s

    <br>
    <h3><em> 2. Who are the most popular article authors of all time? </em></h3>
    %s

    <br>
    <h3><em> 3. On which days did more than 1 %% of requests lead to errors? </em></h3>
    %s

  </body>
</html>
'''

# HTML template for an individual comment
POST = '''\
    <div class=answer><em>" %s "</em> -- %s views </div>
'''
LINE = '''\
    <div class=answer><em> %s </em> -- %s %% errors </div>
'''
QUERY1 = "select path, count(*) as num_appearances from log group by path order by num_appearances desc"
QUERY2 = "select articles.author, authors.name, sum (article_views) as views_sum from (select slug, articles.author, count(*) as article_views from articles join log on path = CONCAT('/article/',slug) group by slug, articles.author) as views,articles join authors on articles.author = authors.id group by articles.author,authors.name order by views_sum desc ;"
QUERY3 = "select overall_count.date, ((error_count.count*100.00)/overall_count.count) as Error_Percentage from overall_count join error_count on overall_count.date =error_count.date where ((error_count.count*100.00)/overall_count.count) > 1 ;"

@app.route('/', methods=['GET'])
def main():
  '''Main page of the forum.'''

  #processing the data for the first answer
  data = get_query(QUERY1)
  cleaned_data =[]
  for path, view in data:
    #counting only the articles & removing the article prefix and '-'
    if "/article/" in path:
      article_name = path[9:]
      article_name = article_name.replace("-", " ")
      cleaned_data.append([article_name.capitalize(),view])

  #taking only the top three articles
  top_three = cleaned_data[:3]

  first_answer = "".join(POST % (path, views) for path, views in top_three)

  '''  Preparing data for the second answer'''
  second_data = get_query(QUERY2)
  second_answer = "".join(POST % (author_name, article_views) for auth_id, author_name, article_views in second_data)

  '''  Preparing data for the third answer'''
  third_dataset = get_query(QUERY3)

  third_answer = "".join(LINE % ((day.strftime("%B %d , %Y") ), str(round(error_prcnt,1)) ) for  day, error_prcnt in third_dataset)

  html = HTML_WRAP % (first_answer, second_answer, third_answer)
  return html


@app.route('/', methods=['POST'])
def post():
  '''New post submission.'''
  message = request.form['content']
  add_post(message)
  return redirect(url_for('main'))


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000)

