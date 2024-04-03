from naiveBayesPredict import NaiveBayesModel
import compare

q1_model = NaiveBayesModel("q1.csv")
# print(q1_model.question)
response = input("Answer: ")
print(q1_model.predict(response))
