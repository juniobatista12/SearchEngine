import json
import re
from Parser import Parser

class SearchEngine:
    def __init__(self):
        file = open("Crawler.json","r")
        self.data = json.load(file)
        self.title = {}
        self.parser = Parser()
    
    # retorna ocorrencias da palavra {word}
    def Search(self,word):
        word = word.lower()
        sites = self.data.get(word)
        pages = {}.keys()
        extracts = {}
        if sites != None:
            pages = sites["pages"].keys()
            for i in pages:
                self.title[i] = sites["pages"][i]["title"]
                if(extracts.get(i) == None):
                    extracts[i] = []
                for j in sites["pages"][i]["extracts"]:
                    extracts[i].append(j[0])

        return pages,extracts,set([word])

    def And(self,word1,word2):
        urls = word1[0] & word2[0]
        words = word1[2].union(word2[2])
        extracts1 = word1[1]
        extracts2 = word2[1]
        extracts = {}
        for i in urls:
            page1 = set(extracts1[i])
            page2 = set(extracts2[i])
            extracts[i] = list(page1.intersection(page2))

        return urls,extracts,words

    def Or(self,word1,word2):
        urls = word1[0] | word2[0]
        words = word1[2].union(word2[2])
        extracts1 = word1[1]
        extracts2 = word2[1]
        extracts = {}
        for i in urls:
            page1 = extracts1.get(i)
            if(page1 == None):
                page1 = []
            page2 = extracts2.get(i)
            if(page2 == None):
                page2 = []
            page1 = set(page1)
            page2 = set(page2)
            extracts[i] = list(page1.union(page2))
            
        return urls,extracts,words


    def Not(self,word1,word2):
        urls = word1[0] - word2[0]
        words = word1[2].difference(word2[2])
        extracts1 = word1[1]
        extracts2 = word2[1]
        extracts = {}
        for i in urls:
            page1 = extracts1.get(i)
            if(page1 == None):
                page1 = []
            page2 = extracts2.get(i)
            if(page2 == None):
                page2 = []
            page1 = set(page1)
            page2 = set(page2)
            extracts[i] = list(page1.difference(page2))
            # print(i)
            # print(page1)
            # print(page2)
            # print(extracts[i])

        return urls,extracts,words

    # busca por string
    def String(self,string):
        words = string.split(" ")
        search = 0
        urls = set()
        extracts_to_return = {}
        if len(words) == 1:
            return self.Search(words[0])
        else:
            search = self.Search(words[0])
            for i in range(1,len(words)):
                search = self.And(search,self.Search(words[i]))
            if search == set():
                return set(),{},set([string])
            else:
                pages = self.data.get(words[0])
                if(pages == None):
                    return set(),{},set([string])
                else:
                    pages = pages["pages"]
                    for i in search[0]:
                        self.title[i] = self.data.get(words[0])["pages"][i]["title"]
                        if(extracts_to_return.get(i) == None):
                            extracts_to_return[i] = []
                        found = False
                        extracts = pages[i]["extracts"]
                        for j in extracts:
                            aux = j[0]
                            aux = re.sub("[^A-Za-z0-9-ÁÇÉÍÓÚÀÈÌÒÙÂÊÎÔÛÃÕËÜÏÖÑÝåáçéíóúàèìòùâêîôûãõëüïöñýÿ ]","",aux)
                            aux_map = aux.maketrans('¿¿¿¿¿ÁÇÉÍÓÚÀÈÌÒÙÂÊÎÔÛÃÕËÜÏÖÑÝåáçéíóúàèìòùâêîôûãõëüïöñýÿ',
                                                    'SZszYACEIOUAEIOUAEIOUAOEUIONYaaceiouaeiouaeiouaoeuionyy')
                            aux = aux.translate(aux_map)
                            aux = re.sub("\t"," ",aux)
                            aux = re.sub("\s+"," ",aux)
                            aux = aux.strip()
                            if(aux.lower().find(string) == -1):
                                continue
                            else:
                                if(not found):
                                    urls.add(i)
                                extracts_to_return[i].append(j[0])
                                found = True
                        if found == False:
                            extracts_to_return.pop(i)
                    return urls,extracts_to_return,set([string])

    # retorna resultados da busca apos operacoes
    def Process(self, search_terms):
        search_results = []

        for w in search_terms:
            if w not in ["AND", "OR", "-"]:
                if w.startswith("\""): 
                    search_results.append(self.String(w[1:-1]))
                else:
                    search_results.append(self.Search(w))
            else:
                i1 = search_results.pop()
                i2 = search_results.pop()
                if w == "AND":
                    search_results.append(self.And(i2, i1))
                elif w == "OR":
                    search_results.append(self.Or(i2, i1))
                elif w == "-":
                    search_results.append(self.Not(i2, i1))

        return search_results[0]

    # metodo a ser utilizado pela pagina web do buscador
    def PerformSearch(self, query):
        ls = self.parser.parse(query)
        urls, response, words = self.Process(ls)

        result = {
            "query": list(words),
            "response": []
        }
        for k,v in response.items():
            result["response"].append({
                "url": k,
                "title": self.title[k],
                "text": " ".join(v)
            })

        return result

if __name__ == "__main__":
    SE = SearchEngine()
    print(SE.PerformSearch(input("Google it: ")))

    # print(SE.And(SE.Search("lucero"),SE.Search("jorge")), end="\n\n")
    # print(SE.Or(SE.Search("lucero"),SE.Search("jorge")), end="\n\n")
    # print(SE.Not(SE.Search("lucero"),SE.Search("jorge")), end="\n\n")
    #ls = SE.parser.parse("lucero -ausdgshasudi")
    #print(ls)
    #print(SE.Process(ls))
    # print(SE.String("jorge lucero"), end="\n\n")
    # print(SE.String("lucero jorge"), end="\n\n")
    # print(SE.String("ughsdughsa"))
