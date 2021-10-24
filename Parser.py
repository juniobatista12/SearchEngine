class Parser:
    def __init__(self):
        pass

    # transforma operacao da forma infixa para posfixa
    def get_query_terms(self, query):
        tokens = query.split(" ")

        operators = []
        output = []
        str_flag = False
        str_list = ""

        for t in tokens:
            if str_flag and not t == "\"":
                str_list += t + " "
                continue
                
            if t == "\"":
                if not str_flag:
                    str_list = "\""
                else:
                    # conserta parenteses
                    str_list = str_list.replace(" ( ", " (")
                    str_list = str_list.replace(" ) ", ") ")
                    output.append(str_list.strip().lower() + "\"")
                str_flag = not str_flag
            elif t == "(":
                operators.append(t)
            elif t == ")":
                while(len(operators) != 0 and operators[-1] != "("):
                    output.append(operators.pop())
                operators.pop()
            elif t in ["AND", "OR", "-"]:
                while(len(operators) != 0 and operators[-1] not in ["(", ")"]):
                    output.append(operators.pop())
                operators.append(t)
            else:
                output.append(t)

        while(len(operators) != 0):
            output.append(operators.pop())

        return output

    # separa palavras e faz transformacoes para uniformizar operadores
    def transform_query(self, query):
        # tudo minusculo
        query = query.lower()

        # separa as aspas
        query = query.replace("\"", " \" ")
        # separa o hifen
        query = query.replace(" -", " - ")

        # operadores AND, OR sao maiusculos
        query = query.replace(" and ", " AND ")
        query = query.replace(" or ", " OR ")

        # adiciona espacos antes e depois de parenteses
        query = query.replace("(", " ( ")
        query = query.replace(")", " ) ")

        # remove espacos duplicados
        query = " ".join(query.split())

        # transforma espacos comuns em "AND"
        new_query = []
        itr = query.split(" ")
        str_flag = False
        for k in range(len(itr)):
            new_query.append(itr[k])

            if itr[k] not in ["AND", "OR", "-", "(", "\""]:
                if (not str_flag and k+1 < len(itr) 
                    and itr[k+1] not in ["AND", "OR", "-", ")"]):
                    new_query.append("AND")
            elif itr[k] == "\"":
                if (str_flag and k+1 < len(itr) 
                    and itr[k+1] not in ["AND", "OR", "-", ")"]):
                    new_query.append("AND")
                str_flag = not str_flag
            

        return " ".join(new_query)


    def parse(self, query):
        # remove acentos
        aux_map = query.maketrans("¿¿¿¿¿ÁÇÉÍÓÚÀÈÌÒÙÂÊÎÔÛÃÕËÜÏÖÑÝåáçéíóúàèìòùâêîôûãõëüïöñýÿ",
                                  "SZszYACEIOUAEIOUAEIOUAOEUIONYaaceiouaeiouaeiouaoeuionyy")
        query = query.translate(aux_map)
        query = self.transform_query(query)
        return self.get_query_terms(query)


if __name__ == "__main__":
    query = "unb (\"universidade de brasilia\")"
    p = Parser()
    print(p.parse(query))