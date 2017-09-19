import math
from heapq import *
import string

stopwords = open("stopwords","r")
stopwords = stopwords.read().splitlines()

arq = open("cf74")
arq1 = open("cf75")
arq2 = open("cf76")
arq3 = open("cf77")
arq4 = open("cf78")
arq5 = open("cf79")

txt = arq.readlines()
txt += arq1.readlines() 
txt += arq2.readlines()
txt += arq3.readlines()
txt += arq4.readlines()
txt += arq5.readlines()


print("[Gerando Lista Invertida...]")
docs = []
words = []

interestedTags = ["TI", "MJ" , "MN" , "AB" , "EX"]          #partes com informações interessantes do texto

for linha in txt:
    linha = linha.strip("\n").split(" ")
    if( linha[0] != ""):
        tag = linha[0]

    if( tag in interestedTags ):
        words += linha
    elif( tag == "PN" and words != []):
        docs.append( [k.strip(string.punctuation).lower() for k in words if( k != "")])
        words = []

docs.append([k.strip(string.punctuation).lower() for k in words if( k != "")])
words = []


hashWords = dict({})

i = 1                                                           #i é o numero do documento atual que está sendo verificado

for doc in docs:                                                #para cada documento da lista de documentos
    for palavra in doc:                                         #para cada palavra no documento atual
        if (palavra not in stopwords and palavra not in interestedTags and palavra.isalpha()):
            if( not palavra in hashWords):                          #se a palavra não estiver no Hash ainda
                hashWords[palavra] = [(i , 1)]                      #adiciona a palavra no hash por meio de uma tupla com documento i e frequencia 1
            else:                                                   #senão, a palavra já estiver no Hash
                achou = False                                       #não achou
                lista = hashWords[palavra]                          #lista auxiliar recebe a lista da palavra atual no Hash
                for k in range( len(lista)):                        #para cada tupla na lista
                    if( lista[k][0] == i):                          #se o primeiro elemento da tupla atual for igual ao i, a palavra já apareceu no documento antes
                        lista[k] = ( lista[k][0] , lista[k][1] + 1) #então substituimos essa tupla por uma tupla com o mesmo i e a frequencia da tupla anterior +1
                        achou = True                                #achou
                        break                                       #fim
                if( not achou ):                                    #se a palavra ainda não foi achada, ela ainda não tinha aparecido no documento antes, então
                    lista.append( (i , 1))                          #adicionamos na lista auxiliar uma tupla com o i atual e frquencia 1
                hashWords[palavra] = lista                          #o Hash da palavra verificada recebe a lista auxiliar como lista definitiva
    i+=1                                                        #incrementa i, pois veremos o próximo documento


ndocs = i
hashIdf = dict({})
hashNorma = dict({})

#Para cada elemento no Hash de palavras, calcula o ln de ndocs sobre o tamanho da 
#lista invertida da palavra( em qtos documentos ela aparece)

for x in hashWords:
    hashIdf[x] = math.log( ndocs/len( hashWords[x]))

def idf( word ):
    return hashIdf[word]

def tf( doc , word):
    lista = hashWords[word]
    for x in lista:
        if( x[0] == doc):
            return x[1]
    
    return 0

def weight( doc , word):
    return tf( doc , word ) * idf( word )

def norma( doc ):
    if( doc in hashNorma):
        return hashNorma[doc]
    else:
        result = 0
        for word in hashWords:
            result += (weight( doc , word) ** 2)
        
        hashNorma[doc] = math.sqrt( result )
        return hashNorma[doc]

print("[Pré-calculando normas...]")
normas = open("normas.dat")
normas = normas.readlines()

for i in range( len(normas)):
    hashNorma[i+1] = float( normas[i])


def filterHash( query ): #Filtra o hash para palavras que tem na consulta
    result = dict({})
    query = query.split()
    query = [x.strip(string.punctuation) for x in query ]

    for word in query:
        if( word in hashWords):
            result[word] = hashWords[word]
    
    
    return result

def TermoaTermo( query ):
    #print("[Filtrando Lista Invertida...]")
    hashQuery = filterHash( query )
    
    acums = [0 for x in range( ndocs )]

    #print("[Calculando acumuladores...]")
    for term in hashQuery:
        for doc,freq in hashQuery[term]:
            acums[doc-1] += freq * (idf( term )**2)

    #Dividindo tudo pela norma
    for i in range( len(acums)):
        if( acums[i] != 0 ):
            acums[i] = acums[i]/(norma(i + 1))

    #associando acumulador ao respectivo documento
    for i in range( len(acums)):
        acums[i] = ( acums[i] , i + 1)
    
    topk = []
    k = 200
    #print("[Filtrando os topk resultados...]")
    for x in acums:
        if( len(topk) < k and x[0] > 0.0):
            heappush( topk , x)
        elif( topk and x > topk[0]):
            heappop( topk )
            heappush( topk , x)
    
    results = []
    for i in range(len( topk)):
        results = [heappop(topk)] + results

    return results

def precisao (resultadoIdeal, meuResultado):
    numIguais = 0
    conta = 1
    precisoes = []
    prec = 0
    for elemento in meuResultado:
        if elemento in resultadoIdeal:
            numIguais += 1
        prec = numIguais / conta
        precisoes.append(prec)
        conta += 1
    return precisoes

#def revocacao (resultadoIdeal, meuResultado):

def MAPi (resultadoIdeal, meuResultado):
    somaPrec = 0
    prec = precisao(resultadoIdeal,meuResultado)
    for i in prec:
        somaPrec += i
    return somaPrec/len(meuResultado)

#PEGA AS CONSULTAS
arq = open("cfquery")

txt = arq.readlines()
i = 0

insterestedTags = ["QU", "RD"]
query = []
relevant = []

hashQueries = dict({})

for linha in txt:
    linha = linha.strip("\n" + string.punctuation).split(" ")
    if (linha[0] != ""):
        tag = linha[0]

    if (tag == "QU"):
        query += linha

    if (tag == "RD"):
        relevant += linha

    if (tag == "QN" and query):
        query = " ".join([x for x in query[1:] if (x != "")])
        relevant = [x for x in relevant[1:] if (x != "")]
        relevant = [relevant[i] for i in range(len(relevant)) if (i % 2 == 0)]

        # print("Texto da Consulta: \n" , query)
        # print("Relevantes: \n" , relevant)

        hashQueries[query] = relevant
        query = []
        relevant = []

query = " ".join([x for x in query[1:] if (x != "")])
relevant = [x for x in relevant[1:] if (x != "")]
relevant = [relevant[i] for i in range(len(relevant)) if (i % 2 == 0)]
hashQueries[query] = relevant

# for k in hashQueries:
#     print(k, " -> ", hashQueries[k])
#FIM DO PEGA AS CONSULTAS

guardaMAPs = 0
meuResult = []
resultIdeal = []

for k in hashQueries:
    Result = TermoaTermo(k)
    for i in Result:
        meuResult.append(i[1])
    for i in hashQueries[k]:
        resultIdeal.append(int(i))
    print("\n\nConsulta: " + k)
    print("Meus resultados: ")
    print(meuResult)
    print("Resultados ótimos: ")
    print(resultIdeal)
    map = MAPi(resultIdeal,meuResult)
    print("MAP dessa consulta = " + str(map))
    guardaMAPs += map
    meuResult = []
    resultIdeal = []

mediaMAPs = guardaMAPs/len(hashQueries)
print("\nMAP geral = " + str(mediaMAPs))



# while True:
#     query = input("Digite aqui para fazer sua busca:\n")
#     query = query.split(" ")
#
#     query = [ word.strip(".,:)(?!;-").lower() for word in query]
#
#     meus = TermoaTermo( query )


