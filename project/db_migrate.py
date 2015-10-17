from views import db
from _config import DATABASE_PATH

import sqlite3
from datetime import datetime

with sqlite3.connect(DATABASE_PATH) as connection:
	#get a cursor object used to execute sql commands
	c = connection.cursor()
	
	#temporarily change the name to tasks table
	# c.execute("""ALTER TABLE tasks RENAME TO old_tasks""")

	#recreate the new tasks table with a updated schema
	db.create_all()

	#retrieve data from old tasks table
	c.execute("""SELECT name, due_date, priority, status FROM old_tasks ORDER BY task_id ASC""")

	#sa
	data = [(row[0], row[1], row[2], row[3], datetime.now(),1) for row in c.fetchall()]

	#insert into tasks table
	c.executemany("""INSERT INTO tasks (name, due_date, priority, status, posted_date, user_id)
	 VALUES (?,?,?,?,?,?)""", data)

	#delete old task table
	c.execute("DROP TABLE old_tasks")
