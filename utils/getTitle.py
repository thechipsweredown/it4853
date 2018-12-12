from pyvi import ViTokenizer

data = []
stop_word = []

def createSuggest() :
    with open('stopword.txt') as f1:
        for line in f1:
            stop_word.append(line.rstrip("\n\r"))      
    with open('../data.txt') as f:
        for line in f:
            arr = ViTokenizer.tokenize(line.rstrip("\n\r")).replace("?","").replace("..."," ").replace('"'," ").replace(",","").split(" ")
            for a in arr:
                if a not in stop_word and a.replace("_"," ").strip().lower() not in data and len(a) > 4:
                    data.append(a.replace("_"," ").lower())
    count = 0                
    with open('datav3.json', 'w') as f3:
        for a in data:
            f3.write('{"index":{"_index":"title","_id":'+str(count)+'}'+'}')
            f3.write("\n")
            f3.write('{"suggest" :"'+a+'"}')
            f3.write("\n")
            count += 1
createSuggest()