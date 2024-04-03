import csv


class NaiveBayesModel:
    def __init__(self, file_name):
        self.all_words = []
        self.positive_words = []
        self.negative_words = []
        self.question = ""
        self.set_model(file_name)
        

    # Assign words to be positive or negative based on if that response gained or lost a mark
    def set_model(self, file_name):
        try:
            with open(file_name, "r") as f:
                f_reader = csv.reader(f)
                i = 0
                for row in f_reader:
                    i += 1
                    if i == 1:
                        self.question = row[1]
                    if i >= 3:
                        self.all_words.append([row[0], int(row[1])])
            for response in self.all_words:
                for word in response[0].split(" "):
                    punctuationless = self.preprocess(word)
                    if response[1] == 1:
                        self.positive_words.append(punctuationless)
                    else:
                        self.negative_words.append(punctuationless)
        except:
            print("Error occured in loading the model")

    def preprocess(self, word):
        return word.replace(",", "").replace(".", "").replace("!", "").replace("?", "").lower()

    def number_of_words_in(self, word, words):
        count = 1 # set to 1 for laplace smoothing
        for i in range(len(words)):
            if word == words[i]:
                count += 1
        return count

    def predict(self, response):
        response = response.split(" ")
        total_words = len(self.positive_words) + len(self.negative_words)
        pos_p = len(self.positive_words) / total_words
        neg_p = 1 - pos_p
        for i in range(len(response)):
            response[i] = self.preprocess(response[i])
            # From equation: pos_p = a * P(positive) * P(Word|Positive) * ...
            # Neg_p is used to normalise the result later on
            pos_p = pos_p * (self.number_of_words_in(response[i], self.positive_words) / len(self.positive_words))
            neg_p = neg_p * (self.number_of_words_in(response[i], self.negative_words) / len(self.negative_words))
        # Normalising constant
        a = 1 / (pos_p + neg_p)
        pos_p = a * pos_p
        if len(response) <= 2:
            pos_p = pos_p * 0.5
        print("Marks: " + str(round(pos_p)))
        return pos_p
        
