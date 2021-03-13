import os
from nltk.stem import SnowballStemmer 
from nltk.tokenize import word_tokenize, sent_tokenize
import os.path
import math


def tf_score(sentences: list):
    terms = dict()
    num_words = 0
    for sentence in sentences:
        for word in word_tokenize(sentence):
            if word.isalnum() == False:
                continue
            num_words += 1
            term = stemmer.stem(word)
            if term in terms:
                terms[term][0] += 1 # update tf
            else:
                terms[term] = [1, 0] # [tf, df]
    return terms, num_words

def process_document_tf(doc_path: str):
    text = open(doc_path, "r", encoding='utf-8').read()
    sentences = sent_tokenize(text)
    terms_tf, doc_num_words = tf_score(sentences)
    return terms_tf, doc_num_words, sentences

def process_outter_document_df(path: str, terms: dict):
    text = open(path, "r", encoding='utf-8').read()
    words = word_tokenize(text)
    doc_terms = set()
    for word in words:
        if word.isalnum() == False:
            continue
        term = stemmer.stem(word)
        doc_terms.add(term)
    for term in terms:
        if term in doc_terms:
            terms[term][1] += 1 # update df

def process_corpus(corpus_path: str, doc_path: str):
    file_paths = list()
    for dirpath, dirs, files in os.walk(corpus_path):
        for file in files:
            path = os.path.abspath(os.path.join(dirpath, file))
            file_paths.append(path)
            # if os.path.samefile(path, os.path.abspath(doc_path)):
            #     continue
            # else:
            #     file_paths.append(path)
    return file_paths, len(file_paths)

def calculate_tf_idf(terms: dict, doc_num_words: int, num_total_documents: int):
    for term in terms:
        terms[term] = terms[term][0]/doc_num_words * math.log(num_total_documents/terms[term][1])

def process_tf_idf(doc_path: str, corpus_path: str):
    terms, doc_num_words, doc_sentences = process_document_tf(doc_path)
    corpus_file_paths, num_total_documents = process_corpus(corpus_path, doc_path)
    for path in corpus_file_paths:
        process_outter_document_df(path, terms)
    calculate_tf_idf(terms, doc_num_words, num_total_documents)
    return terms, doc_sentences

def get_best_tf_idf_scores(tf_idf: dict):
    out = list(tf_idf.keys())
    out.sort()
    out.sort(key=lambda x: tf_idf[x], reverse=True)
    string = ''
    for i in range(len(out)):
        if i == 10:
            break
        elif i == 0:
            string += out[i]
        else:
            string += ', %s' % out[i]
    return string

def get_key_sentences_tf_idf_scores(sent_imp: dict, sentences: list, tf_idf: dict):
    if len(sentences) > 5:
        for key in sent_imp:
            sent_scores = list()
            words = word_tokenize(key)
            for word in words:
                if word.isalnum() == False:
                    continue
                token = stemmer.stem(word)
                sent_scores.append(tf_idf[token])
            sent_scores.sort(reverse=True)
            if len(sent_scores) > 10:
                sent_scores = sent_scores[0:10]
            sent_imp[key] = sum(sent_scores)
        relevant_sent = list(sent_imp.keys())
        relevant_sent.sort(key=lambda x: sentences.index(x))
        relevant_sent.sort(key=lambda x: sent_imp[x], reverse=True)
        if len(relevant_sent) > 5:
            relevant_sent = relevant_sent[0:5]
    else:
        relevant_sent = sentences
    print_count = 0
    string = ''
    for sentence in sentences:
        if sentence in relevant_sent:
            if print_count == 0:
                string += sentence
            else:
                string += ' %s' % sentence
            print_count += 1
    return string


stemmer = None


if __name__ == '__main__':
    corpus = os.path.abspath(input())
    document = os.path.abspath(input())
    stemmer = SnowballStemmer('english')
    tf_idf, sentences = process_tf_idf(document, corpus)
    best_terms = get_best_tf_idf_scores(tf_idf)
    sent_imp = dict.fromkeys(sentences, 0)
    print(best_terms)
    summary = get_key_sentences_tf_idf_scores(sent_imp, sentences, tf_idf)
    print(summary)
    # out_filename = input()
    # f = open('tf-idf\\public\\outputs\\'+ out_filename + '.out', "w", encoding='utf-8')
    # f.write(best_terms + '\n')
    # f.write(summary)
    # f.close()
