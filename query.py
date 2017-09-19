arq = open("cfquery")

txt = arq.readlines()
i = 0

insterestedTags = ["QU" , "RD"]
query = []
relevant = []

hashQueries = dict({})

for linha in txt:
    linha = linha.strip("\n").split(" ")
    if( linha[0] != ""):
        tag = linha[0]

    if( tag == "QU"):
        query += linha
    
    if( tag == "RD"):
        relevant += linha
    
    if( tag == "QN" and query):

        query = " ".join([ x for x in query[1:] if( x != "")])
        relevant = [x for x in relevant[1:] if(x != "")]
        relevant = [relevant[i] for i in range(len(relevant)) if( i % 2 == 0)]

        # print("Texto da Consulta: \n" , query)
        # print("Relevantes: \n" , relevant)

        hashQueries[query] = relevant
        query = []
        relevant = []

query = " ".join([ x for x in query[1:] if( x != "")])
relevant = [x for x in relevant[1:] if(x != "")]
relevant = [relevant[i] for i in range(len(relevant)) if( i % 2 == 0)]
hashQueries[query] = relevant

for k in hashQueries:
    print( k , " -> " , hashQueries[k])
