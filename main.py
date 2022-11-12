import re, json
import os
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

def getBatch(batchSize, batchNumber, fileNames, folderPath): 
    #gets a batch of documents from /DEV, if there's no more documents it returns an empty list

    # TODO: Go through the DEV folder and use json.load on all the files so that we can extract the 
    # object and obtain the url, content/tokens and encoding. Then return a list of BatchDocument objects.

    # path = 'DEV'
    # dir_list = sorted(os.listdir(path))
    # dir_list.remove(".DS_Store")
    # print(sorted(dir_list))

    # for folder in dir_list:
    #     print(folder + "-----------------")
    #     sub_path = path + "/" + folder
    #     print(sub_path)
        
    #     files = sorted(os.listdir(sub_path))
    

    #     print(files)

    batchStartPosition = batchSize * (batchNumber-1)
    batchEndPosition = batchStartPosition + batchSize

    print("All: " + str(fileNames))
    print("Getting batch number " + str(batchNumber) + " of size " + str(batchSize))

    batchFileNames = []
    if (batchSize > len(files) and batchNumber == 1):
        batchFileNames = fileNames
    elif (batchSize > len(files) and batchNumber != 1):
        return []
    else:
        batchFileNames = fileNames[batchStartPosition:batchEndPosition]

    batchDocuments = []

    for fileName in batchFileNames:
        
        file = open(folderPath + "/" + fileName)
  
        # returns JSON object as 
        # a dictionary
        data = json.load(file)
        
        url = data["url"]
        content = data["content"]
        encoding = data["encoding"]

        batchDocument = BatchDocument(url, content, encoding)
        batchDocuments.append(batchDocument)
        

    return batchDocuments

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
    # buildIndex()

    files = ['25ab7a717ab32cbdc126dd69dc405451d63b7eb55b21d4384a2847cd802e73ec.json', '358e172599eeb10e5fe57b7befea5113233b334eb13492c4adf694945c69b4d1.json', '59cd2d37c5ff77fd43da46c122c76f1df4b288ab029182c901c11ee01794896a.json', '7ab99efdcd4dfa1251cbc3ef75875758491308240d6e8efc633599b7c094551b.json', '897b5c4dc19303a9a3fffd0d9d49fc831d7b52072b29446f97900ac58fc4181a.json', 'da5aff1b5ca2bad6609f97f11c91fef3a503ded6d9d0f14592793c9391b92fd9.json']
    batch = getBatch(1, 1, files, "DEV/xtune_ics_uci_edu")
    
    print(batch)
