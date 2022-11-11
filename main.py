import re, json
from bs4 import BeautifulSoup

# BatchDocument takes in a url, the content, and the encoding for any specific json file given to us in the DEV folder
# given the content, BatchDocument will tokenize the content and save it into a variable, tokens
class BatchDocument:
    def __init__(self, url, content, encoding):
        self.url = url
        self.encoding = encoding
        # create beautiful soup object to parse the given content string and find the body tag and the content within it
        soup = BeautifulSoup(content, "html.parser")
        textContent = ""
        for tag in soup.find_all('body'):
            textContent += " " + tag.getText()
        self.tokens = tokenize(textContent) # return the tokenized textContent
    
class Posting:
    def __init__(self, docid, tfidf):
        self.docid = docid # int n, will map to file in different dict
        self.tfidf = tfidf # frequency or count of token in given document
        self.fields = []

def getBatch(batchSize): 
    #gets a batch of documents from /DEV, if there's no more documents it returns an empty list

    # TODO: Go through the DEV folder and use json.load on all the files so that we can extract the 
    # object and obtain the url, content/tokens and encoding. Then return a list of BatchDocument objects.
    return None

def sortAndWriteToDisk(index, fileName):
    #adds the index to a .txt file
    return None
    
def buildIndex():
    docID = 0
    invertedIndex = dict()
    batch = 0
    while True:
        # TODO: add a constant batch size
        # TODO: be able to call documentsInBatch[i].tokens to get the tokens
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


    
def tokenize(text):
    #return a list of tokens (no duplicates)
    return re.findall('[a-zA-Z0-9]+', text)


if __name__ == '__main__':
    buildIndex()