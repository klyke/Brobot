import random
from word_server import Server

terminating_punc = [".", "!", "?"]

class Markov(object):

	def load(self, database_name):
		self.server = Server(database_name)
		self.server.connect()

	def update(self, msg, key_length=2):
		self.add_text_to_chain(msg, key_length)

	def add_text_to_chain(self, msg, key_length):
		msg = self.format_message(msg)
		for i in range(len(msg) - key_length):
			key = []
			for j in range(key_length):
				key.append(msg[i+j])
			word = msg[i+key_length]
			self.server.add_key_word_pair(key, word)

	def format_message(self, msg):
		msg = msg.replace("\n", " ").replace("\r", " ").replace("\t", " ")
		msg = [self.strip_word(w) for w in msg.split(" ") if (not w.isspace() and ".com" not in w and w != "")]
		return msg

	def create_message(self, num_words):
		return_message = ""
		key = self.server.get_random_key()
		return_message += self.capitalize_first(key) + " "
		
		for _ in range(num_words):
			try:
				words = self.server.get_words(key)
				word = random.choice(words.split(" "))
				if word == "":
					return_message += " "
				else:
					return_message += word + " "
				new_key = key.split(" ")[1:]
				new_key.append(word)
				key = " ".join(new_key)

			except Exception as e:
				return_message = return_message.strip()
				if return_message[-1] not in terminating_punc:
					return_message += random.choice(terminating_punc) 
				key = self.server.get_random_key()
				return_message += self.capitalize_first(key) + " "

		return_message = self.remove_mulit_spaces(return_message)
		return_message = return_message.strip()
		if(return_message[-1] not in terminating_punc):
			return_message += random.choice(terminating_punc)
		return return_message

	def capitalize_first(self, s):
		words = s.split(" ")
		words[0] = words[0].title()
		return " ".join(words)

	def strip_word(self, word):
		word = word.strip()
		out_word = ""
		ok_punc = [".", "!", "?", "=", "/"]
		for char in word:
			if char.isalpha() or char.isdigit() or char in ok_punc:
				out_word += char
		return out_word

	def remove_mulit_spaces(self, msg):
		while "  " in msg:
			msg = msg.replace("  ", " ")
		return msg

	def finish(self):
		self.server.close()
