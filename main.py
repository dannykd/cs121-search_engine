


documents = [] #temp for now will store all .jsons



def buildIndex():
    docID = 0
    invertedIndex = dict()
    for document in documents:
        docID+=1
        tokens = tokenize(document)
        tokensWithNoDuplicate = set(tokens)
        #build posting for document
        docPosting = None #temp create posting (docid, frequency of token in that document)
        for token in tokensWithNoDuplicate:
            if token in invertedIndex.keys():
                invertedIndex[token].append(docPosting)
            else:
                invertedIndex[token] = []
    return invertedIndex
        

#todo: associate docIDs with urls


        

def tokenize():
    #return a list of tokens (no duplicates)
    return 0


class Posting:
    def __init__(self, docid, tfidf):
        self.docid = docid # int n, will map to file in different dict
        self.tfidf = tfidf # frequency or count of token in given document