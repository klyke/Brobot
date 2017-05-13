import sqlite3

'''
Table: chains, Columns: key(text), words(text)
space delimited
'''

class Server(object):

	def __init__(self, db_name):
		self.db_name = db_name

	def connect(self):
		self.conn = sqlite3.connect(self.db_name)

	def create_table(self, table_name, columns):
		c = self.conn.cursor()
		command = "CREATE TABLE %s %s"%(table_name, columns)
		c.execute(command)

	def add_key_word_pair(self, key, word):
		key = self.iter_to_string(key)
		if(self.key_exists(key)):
			c = self.conn.cursor()
			c.execute("UPDATE chains SET words = words||? WHERE key=?", (" "+word, key))
		else:
			c = self.conn.cursor()
			c.execute("INSERT INTO chains VALUES (?,?)", (key, word))
		self.conn.commit()

	def key_exists(self, formatted_key):
		c = self.conn.cursor()
		c.execute("SELECT EXISTS(SELECT 1 FROM chains WHERE key = ? LIMIT 1)", (formatted_key, ))#TODO: make table name a variable, ? not working
		result = c.fetchone()
		return result[0]

	def get_words(self, key):
		c = self.conn.cursor()
		c.execute("SELECT words FROM chains WHERE key=?", (key, )) 
		result = c.fetchall()
		return result[0][0]

	def get_random_key(self):
		c = self.conn.cursor()
		c.execute("SELECT * FROM chains WHERE key IN (SELECT key FROM chains ORDER BY RANDOM() LIMIT 1)")
		result = c.fetchone()
		return result[0]

	def iter_to_string(self, it):
		return " ".join(it);

	def close(self):
		self.conn.close()
