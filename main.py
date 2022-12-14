import re, json
import os
from bs4 import BeautifulSoup
import time
import math
import orjson


# BatchDocument takes in a url, the content, and the encoding for any specific json file given to us in the DEV folder
# given the content, BatchDocument will tokenize the content and save it into a variable, tokens
class BatchDocument:
    def __init__(self, url, content, encoding):
        self.url = url
        self.encoding = encoding
        self.tokens = []
        # create beautiful soup object to parse the given content string and find the body tag and the content within it
        soup = BeautifulSoup(content, "html.parser")
        textContent = ""
        for tag in soup.find_all('body'):
            textContent += " " + tag.getText()
        tokens = tokenize(textContent) # return the tokenized textContent
        for token in tokens: #convert tokens to lower case
            self.tokens.append(token.lower())
    
class Posting:
    def __init__(self, docid, tfidf):
        self.docid = docid # int n, will map to file in different dict
        self.tfidf = tfidf # frequency or count of token in given document
        self.fields = []

    def to_dict(self):
        return dict(docid=self.docid, tfidf=self.tfidf, fields=self.fields)



def getBatch(batchSize, batchNumber, fileNames, folderPath): 
    #gets a batch of documents from /DEV, if there's no more documents it returns an empty list

    start_time = time.time()


    batchStartPosition = batchSize * (batchNumber-1)
    batchEndPosition = batchStartPosition + batchSize

    batchFileNames = []
    
    # If batch size exceeds the number of files and it's the first batch, then return all files
    if (batchSize > len(fileNames) and batchNumber == 1):
        batchFileNames = fileNames
    # If batch size exceeds the number of files, then there can only be one batch. Return [] if batch number exceeds 1.
    elif (batchSize > len(fileNames) and batchNumber != 1):
        return []
    # Gets the filenames for the current batch
    else:
        batchFileNames = fileNames[batchStartPosition:batchEndPosition]

    batchDocuments = []

    if batchFileNames:
        print("Getting batch number " + str(batchNumber) + " of size " + str(batchSize) + " for " + folderPath)

    for fileName in batchFileNames:
        
        file = open(folderPath + "/" + fileName)
        data = json.load(file)
        
        url = data["url"]
        content = data["content"]
        encoding = data["encoding"]

        batchDocument = BatchDocument(url, content, encoding)
        batchDocuments.append(batchDocument)
        
    print("--- %s seconds ---" % (time.time() - start_time))

    return batchDocuments

def sortAndWriteToDisk(index: dict, fileName):
    print("WRITING INDEX " + str(index))

    if os.path.isfile(fileName):
        indexFile = open(fileName, "r")
        existingData:dict = json.load(indexFile)
        indexFile.close()

        for token in existingData.keys():
            if token in index.keys():
                existingData[token] = existingData[token] + index[token] #combine the postings array of the existing index with new index
                del index[token] #delete the token from the new index since we combined it already

        existingData.update(index) #update the existing array to add the new keys (tokens) from new array

        with open(fileName,'w+') as diskFile: #opens file or creates file or rewrites file 
            diskFile.write(json.dumps(existingData, sort_keys=True))

        return None


    with open(fileName,'w+') as diskFile: #opens file or creates file or rewrites file 
      diskFile.write(json.dumps(index, sort_keys=True))
    return None

def mergeDisksIntoDict():
    mergedIndex = dict()
    indexesOnDisk = getFilesInFolder('indexes')
    for index in indexesOnDisk:
        with open(f'indexes/{index}' , 'r+') as indexFile:
            currentIndex = json.load(indexFile)
            mergedIndex.update(currentIndex)
    
    sortAndWriteToDisk(mergedIndex, 'indexes/final.txt' )
    return mergedIndex
            
def buildDfDict():
    numDocs = 0
    dfDict = dict() #token, number of docs that token appears in
    folders = getFolders("DEV")
    batchSize = 500
    for folder in folders:
        fileNames = getFilesInFolder(folder)
        currBatch = 1
        while True:
            documentsInBatch = getBatch(batchSize, currBatch, fileNames, folder)
            if not documentsInBatch:
                break #end the loop if there's no more documents to process
            currBatch +=1
            
            for document in documentsInBatch:
                numDocs += 1
                for token in set(document.tokens):
                    if token in dfDict.keys():
                        dfDict[token] +=1
                    else:
                        dfDict[token] = 1
    
    return (dfDict,numDocs)



def buildIndex():
    docID = 0
    invertedIndex = dict()
    IDToUrl = dict()
    folders = getFolders("DEV")
    batchFileNumber = 0
    batchSize = 500
    dfDict, numOfDocs = buildDfDict()

    invertedIndex = {
        "a":dict(),
        "b":dict(),
        "c":dict(),
        "d":dict(),
        "e":dict(),
        "f":dict(),
        "g":dict(),
        "h":dict(),
        "i":dict(),
        "j":dict(),
        "k":dict(),
        "l":dict(),
        "m":dict(),
        "n":dict(),
        "o":dict(),
        "p":dict(),
        "q":dict(),
        "r":dict(),
        "s":dict(),
        "t":dict(),
        "u":dict(),
        "v":dict(),
        "w":dict(),
        "x":dict(),
        "y":dict(),
        "z":dict(),
        "0":dict(),
        "1":dict(),
        "2":dict(),
        "3":dict(),
        "4":dict(),
        "5":dict(),
        "6":dict(),
        "7":dict(),
        "8":dict(),
        "9":dict(),
    }

    print("STARTING BUILD INDEX")

    for folder in folders:
        fileNames = getFilesInFolder(folder)
        currBatch = 1
        while True:
            documentsInBatch = getBatch(batchSize, currBatch, fileNames, folder)
            if not documentsInBatch:
                break #end the loop if there's no more documents to process
            currBatch +=1
            
            for document in documentsInBatch:
                
                docID+=1
                IDToUrl[docID] = document.url
                tokensWithNoDuplicate = set(document.tokens)
                for token in tokensWithNoDuplicate: 
                    tfidfForDoc = (1 + math.log(document.tokens.count(token.lower()),10)) * math.log((numOfDocs/dfDict[token]),10)
                    #calculate td-idf, i.e, (1+log(count of token in doc)) * log(num of documents / num of doc term occurs in)
                    #prolly write a function to get the total number of docs and number of document term occurs in
                    #log base 10 btw
                    #tfidfForDoc = 0
                    # if token[0].lower() in invertedIndex.keys():
                    docPosting = Posting(docID, tfidfForDoc).to_dict()

                    if token[0].lower() not in invertedIndex.keys():
                        invertedIndex[token[0].lower()] = {}
                    
                    if token.lower() in invertedIndex[token[0].lower()]:
                        invertedIndex[token[0].lower()][token.lower()].append(docPosting)
                    else:
                        invertedIndex[token[0].lower()][token.lower()] = [docPosting]

                    # else:
                    #     invertedIndex[token[0].lower()] = dict()
                    #     invertedIndex[token[0].lower()][token.lower()] = [Posting(docID, tfidfForDoc).to_dict()]

                  
            batchFileNumber += 1 
            
        for k, v in invertedIndex.items():
            fileName = f'indexes/disk-{k}.txt'
            sortAndWriteToDisk(v, fileName)
        invertedIndex.clear()


          
    sortAndWriteToDisk(IDToUrl, "mappings/urlMappings.txt") #put the url mappings into memory
    

    mergedIndex = mergeDisksIntoDict() # merge index back into one dictionary mergedIndex
    print(f'Number of Documents : {docID}')
    print(f'Number of Unique Tokens : {len(mergedIndex.keys())}')

    # write mergedIndex to an output file to read file size on disk
    
    # write to mergedFileName
    fileSize = os.path.getsize('indexes/final.txt')
    print(f'Size of Index on Disk : {fileSize}')
    return None
        

#todo: associate docIDs with urls   


    
def tokenize(text):
    #return a list of tokens (no duplicates)
    return re.findall('[a-zA-Z0-9]+', text)

def getFolders(parentFolder):
    subfolders = sorted(os.listdir(parentFolder))
    if (".DS_Store") in subfolders:
        subfolders.remove(".DS_Store")
    # print(sorted(dir_list))
    subFoldersWithParentPath = [(parentFolder + "/" + i) for i in subfolders]
    return sorted(subFoldersWithParentPath)

def getFilesInFolder(folderName):
    files = sorted(os.listdir(folderName))
    return files

def search(query):
    
    matchedDocs = []
    
    docScore = dict() #key will be a docID, value is the SCORE of that document
   
    docScoreHeap = [] #heap to try to optimize, rather than sorting a dictionary
    #i.e, if the value is len(queryTokens) then that document contains atleast 1 of every token in the query
    queryTokens = tokenize(query)
    for token in queryTokens:
        #find the disk file that has that token
        #ex. json.loads(disk-5.txt)
        with open(f'indexes/disk-{token[0].lower()}.txt' , 'r+') as indexFile:
            index = orjson.loads(indexFile.read())
            

        if token in index.keys():
            tokenPostings = index[token]
            for posting in tokenPostings:
                if posting["docid"] in docScore.keys():
                    docScore[posting["docid"]] += posting['tfidf']
                else:
                    docScore[posting["docid"]] = posting['tfidf']
        
    
    # #sort by score/sum of weights for that docid, return matched docs
    # sort by highest to lowest docscore dict

    docScoreSorted = sorted(docScore.items(), key=lambda x:x[1], reverse=True)
 
    for docScore in docScoreSorted[:5]:
        matchedDocs.append(docScore[0])
    return matchedDocs

def search_from_client(query:str):
    matchedDocs = []
    
    docScore = dict() #key will be a docID, value is the SCORE of that document
    #i.e, if the value is len(queryTokens) then that document contains atleast 1 of every token in the query
    queryTokens = tokenize(query)
    for token in queryTokens:
        #find the disk file that has that token
        #ex. json.loads(disk-5.txt)
        with open(f'indexes/disk-{token[0].lower()}.txt' , 'r+') as indexFile:
            index = orjson.loads(indexFile.read())

        if token in index.keys():
            tokenPostings = index[token]
            for posting in tokenPostings:
                if posting["docid"] in docScore.keys():
                    docScore[posting["docid"]] += posting['tfidf']
                else:
                    docScore[posting["docid"]] = posting['tfidf']
        
    
    # #sort by score/sum of weights for that docid, return matched docs
    # sort by highest to lowest docscore dict
    docScoreSorted = sorted(docScore.items(), key=lambda x:x[1], reverse=True)
    
    urlMappings = getUrlMappingFromDisk()
    for docScore in docScoreSorted[:5]:
        matchedDocs.append(urlMappings[str(docScore[0])])
    return matchedDocs


def getUrlMappingFromDisk():
    with open(f'mappings/urlMappings.txt' , 'r+') as mappingFile:
        urlMappings = json.load(mappingFile)

    return urlMappings
    


        
 


if __name__ == '__main__':
    # start = time.time()
    #buildIndex()
    # print("--- FINISHED BUILDING INDICES IN %s seconds ---" % (time.time() - start))
    #print("--- FINISHED BUILDING INDICES IN %s minutes ---" % (time.time() - start / 60))

    querys = [
        "cristina lopes",
        "machine learning",
        "ACM",
        "master of software engineering",
        "software uci computer",
        "testing hopefully",
        "mark baldwin",
        "informatics major",
        "computer science",
        "undergraduate degree",
        "ICS School of ",
        "search engine", 
        "health",
        "statistics math",
        "software engineering",
        "python programming",
        "java programming",
        "javascript tutorial",
        "where is the bathroom",
        "irvine company apartments",
        "university of california irvine"
    ]

    for query in querys:
        print()
        print(query)
        start = time.time()
        
        matchedDocs = search(query.lower())
        urlMappings = getUrlMappingFromDisk()
        for docid in matchedDocs:
            print(f'{urlMappings[str(docid)]}')
        print("--- FINISHED QUERYING IN %s seconds ---" % (time.time() - start))

    # files = ['25ab7a717ab32cbdc126dd69dc405451d63b7eb55b21d4384a2847cd802e73ec.json', '358e172599eeb10e5fe57b7befea5113233b334eb13492c4adf694945c69b4d1.json', '59cd2d37c5ff77fd43da46c122c76f1df4b288ab029182c901c11ee01794896a.json', '7ab99efdcd4dfa1251cbc3ef75875758491308240d6e8efc633599b7c094551b.json', '897b5c4dc19303a9a3fffd0d9d49fc831d7b52072b29446f97900ac58fc4181a.json', 'da5aff1b5ca2bad6609f97f11c91fef3a503ded6d9d0f14592793c9391b92fd9.json']
    # batch = getBatch(10, 1, files, "DEV/xtune_ics_uci_edu")
    
    # for i in batch:
    #     print(i.url)



    # folders = getFolders("DEV")
    # print(folders)
    # for folder in folders:
    #     fileNames = getFilesInFolder(folder)
        
    #     batch = getBatch(100, 1, fileNames, folder)
    #     # print(batch)
