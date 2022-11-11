class Posting:
    def __init__(self, docid, tfidf):
        self.docid = docid # int n, will map to file in different dict
        self.tfidf = tfidf # frequency or count of token in given document
        self.fields = []

def getBatch(): 
    #gets a batch of documents from /DEV, if there's no more documents it returns an empty list

    return None

def sortAndWriteToDisk(index, fileName):
    #adds the index to a .txt file
    return None
    
def buildIndex():
    docID = 0
    invertedIndex = dict()
    batch = 0
    while True:
        documentsInBatch = getBatch()
        if not documentsInBatch:
            break #end the loop if there's no more documents to process
        batch +=1
        for document in documentsInBatch:
            docID+=1
            tokens = tokenize(document)
            tokensWithNoDuplicate = set(tokens)
            for token in tokensWithNoDuplicate:
                if token in invertedIndex.keys():
                    docPosting = Posting(docID, tokens.count(token), [])
                    invertedIndex[token].append(docPosting)
                else:
                    invertedIndex[token] = []
            
        fileName = f'indexes/disk-{batch}.txt'
        sortAndWriteToDisk(invertedIndex, fileName)
        invertedIndex.clear()

    # merge index back into one dictionary mergedIndex
    mergedIndex = None
    print(f'Number of Documents : {docID}')
    print(f'Number of Unique Tokens : {len(mergedIndex.keys())}')

    # write mergedIndex to an output file to read file size on disk
    mergedFileName = 'indexes/final.txt'
    # write to mergedFileName

    #print(f'Size of Index on Disk : FIND FUNCTION TO DO THIS') -- reading size of mergedFileName
    return None
        

#todo: associate docIDs with urls   


    
def tokenize():
    #return a list of tokens (no duplicates)
    return re.findall('[a-zA-Z0-9]+', text)


if __name__ == '__main__':
    buildIndex()