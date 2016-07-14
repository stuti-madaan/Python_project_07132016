import re
from collections import Counter
from pprint import pprint
import math
def read_quotes(input):

    #takes the text file and reads it into a list with the quote and the speaker in the same item

    lines = open(input).read().split('\n')
    quote_list = []
    for i in range(0,len(lines)-1,2):
        quote1 = str(lines[i].replace('"', ""))
        quote1 = str(quote1.replace('.', ""))
        quote1 = str(quote1.replace(',', ""))
        quote1 = str(quote1.replace('?', ""))
        quote1 = str(quote1.replace("(", ""))
        quote1 = str(quote1.replace(")", ""))
        quote1 = str(quote1.replace(":", ""))
        quote1 = str(quote1.replace(";", ""))
        quote2 = quote1 + " - " + str(lines[i+1])
        quote_list.append(quote2)
    return quote_list

def words_from_quotes(input1):

    #splits the quote into a list of words in the quote

    input1 = input1.lower()
    input1 = str(input1.replace('"', ""))
    input1 = str(input1.replace('.', ""))
    input1 = str(input1.replace(',', ""))
    input1 = str(input1.replace('?', ""))
    input1 = str(input1.replace("(", ""))
    input1 = str(input1.replace(")", ""))
    input1 = str(input1.replace(":", ""))
    input1 = str(input1.replace(";", ""))
    input1 = str(input1.replace("'", "`"))
    word_list = re.split(" ",input1)
    return word_list

def create_postings_list_dictionary(input2):

    ###creates a dictionary where the keys are full quotes and the values are dictionaries themselves with a key being
    #  a word and the value being the number of times the word occurs in the full quote

    postings_list = {}
    counter_list = []
    for x in input2:
        counter_dict = {}
        wordlist = words_from_quotes(x)
        for word in wordlist:
            counter = 0
            in_counter_list = False
            for word2 in wordlist:
                if word == word2:
                    counter += 1
            for y in counter_list:
                if word == y:
                    in_counter_list = True
            if in_counter_list == False and word != '-':
                counter_dict[word] = counter
        postings_list[x] = counter_dict
    return postings_list

def reverse_postings_list(input3):

    word_list = []
    keys = input3.keys()

# create list of all words used

    for x in keys:
        y = words_from_quotes(x)
        for words in y:
            if words in word_list:
                pass
            elif words != '-':
                word_list.append(words)

#create reverse posting list by iterating through all words
    word_dict = {}

    for x in word_list:
        word_dict[x] = {}
        for y in keys:
            if x in input3[y]:
                counter = input3[y][x]
                word_dict[x][y] = counter

    return word_dict
def tf(word, quote):

    #gives the tf-idf number given a word and a quote

        max = Counter(quote.split()).most_common()[0][1]
        counter = 0
        word_list = words_from_quotes(quote)
        for x in word_list:
            if x == word:
                counter += 1
        inputnum = counter
        tf = float(inputnum) / float(max)
        quotelist = read_quotes("quotes.txt")
        postlist = create_postings_list_dictionary(quotelist)
        reverse_postlist = reverse_postings_list(postlist)
        idf = math.log(895.0 / float(len(reverse_postlist[word])))
        return idf*tf

def tf_idf(input4):

#pass in a reverse postlist specific to a word where the keys are phrases and the values are the number of times the
#word appears in the phrase

#returns a dictionary with keys being the phrases and values being the tf_idf values
    tf_idf_dict = {}
    for keys in input4.keys():
        max = Counter(keys.split()).most_common()[0][1]
        inputnum = int(input4[keys])
        tf = float(inputnum)/float(max)
        idf = math.log(895.0/float(len(input4)))
        tf_idf_dict[keys] = float(tf*idf)
    return tf_idf_dict

def one_word_quote_search(word):

    #takes in a single word and outputs a dictionary with keys being the phrases and the values being the tf_idf values

    quotelist = read_quotes("quotes.txt")
    postlist = create_postings_list_dictionary(quotelist)
    reverse_postlist = reverse_postings_list(postlist)
    tf_dict = tf_idf(reverse_postlist[word])
    return tf_dict

def mult_words_quote_search(words):

    #takes in a string of undetermined length, splits it into words and returns a dictionary with the sums of the tf-idf
    #for each applicable quote

    quotelist = read_quotes("quotes.txt")
    postlist = create_postings_list_dictionary(quotelist)
    reverse_postlist = reverse_postings_list(postlist)
    words_dict = {}
    word_list = words_from_quotes(words)
    good_word_list = []
    for x in range(len(word_list)):
        if word_list[x] in reverse_postlist.keys():
            words_dict[word_list[x]] = one_word_quote_search(word_list[x])
            good_word_list.append(word_list[x])
    final_dict = {}
    for key in words_dict.keys():
        final_dict.update(words_dict[key])
    for key in final_dict:
        sums = 0
        for y in good_word_list:
            sums += tf(y,key)
        final_dict[key] = sums
    pprint(final_dict)
    return final_dict


mult_words_quote_search(str(raw_input("Input Search: ")))





