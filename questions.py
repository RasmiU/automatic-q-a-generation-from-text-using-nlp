from textblob import TextBlob
import nltk
import re
import string,sys,os
from rake_nltk import Rake
from nltk.tokenize import word_tokenize,sent_tokenize
import io
from io import StringIO
import sys
import random

questions=[]
answers=[]
choices=[]

def find_key(sent,tagged_list):
    flag=0
    for tag in tagged_list:
        if(tag[1]=='NNP'):
            key_word=tag[0]
            flag=1
            break
    if(flag==0):
        for tag in tagged_list:
            if(tag[1]=='NNPS'):
                key_word=tag[0]
                flag=1
                break
    if(flag==0):
        for tag in tagged_list:
            if(tag[1]=='NN'):
                key_word=tag[0]
                flag=1
                break
    if(flag==0):
        for tag in tagged_list:
            if(tag[1]=='NNS'):
                key_word=tag[0]
                flag=1
                break
    #tagged_list_copy=tagged_list
    if(flag==1):
        display(sent,key_word)

def display(qtn,ans):
    blank='________'
    qtn = re.sub(ans, blank, qtn, 1, flags=re.IGNORECASE)
    #qtn=str.replace(qtn,ans,blank)
    mc=[]
    disp_mc=[]
    mc=random.sample(choices, 3)
    mc.append(ans)
    disp_mc=random.sample(mc, 4)
    print("Q:",qtn)
    i=1
    for choice in disp_mc:
        print(i,".",choice)
        i=i+1
    print("\nAns:",ans,"\n")
    questions.append(qtn)
    answers.append(ans)
    outF = open('questions.txt',"a")
    outF.write("Q:")
    outF.write(qtn)
    outF.write("\n")
    outF.write("Options:")
    outF.write(str(disp_mc))
    outF.write("\nAns:")
    outF.write(ans)
    outF.write("\n\n")
    outF.close()


#read summary into text and tokenize text into sentences in collection
filename=sys.argv[1]
with open(filename) as f:
            text=f.read()
f.close()
collection=sent_tokenize(text)

#find noun keywords from text
r = Rake(min_length=1, max_length=1) 
r.extract_keywords_from_text(text)
text_keys=r.get_ranked_phrases()
text_keys_tagged=nltk.pos_tag(text_keys)
for tag_key in text_keys_tagged:
    if(tag_key[1]=='NNP'):
        choices.append(tag_key[0])
    #if(tag_key[1]=='NNPS'):
     #   choices.append(tag_key[0])
    if(tag_key[1]=='NN'):
        choices.append(tag_key[0])
    #if(tag_key[1]=='NNS'):
    #    choices.append(tag_key[0])

#find the relevant keywords from each sentence
r = Rake(min_length=1, max_length=1) 
for collec in collection:
    r.extract_keywords_from_text(collec)
    if(r.get_ranked_phrases()):
        phrase_list=r.get_ranked_phrases()
        tagged=nltk.pos_tag(phrase_list)
        #print(collec,"\t",tagged,"\n")
        find_key(collec,tagged)
        