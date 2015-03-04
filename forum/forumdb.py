#
# Database access functions for the web forum.
# 

import time
import psycopg2
import bleach

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    ## Connect to forum database
    DB = psycopg2.connect("dbname=forum")

    ## Create a cursor to execute dbase commands
    cursor = DB.cursor()
    
    query_content = "SELECT content, time FROM posts ORDER BY time DESC"
    
    cursor.execute(query_content)

    posts = ({'content': str(row[1]), 'time': str(row[0])} 
             for row in cursor.fetchall())
    return posts

    cursor.close()
    DB.close()

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    ## Connect to forum database
    DB = psycopg2.connect("dbname = forum")

    ## Create a cursor to execute dbase commands
    cursor = DB.cursor()

    bleachCycle1 = bleach.clean(content)
    bleached_content = bleach.linkify(bleachCycle1)

    query_content  = "INSERT INTO posts (content) VALUES (%s);"
    post_content = (bleached_content,)

    cursor.execute(query_content, post_content)
    DB.commit()
    DB.close()
