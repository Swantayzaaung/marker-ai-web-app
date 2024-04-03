print("Loading model...")
import spacy
from spacy import displacy
from gensim.models import Word2Vec
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

# en_core_web_lg is a large English language model 
nlp = spacy.load("en_core_web_lg")

# Load Universal Sentence Encoder
use_model_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
use_embed = hub.load(use_model_url)

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

""" model uses sentence embeddings, it can capture contextual information"""
def calculate_similarity_use(response, markscheme):
    # Get embeddings for the response and mark scheme
    response_embedding = use_embed([response])[0].numpy()
    markscheme_embedding = use_embed([markscheme])[0].numpy()
    # Calculate the cosine similarity between the embeddings
    similarity_score = np.dot(response_embedding, markscheme_embedding) / (np.linalg.norm(response_embedding) * np.linalg.norm(markscheme_embedding))

    return similarity_score

""" model_used can take in 1 2 or 3, 1 = word2vec, 2 = use, 3 = both"""
def output_mark(response, markscheme, model_used = 1, word2vec_threshold=0.78, use_threshold=0.5):
    word2vec_similarity_score = 0
    use_similarity_score = 0
    word2vec_similarity_score = word2vec_calculate_similarity(response, markscheme)
    use_similarity_score = calculate_similarity_use(response, markscheme)
    if model_used == 1:
        print("Word2vec (threshold: {}): {}".format(word2vec_threshold, word2vec_similarity_score))
        return word2vec_similarity_score > word2vec_threshold
    elif model_used == 2:
        print("USE (threshold: {}): {}".format(use_threshold, use_similarity_score))
        return use_similarity_score > use_threshold
    else:
        print("Word2vec (threshold: {}): {}".format(word2vec_threshold, word2vec_similarity_score), end=" || ")
        print("USE (threshold: {}): {}".format(use_threshold, use_similarity_score))
        return word2vec_similarity_score > word2vec_threshold and use_similarity_score > use_threshold

""" For each point given by the student, compare it against each markscheme point which have not been used and award a mark if they are similar
 If a mark is awarded (or more), return a list of indexes in markscheme_point used
 Note: 1 point can be awarded multiple marks """
def mark_per_point(student_point, markscheme, indexes_not_allowed, model_used = 1):
    marks = 0
    for i in range(len(markscheme)):
        if i not in indexes_not_allowed:
            print("\nYour point: {}".format(student_point), end=" || ")
            print(markscheme[i])
            if output_mark(student_point, markscheme[i], model_used):
                marks += 1
                indexes_not_allowed.append(i)
                print("Marks +1")
            else:
                print("Marks +0")
            
    return marks

def main():
    # TODO: Done as a drop down
    example_ms = [[1, 1, ["Physical components of a computer system"]],
                   [2, 3, ["Microphone", "Camera", "Sensors"]], 
                   [4, 6, ["Read Only Memory", "Non-volatile//Data is not lost when the computer is switched off", "Used to store the startup instructions/BIOS", "Random Access Memory", "Volatile//Data is lost when the computer is turned off", "Stores the current running program/instruction", "RAM can be written to and read from"]]]
    example_responses = ["Physical parts of a computer", "Microphone. Camera", "ROM stands for Read only Memory. It is volatile. It is used to store startup instructions for the computer. RAM stands for Random Access Memory. It is volatile, which means data is lost when powered off. It stores the current running program."]
    model_used = 1

    for i in range(len(example_responses)):
        for i in range(len()):
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
Model: 3
Marks: 3
Points: 3

The ADC takes samples of the (analogue / continuous electrical) signal / voltage
The samples are quantised // the amplitude (A. height) of each sample is approximated to an integer value // the amplitude (A. height) of samples are measured;
Each sample is assigned a binary value / encoded as a binary value

Response: The ADC will first take samples of the analogue signal at regular intervals. It will then convert these values into the appropriate integer values, the amplitude is measure
d. Finally the samples are assigned a binary value, and the data is digital
"""