import codecs, re

class SpellCorrector():
	def __init__(self, filepath):
		'''init function
		:param filepath: Relative path to corpus textfile
		'''
		with open(filepath, 'rt', encoding = "ISO-8859-1") as f:
			self.raw_text = f.read()
		self.word_list = re.findall(r"[\w']+", self.raw_text)
		self.vocabulary = set(self.word_list)
		self.size = len(self.word_list)

	def value(self, word):
		'''Returns the value of a word with previous knowledge.
		Currently calculated as probability of finding the same word
		in the corpus text.
		:parm word: Query word.
		'''
		return self.word_list.count(word) / self.size

	def unigram(self, word):
		'''Returns all possibilites of words (known and unknown)
		with up to two mistakes.
		:param words: Set of words.
		'''
		letters = 'abcdefghijklmnopqrstuvwxyz'
		deletes = [word[:i]+word[i+1:] for i in range(len(word))]
		splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
		switchs = [L+R[1]+R[0]+R[2:] for L, R in splits if len(R)>1]
		replaces = [L + letter + R[1:] for L, R in splits for letter in letters]
		adds = [L + letter + R for L, R in splits for letter in letters]
		return set(deletes + switchs + replaces + adds)

	def bigram(self, word, unigrams):
		'''Returns all possibilites of words (known and unknown)
		with up to two mistakes.
		:param word: Query word.
		:param word: all possibilites of words (known and unknown) with a mistake. Previously calculated.
		'''
		return set([e2 for e1 in unigrams for e2 in self.unigram(e1)])

	def filter_in_dictionary(self, words):
		'''Intersection of words and vocabulary.
		:param words: Set of words.
		'''
		return [w for w in words if w in self.vocabulary]

	def candidates(self, word):
		'''Returns all word candidates contained in the vocabulary.
		1. If query word known,
		2. If any unigram known,
		3. If any bigram known,
		4. Just original query.
		:param word: Query word.
		'''
		unig = self.filter_in_dictionary(self.unigram(word))
		candidates = (self.filter_in_dictionary([word]) or
			unig or
			self.filter_in_dictionary(self.bigram(word, unig)) or
			[word])
		return candidates

	def correct(self, word):
		'''Take the known candidate with highest probability
		:param word: Query word.
		'''
		candidates = self.candidates(word)
		return max(candidates, key = self.value)

if __name__=="__main__" :
	corpus = input("Corpus documento path [default: spanish.txt]: ")
	if (corpus==""):
		corpus = "spanish.txt"
	sc = SpellCorrector(corpus)
	word = input("Introduzca palabra: ")
	print(sc.correct(word))