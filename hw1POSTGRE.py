import psycopg2
import pandas as pd
from IPython.core.display_functions import display
from datetime import datetime
import faker
from faker.providers import DynamicProvider
from faker import Faker
from random import randint, choice

status_provider = DynamicProvider(provider_name='status', elements= ['new','in progress','completed'])
fake = Faker()
fake.add_provider(status_provider)
tasks_list = [
    "Implement authentication system",
    "Optimize database queries",
    "Refactor legacy codebase",
    "Integrate weather API",
    "Design RESTful API endpoints",
    "Write unit tests",
    "Enhance UI/UX",
    "Implement data caching",
    "Research security measures",
    "Migrate to microservices",
    "Optimize image loading",
    "Implement real-time updates",
    "Integrate CI/CD pipeline",
    "Implement access control system",
    "Update dependencies",
    "Refactor CSS styles",
    "Implement error logging",
    "Optimize for mobile",
    "Implement MFA system",
    "Conduct code reviews",
]

tasks_description = [
    "Explore possibilities for improving user authentication system",
    "Analyze database query performance and identify optimization opportunities",
    "Review existing codebase structure and consider refactoring options",
    "Research available weather APIs and their potential integration",
    "Discuss and design architecture for RESTful API endpoints",
    "Write comprehensive unit tests to ensure code reliability",
    "Brainstorm ideas for enhancing user interface and experience",
    "Investigate strategies for implementing efficient data caching mechanisms",
    "Investigate industry-standard security measures and best practices",
    "Evaluate advantages and challenges of migrating to microservices",
    "Study techniques for optimizing image loading in web applications",
    "Discuss potential approaches for implementing real-time updates",
    "Explore options for setting up CI/CD pipelines for automated deployment",
    "Brainstorm ideas for implementing a flexible access control system",
    "Review project dependencies and assess updates and compatibility",
    "Assess current CSS styles and consider options for refactoring",
    "Investigate error logging and monitoring solutions for application",
    "Consider design principles and techniques for mobile optimization",
    "Brainstorm ideas for implementing a robust multi-factor authentication system",
    "Establish guidelines and procedures for conducting code review sessions",
    None
]

def create_tables(con):
  sql = '''
CREATE TABLE users
(id SERIAL PRIMARY KEY,
fullname varchar(100),
email varchar(100) UNIQUE
);
CREATE TABLE status
(id SERIAL PRIMARY KEY,
name varchar(50) UNIQUE
);
CREATE TABLE tasks
(id SERIAL PRIMARY KEY,
title varchar(100),
description text,
status_id int,
user_id int,
CONSTRAINT fk_status_id
      FOREIGN KEY(status_id) 
	  REFERENCES status(id)
	  ON DELETE CASCADE
,  
CONSTRAINT fk_user_id
      FOREIGN KEY(user_id) 
	  REFERENCES users(id)
	  ON DELETE CASCADE
);
'''
  cur = connection.cursor()
  try:
      for querry in sql.split(';'):
        cur.execute(sql)
        con.commit()
  except Exception as e:
      print(e)
  finally:
      cur.close()
  return cur.lastrowid

def drop_tables(con):
  sql = '''
DROP TABLE IF EXISTS users, status, tasks CASCADE;'''
  cur = connection.cursor()
  try:
      cur.execute(sql)
      con.commit()
  except Exception as e:
      print(e)
  finally:
      cur.close()
  return cur.lastrowid

def create_task(con):
  cur = connection.cursor()
  #id's of our statuses
  cursor.execute("SELECT id FROM status")
  result = cursor.fetchall()
  status_id_list = []
  for i in result:
    status_id_list.append(i[0])
  #id's of our users
  cursor.execute("SELECT id FROM users")
  result = cursor.fetchall()
  users_id_list = []
  for i in result:
    users_id_list.append(i[0])
  #query for creating task
  sql = f'''
  INSERT INTO tasks(title,description,status_id,user_id) 
  VALUES('{choice(tasks_list)}','{choice(tasks_description)}','{choice(status_id_list)}','{choice(users_id_list)}');
  '''
  cur = connection.cursor()
  try:
    cur.execute(sql)
    con.commit()
  except Exception as e:
    print(e)
  finally:
    cur.close()
  return cur.lastrowid

def create_status(con):
  sql = f'''
INSERT INTO status(name)
VALUES('{fake.unique.status()}')'''
  cur = connection.cursor()
  try:
    cur.execute(sql)
    con.commit()
  except Exception as e:
      print(e)
  finally:
      cur.close()
  return cur.lastrowid

def create_user(con):
  sql = f'''
INSERT INTO users(fullname,email)
VALUES('{fake.name()}','{fake.unique.email()}')'''
  cur = connection.cursor()
  try:
      cur.execute(sql)
      con.commit()
  except Exception as e:
      print(e)
  finally:
      cur.close()
  return cur.lastrowid

if __name__ == '__main__':
  connection = psycopg2.connect(
  database="", user='postgres',
  password='mysecretpassword', host='localhost', port=5432
  )
  connection.autocommit = True
  drop_tables(connection)
  create_tables(connection)
  cursor = connection.cursor()
  for i in range(100):
    create_user(connection)
  for i in range(3):
    create_status(connection)
  for i in range(100):
    create_task(connection)
  cursor.execute("SELECT * FROM tasks")
  result = cursor.fetchall()
  display(pd.DataFrame(result))
  cursor.execute("SELECT * FROM users")
  result = cursor.fetchall()
  display(pd.DataFrame(result))
  cursor.execute("SELECT * FROM status")
  result = cursor.fetchall()
  display(pd.DataFrame(result))
  cursor.close()
  connection.close()
  