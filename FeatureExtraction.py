# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 14:21:18 2022
Followed articles: 
https://www.thepythoncode.com/article/using-proxies-using-requests-in-python #Proxy setup
https://www.thepythoncode.com/article/extract-web-page-script-and-css-files-in-python #webscraping
https://stackoverflow.com/questions/27162694/can-i-use-beautifulsoup-to-dig-into-inline-javascript #javascript parser
https://www.w3schools.com/tags/att_script_src.asp#:~:text=Definition%20and%20Usage,script%20over%20and%20over%20again.  #Documentation about scripts and "src" attributes
https://medium.com/swlh/entropy-in-the-world-of-computer-science-2bd736e48c58 #Entropy
@author: Tshegofatso Mohlala
"""

from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin

# from slimit.lexer import Lexer

from Proxy import get_tor_session, renew_connection
from RemoveHTML import get_js_only
import csv
import numpy as np
import urllib3  # the lib that handles the url stuff
from collections import deque

import warnings
warnings.filterwarnings('ignore')

def get_js_as_str(js):
    '''
        * Gets the js code and 
        * Returns it as a string which is easier to manipulate
    '''     
    output = "" #The output string                                             
    for item in js:
            output += item

    return output

def get_dir_str_assig(js_code):
    '''
        * Gets the script as input
        * Returns the number of direct string assignments
    '''
    
    #Split the string using ";" this will give you lines of code
    #Further split the splitted strings using "=" this will help us to check for direct assignments
    js_lines = js_code.split(";")  #A list of all js lines in the script
    res_str = [] #A list containing the strings in the js file
    
    for line in js_lines:
        line_list = line.split(',')
        for item in line_list:
            var_assig = item.split('=')  #Breaks down the variable assignment and checks if the element on the 
                                        #right hand side begings with " to check for direct assignment
            length = len(var_assig)  #The length of the var_assig list
            for i in range(length):
                if length == 1:
                    break
                else:
                    for j in range(1, length):
                        if (var_assig[j].startswith('"') and var_assig[j].endswith('"')) or (var_assig[j].startswith("'") and var_assig[j].endswith("'")):
                            res_str.append(var_assig[j])
    
    return res_str

def num_dir_str_assig(str_list):
    '''
        * Given a list of strings it returns the number of strings
    '''
    return len(str_list)

def num_long_str(str_list):
    '''
        * Given a list of strings, it returns the number of long strings
    '''
    count = 0 # The number of long strings
    for item in str_list:
        if len(item)>200:
            count += 1
    
    return count

def num_of_chars(script_str):
    '''
        * Takes a script represented as a string and 
        * returns the number of characters
    '''
    return len(script_str)

def num_spaces(script_str):
    '''
        * Takes js code as a string and counts the number of blank spaces
    '''
    return script_str.count(" ")

def share_of_spaces(num_spaces, num_chars):
    '''
        * calculates the percentage of spaces in the js code
    '''
    if num_chars!=0:
        return num_spaces/num_chars
    else:
        return np.inf

def extract_features(script_str, features):
    '''
        * Gets a script and a list of features to extract
        * Returns the extracted feature values
    '''
    feat_values = []  #The values of the features
    for feat in features:
        feat_values.append(script_str.count(feat))
    
    return feat_values

def count_chars(script_str):
    '''
        * Takes a string as input and
        * returns a dictionary containing the count of each string
    '''
    uniq_chars = set(script_str)  #The characters contained in the string
    countOfChars = dict()
    for element in uniq_chars:
        countOfChar = script_str.count(element)
        countOfChars[element] = countOfChar
        
    return countOfChars

def entropy(prob_list, sample_size):
    '''
        * Gets a list of number of occurences of each item and the sample size
        * returns the entropy
        * The entropy will give us the measure of randomness in the file
        *  The characters in an encrypted javascript files will appear more random than in a normal js file
        *  Using entropy we can quantify this measure
    '''
    entr = 0
    for value in prob_list:
        prob = value/sample_size
        entr += prob*np.log2(prob)

    return -1*entr

# def tokens_(script_str):
#     '''
#         * Gets the js code as a string and
#         * Returns a list of the tokens in the js code
#     '''
#     lexer = Lexer()
#     lexer.input(script_str)
#     words = list()
#     while True:
#         token = lexer.token()
#         if not token:
#             break
#         words.append(token)
#
#     return words

def get_words(words, keywords):
    '''
        * Takes the list of lexical tokens and
        * returns only the tokens which are keywords, variables, datatypes, numbers and strings
    '''
    out_words = [] #A list of the returned tokens
    for token in words:
        if (token.type in ['ID', 'STRING', 'NUMBER']) or (token.value in keywords):
            out_words.append(token)
            
    return out_words

def num_words(words):
    return len(words)

def long_short_words(words):
    '''
        * Gets a list of js words as tokens and 
        * returns the length of the longest and shortest words
    '''
    longest = 0
    long_word = ""
    shortest = np.inf
    short_word = ""
    len_words = 0 #The length of the words
    for token in words:
        length = len(token.value)
        len_words += length
        if length>longest:
            longest = length
            long_word = token.value
        elif length<shortest:
            shortest = length
            short_word = token.value
            
    if len(words)!=0:
        ave = len_words/len(words)
    else:
        ave = np.inf
    
    return short_word, long_word, ave

def len_long_short_word(short_word, long_word):
    '''
        * Gets the shortest and longest words and
        * returns their lengths
    '''
    return len(short_word), len(long_word)

def num_hex(words):
    '''
        * Takes a list of lexical tokens and 
        * returns the number of hexadecimal values
    '''
    count = 0
    for token in words:
        if token.type=='NUMBER' or token.type=='STRING':
            if token.value.startswith('0x'):
                count += 1
                
    return count

def num_keywords(keywords, script_str):
    '''
        * gets the js keywords and the js code as a string and
        * returns the number of keywords in the js code
    '''
    count = 0
    for keyword in keywords:
        count += script_str.count(keyword)
        
    return count

def ratio_keywords_words(num_key, num_words):
    '''
        * Takes the number of keywords and number of words and
        * returns their ratio
    '''
    if num_words!=0:
        return num_key/num_words
    else:
        return np.inf

def read_csv(file):
    '''
        * Takes the path to the csv file you want to read and
        * returns a list of the contents
    '''
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        output_list = list(csv_reader)
        
    return output_list

def get_urls(url):
    '''
        * Gets the url of the website we want to extract
        * Returns a tuple where the first element is a list of inline scripts and the 
          second element is a list of absolute paths of the external js files
    '''
    # initialize a session
    session = get_tor_session()  #Connect to the tor network
    renew_connection() #Get another ip address using the tor network
    # set the User-agent as a regular browser
    session.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    
    # get the HTML content
    html = session.get(url).content
    
    # parse HTML using beautiful soup
    html_format = bs(html, "html.parser")
    url_list = []
    links = html_format.findAll("a",href=True)
    for a in links:   #Get the relative paths within a webpage
        if a['href'].startswith(url):
            url_list.append(a['href'])
            
    return url_list

def get_all_urls(url):
    #The entire set of relative paths within a website
    #That is every relative path from all the webpages of a website
    tmp_list = deque([url])
    url_list = []
    
    while len(tmp_list)!=0:

        to_append = tmp_list.pop()
        if to_append not in url_list: 
            url_list.append(to_append)
            tmp_list += get_urls(url_list[-1])
        
    return url_list
        
def get_scripts(url):
    session = get_tor_session()   #Connect to the tor network
    # set the User-agent as a regular browser to hide the fact that we are using the tor network 
    session.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    
    
    script_files = []  #The links to external js files
    inline_scripts =  []   #The javascript content which is contained within the html files
    try:
        # get the HTML content
        html = session.get(url).content
        renew_connection()
        # parse HTML using beautiful soup
        html_format = bs(html, "html.parser")
        
        # get the JavaScript file
    
        
        for script in html_format.find_all("script"):
            if script.attrs.get("src"):
                # if the tag has the attribute 'src'
                script_url = urljoin(url, script.attrs.get("src"))
                script_files.append(script_url)
            else:
                inline_scripts.append(script)
                
    except:
        pass
    
    return (inline_scripts, script_files)


def extract_all_features(script_str, features, keywords):
    '''
        * Gets the js file as input and extracts all the features
    '''
    feat_values = extract_features(script_str, features)
    
    str_list = get_dir_str_assig(script_str)
    feat_values.append(num_dir_str_assig(str_list))
    feat_values.append(num_of_chars(script_str))
    feat_values.append(num_long_str(str_list))
    num_s = num_spaces(script_str)
    num_c = num_of_chars(script_str)
    feat_values.append(num_s)
    feat_values.append(share_of_spaces(num_s, num_c))
    feat_values.append(entropy(list(count_chars(script_str).values()), num_c))
    lex_words = []#tokens(script_str)
    num_lex = num_hex(lex_words)
    feat_values.append(num_lex)
    num_key = num_keywords(keywords, script_str)
    feat_values.append(num_key)
    num_lex_words = num_words(lex_words)
    feat_values.append(ratio_keywords_words(num_key, num_lex_words))
    feat_values.append(num_lex_words)
    short_word, long_word, ave = long_short_words(lex_words)
    short, long = len_long_short_word(short_word, long_word)
    feat_values.append(long)
    feat_values.append(short)
    feat_values.append(entropy(list(count_chars(long_word).values()), len(long_word)))
    feat_values.append(ave)
    
    norm_words = get_words(lex_words, keywords)
    num_word = num_words(norm_words)
    feat_values.append(ratio_keywords_words(num_key, num_word))
    feat_values.append(num_word)
    short_word_n, long_word_n, ave_n = long_short_words(norm_words)
    short_n, long_n = len_long_short_word(short_word_n, long_word_n)
    feat_values.append(long_n)
    feat_values.append(short_n)
    feat_values.append(entropy(list(count_chars(long_word_n).values()), len(long_word_n)))
    feat_values.append(ave_n)
    
    return feat_values
    
def extract_inline(inline_scripts, features, keywords, feature_list):
    '''
        * Gets the inline scripts and returns the feature values
    '''
    feat_values = list(np.zeros(len(feature_list)))  #The extracted feature values
    for script in inline_scripts:
        new_script = extract_all_features(script, features, keywords)
        tmp = [x + y for x, y in zip(feat_values, new_script)]
        feat_values = tmp
    
    return feat_values

def read_ext_js(pool_man, ext_files):
    '''
        * The pool manager is responsible for making us to connect to multiple urls/websites at the same time
        * gets the http pool manager and external js files as input and
        * returns a list of scripts as strings
    '''
    scripts = []
    for file in ext_files:
        resp = pool_man.request('GET', file)
        try:
            data = resp.data.decode('utf-8')  #utf-8 is the encoding used to transfer data using http
        
        except:
            data = resp.data.decode('latin-1')  #Try other encodings if the utf-8 does not work
            
        scr_str = ""
        for line in data: # files are iterable
            scr_str += line
        scripts.append(get_js_only(scr_str))
        
    return scripts

def feats_web(website_pages, keywords, features, feature_list):
    '''
        * Gets all the website page urls and returns the feature values
    '''
    http = urllib3.PoolManager()
    feat_values = list(np.zeros(len(feature_list)))
    for url in website_pages:
        inline_scripts, external_scripts = get_scripts(url)
        ext_files = read_ext_js(http, external_scripts)
        in_files = []
        for script in inline_scripts:
            in_files.append(get_js_only(get_js_as_str(script)))
            
        scripts = ext_files+in_files
        
        feats = extract_inline(scripts, features, keywords, feature_list)
        tmp = [x + y for x, y in zip(feat_values, feats)]
        feat_values = tmp
        
    return feat_values
    

def get_values(url):
    # Takes the extracted features and passes them to the detector.py file where prediction happens
    keywords = read_csv('keywords.csv')[0]
    features = read_csv('features.csv')[0]
    feature_list = read_csv('AllFeatures.csv')[0]
    
    # URL of the web page you want to extract
    website_pages = get_all_urls(url)
    feat_values = feats_web(website_pages, keywords, features, feature_list)
    
    return feat_values
    


