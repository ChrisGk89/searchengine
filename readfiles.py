#!/usr/bin/env python
# -*- coding: utf-8 -*-
from nltk.corpus import stopwords
import sys
import csv
from Page import Page
import os
import nltk
nltk.download('stopwords')
reload(sys)
sys.setdefaultencoding('utf8')


class documentLists():
    def __init__(self):
        self.wordToId = {}
        self.pages = []

    # this  function will read all the files in the folder and sub-folders
    def all_documents_name(self, folderName):
        documents_name = []
        fileindex = 0
        for root, dirs, files in os.walk(folderName):
            for filename in files:
                docname = os.path.join(root, filename)
                documents_name.insert(fileindex, docname)
                fileindex = fileindex + 1
        del documents_name[0]
        return documents_name

    # iterate through all docs to find and append all words and links exists in the document.
    def iterateOverAllDocs(self):
        print "started"
        docsnameslist = self.all_documents_name("data/Words")
        linksList = self.all_documents_name("data/Links")
        nos_of_documents = len(docsnameslist)
        #print nos_of_documents

        # Check all the documents
        for i in range(nos_of_documents - 1):
            page = Page()
            filename = docsnameslist[i].split('/')[3]
            print filename
            page.url = "/wiki/" + filename
            stop_words = set(stopwords.words('english'))

            # Then opens the docsnameslist and read it as file
            with open(docsnameslist[i], "r") as f:
                # We use delimiter a one-character string used to separate fields
                # in our case is white space
                reader = csv.reader(f, delimiter=" ", quoting=csv.QUOTE_NONE)
                for row in reader:
                    for word in row:
                       if word not in stop_words:
                           if word != "":
                             word_exist = self.keyExists(word)
                             if word_exist:
                               word_id = self.getIdForWord(word)
                             else:
                               word_id = len(self.wordToId)
                               self.wordToId[word] = word_id

                           page.words.append(word_id)

            with open(linksList[i], "r") as f:
                reader = csv.reader(f, delimiter="\n", quoting=csv.QUOTE_NONE)
                for row in reader:
                    for link in row:
                        page.links.append(link)

            self.pages.append(page)
            print "file index: " + str(i)
        return None

    # We read the words from every document in wikipedia/words
    def getDocumentTextFromDocId(self, doc_id):
        docsnameslist = self.all_documents_name("wikipedia/Words")
        # noinspection PyBroadException
        try:
            str1 = open(docsnameslist[doc_id]).read()
        except:
            str1 = ""
        return str1

    # this function returns a list of tokenized and stemmed words of any text
    # Stemming is the process of reducing inflected (or sometimes derived) words to their stem,
    # base or root form generally a written word form.
    def getTokenizedAndNormalizedList(self, doc_text):
        tokens = nltk.word_tokenize(doc_text)

        ps = nltk.stem.PorterStemmer()
        stop_words = set(stopwords.words('english'))

        # Removing Punctuation after tokenization
        stemmed = []
        for words in tokens:
            if words not in stop_words:
                stemmed.append(ps.stem(words))
        return stemmed

    # Returning the id of the word instead of the word itself
    def getIdForWord(self, word):
        if word in self.wordToId:
            return self.wordToId[word]
        else:
            return

    # We check if any word id is missing
    def keyExists(self, word):
        if word in self.wordToId:
            return True
        else:
            return False

    # We get the documents ids that we previously indexed
    # that include the word id we ask for in the search
    def getDocuments(self, words):
        pages = []
        for word_id in words:
            for page in self.pages:
                if word_id in page.words:
                    if page not in pages:
                        pages.append(page)
        return self.pages

    # Run the PageRank algorithm for 20 iterations
    # then pass the values to search
    def pageRank(self):
        MAX_ITERATIONS = 20
        for i in range(0, MAX_ITERATIONS):
            print i
            for page in self.pages:
                weightValue = self.pageRankPage(page)
                page.pageRank = (0.85 * weightValue) + 0.15
                # self
        return None

    def pageRankPage(self, pagerank):
        pr = 0
        for page in self.pages:
            if page.url != pagerank.url:
                for link in page.links:
                    if link == pagerank.url:
                        # (PR1/links1 + PR2/links2 + ... + PRn/linksn)
                        pr += (page.pageRank / len(page.links))

        return pr
