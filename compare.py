print("Loading model...")
import spacy
import numpy as np

# en_core_web_lg is a large English language model 
nlp = spacy.load("en_core_web_lg")

""" This model only compares word vectors"""
def word2vec_calculate_similarity(response, markscheme):
    # Tokenize and get Word2Vec vectors for each token
    response_vectors = [token.vector for token in nlp(response) if not token.is_stop and not token.is_punct]
    markscheme_vectors = [token.vector for token in nlp(markscheme) if not token.is_stop and not token.is_punct]
    # If either of the vectors is empty, return a low similarity score
    if not response_vectors or not markscheme_vectors:
        return 0.0

     # Calculate the cosine similarity between the vectors
    similarity_score = np.dot(np.sum(response_vectors, axis=0), np.sum(markscheme_vectors, axis=0))
    response_norm = np.linalg.norm(np.sum(response_vectors, axis=0))
    markscheme_norm = np.linalg.norm(np.sum(markscheme_vectors, axis=0))
    # Normalize the similarity score to be in range [-1, 1]
    if response_norm > 0 and markscheme_norm > 0:
        similarity_score /= (response_norm * markscheme_norm)

    return similarity_score


""" model_used can take in 1 2 or 3, 1 = word2vec, 2 = use, 3 = both"""
def output_mark(response, markscheme, word2vec_threshold=0.8):
    word2vec_similarity_score = 0
    word2vec_similarity_score = word2vec_calculate_similarity(response, markscheme)
    print("Word2vec (threshold: {}): {}".format(word2vec_threshold, word2vec_similarity_score))
    return word2vec_similarity_score > word2vec_threshold

""" For each point given by the student, compare it against each markscheme point which have not been used and award a mark if they are similar
 If a mark is awarded (or more), return a list of indexes in markscheme_point used
 Note: 1 point can be awarded multiple marks """
def mark_per_point(student_point, markscheme, indexes_not_allowed):
    marks = 0
    for i in range(len(markscheme)):
        if i not in indexes_not_allowed:
            print("\nYour point: {}".format(student_point), end=" || ")
            print(markscheme[i])
            if output_mark(student_point, markscheme[i]):
                marks += 1
                indexes_not_allowed.append(i)
                print("Marks +1")
            else:
                print("Marks +0")
            
    return marks

def main():
    # TODO: Done as a drop down
    max_marks = int(input("How many marks the question is worth: "))
    # max_marks = 2 # test data
    no_of_markscheme_points = int(input("Number of points given by the markscheme: "))
    mark_scheme_points = []
    # mark_scheme_points = ["A pixel uses RGB to display a variety of colours", "A pixel is the smallest part in the display"] # test data
    for i in range(no_of_markscheme_points):
        mark_scheme_points.append(input("Point {}: ".format(i + 1)))
    student_response = input("Your response (seperate each point by a full-stop): ")
    # student_response = "A pixel is the smallest unit on a computer's display. It is comprised of RGB values to show different shades" # test data
    student_response_by_point = student_response.split(".")
    indexes_not_allowed = [] # passed by ref
    marks = 0
    for point in student_response_by_point:
        marks += mark_per_point(point, mark_scheme_points, indexes_not_allowed)
        if marks >= max_marks:
            break
    print("Total marks: {}".format(marks))
    
main()

""" 
EXAMPLE INPUT
Marks: 3
Points: 3

The ADC takes samples of the (analogue / continuous electrical) signal / voltage
The samples are quantised // the amplitude (A. height) of each sample is approximated to an integer value // the amplitude (A. height) of samples are measured;
Each sample is assigned a binary value / encoded as a binary value

Response: The ADC will first take samples of the analogue signal at regular intervals. It will then convert these values into the appropriate integer values, the amplitude is measured. Finally the samples are assigned a binary value, and the data is digital
"""