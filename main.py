





def getBatch(): 
    #gets a batch of documents from /DEV, if there's no more documents it returns an empty list

    return None

def sortAndWriteToDisk(index, fileName):
    #adds the index to a .txt file
    return None
    
def buildIndex():
    docID = 0
    invertedIndex = dict()
    while True:
        documentsInBatch = getBatch()
        if not documentsInBatch:
            break #end the loop if there's no more documents to process
        for document in documentsInBatch:
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
            
        fileName = "disk.txt"
        sortAndWriteToDisk(invertedIndex, fileName)
        invertedIndex.clear()

    return None
        

#todo: associate docIDs with urls   


        

def tokenize():
    #return a list of tokens (no duplicates)
    return 0


class Posting:
    def __init__(self, docid, tfidf):
        self.docid = docid # int n, will map to file in different dict
        self.tfidf = tfidf # frequency or count of token in given document