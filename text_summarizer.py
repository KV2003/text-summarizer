from heapq import nlargest
from string import punctuation

import spacy
from spacy.lang.en.stop_words import STOP_WORDS


def summarizer(raw_docs):
    stop_words=list(STOP_WORDS)
    nlp=spacy.load("en_core_web_sm")
    doc=nlp(raw_docs)
    tokens =[token.text for token in doc] 
    word_freq={}
    for word in doc:
        if word.text.lower() not in stop_words and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text]=1
            else:
                word_freq[word.text]+=1
    #print(word_freq)
    max_freq=max(word_freq.values())
    #print(max_freq)
    for word in word_freq.keys():
        word_freq[word]=word_freq[word]/max_freq
    #print(word_freq)
    sent_tokens=[sent for sent in doc.sents]
    #print(sent_tokens)
    sent_score={}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_score.keys():
                    sent_score[sent]=word_freq[word.text]
                else:
                    sent_score[sent]+=word_freq[word.text]
    #print(sent_score)
    select_len = int(len(sent_tokens)*0.3)
    #print(select_len)
    summary = nlargest(select_len,sent_score,key=sent_score.get)
    #print(summary)
    final_summary=[word.text for word in summary]
    summary=" ".join(final_summary)
    '''print(text)
    print("len of original text:",len(text.split(" ")))
    print(summary)
    print("len of generated summary:",len(summary.split(" ")))'''
    return summary,doc,len(raw_docs.split(" ")),len(summary.split(" "))