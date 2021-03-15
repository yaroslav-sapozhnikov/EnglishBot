import random
from pymongo import MongoClient


class DataBase:

    def __init__(self):
        self.cluster = MongoClient(
            "mongodb+srv://main:vA4u7DPQZLZoYe3q@englishbot.gwdyj.mongodb.net/main?retryWrites=true&w=majority")
        self.db = self.cluster.main
        self.words = self.db.words

    def word_count(self):
        return self.words.count()

    def add_word(self, word):
        print(self.words.count_documents({"word": word["word"]}))
        if self.words.count_documents({"word": word["word"]}) == 0:
            self.words.insert_one(word)
            return 1
        else:
            return 0

    def parse_words(self):
        with open("ParseFile.txt", "r") as f:
            count = 0
            for i in f.read().splitlines():
                word = Word(i)
                count += self.add_word(word.to_json())
        return count

    def get_random(self):
        return self.words.find_one({"_id": random.randint(0, self.word_count())})

    def update_yes(self, word):
        self.words.update_one({'word': word['word']}, {'$set': {'yes': int(word['yes'])+1}})

    def update_no(self, word):
        self.words.update_one({'word': word['word']}, {'$set': {'no': int(word['no'])+1}})


class Word:

    words = DataBase().words

    def __init__(self, word):
        self.word = word
        self.id = self.generate_id()
        self.yes = 0
        self.no = 0

    def generate_id(self):
        return self.words.count() + 1

    def to_json(self):
        return {"_id": self.generate_id(), "word": self.word, "yes": self.yes, "no": self.no}

