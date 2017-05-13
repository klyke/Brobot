import random
import os
from markov_chain import Markov
from gmail_scrapper import Scrapper

min_num_words = 50
max_num_words = 200

class Brobot(object):

	def __init__(self, db_path):
		self.markov = Markov()
		self.markov.load(db_path)

	def update(self, msg):
		if ("Brobot") in msg or "robot" in msg or "bot" in msg:
			print("BROBOT WAS MENTIONED")
		self.markov.update(msg)

	def make_response(self):
		num_words = random.randint(min_num_words, max_num_words)
		msg = self.markov.create_message(num_words)
		return msg

	def train(self, email, pwd, num):
		scrapper = Scrapper()
		msg_getter = scrapper.get_emails(email, pwd)
		i = 0
		for msg in msg_getter:
			msg = self.remove_gmail_artifacts(msg)
			self.update(msg)
			print("Training..." + str(i))
			i+=1
			if i >= num:
				break

	def remove_gmail_artifacts(self, msg):
		return_message = ""

		for line in msg.split("\n"):
			if line.startswith(">") or line.isspace():
				continue
			elif line.startswith("On") and "wrote:" in line:
				continue
			elif line.startswith("Begin forwarded message:"):
				continue
			elif line.startswith("Sent from my iPhone"):
				continue
			else:
				return_message += line + "\n"
		return return_message

	def run(self, email, pwd):
		pass

	def new_email_event(self):
		pass

	def finish(self):
		self.markov.finish()

	def clear_database(self):
		r = raw_input("Are you sure you want to clear the database? (Y/N): ")
		if r.upper() == "Y":
			conn = self.markov.server.conn
			c = conn.cursor()
			c.execute("DELETE FROM chains")
			conn.commit()


def main():
	brobot = Brobot("brobot.db")
	# brobot.clear_database()
	# brobot.train(some_email, some_password, 150)
	print(brobot.make_response())

if __name__ == '__main__':
	main()



