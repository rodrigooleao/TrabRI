import math
from heapq import *
import string
import math

def idf(word):
    return hashIdf[word]

def tf(doc, word):
    lista = hashWords[word]
    for x in lista:
        if (x[0] == doc):
            return x[1]
    return 0

def weight(doc, word):
    return tf(doc, word) * idf(word)

def norma(doc):
    if (doc in hashNorma):
        return hashNorma[doc]
    else:
        result = 0
        for word in hashWords:
            result += (weight(doc, word) ** 2)

        hashNorma[doc] = math.sqrt(result)
        return hashNorma[doc]

def insertionSort(alist):
   for index in range(1,len(alist)):

     currentvalue = alist[index]
     position = index

     while position>0 and alist[position-1]<currentvalue:
         alist[position]=alist[position-1]
         position = position-1

     alist[position]=currentvalue

def TermoaTermo(query):
    # print("[Filtrando Lista Invertida...]")
    hashQuery = filterHash(query)

    acums = [0 for x in range(ndocs)]

    # print("[Calculando acumuladores...]")
    for term in hashQuery:
        for doc, freq in hashQuery[term]:
            acums[doc - 1] += freq * (idf(term) ** 2)

    # Dividindo tudo pela norma
    for i in range(len(acums)):
        if (acums[i] != 0):
            acums[i] = acums[i] / (norma(i + 1))

    # associando acumulador ao respectivo documento
    for i in range(len(acums)):
        acums[i] = (acums[i], i + 1)

    topk = []
    k = len(acums)

    # print("[Filtrando os topk resultados...]")
    for x in acums:
        if (len(topk) < k and x[0] > 0.1):
            heappush(topk, x)
        elif (topk and x > topk[0]):
            heappop(topk)
            heappush(topk, x)

    results = []
    for i in range(len(topk)):
        results = [heappop(topk)] + results

    return results

def filterHash(query):  # Filtra o hash para palavras que tem na consulta
    result = dict({})
    query = query.split()
    query = [x.strip(string.punctuation) for x in query]
    query = [x for x in query if x not in stopwords]

    for word in query:
        if (word in hashWords):
            result[word] = hashWords[word]

    return result

def precisao(resultadoIdeal, meuResultado):
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

# def revocacao (resultadoIdeal, meuResultado):

def MAPi(resultadoIdeal, meuResultado):
    somaPrec = 0
    prec = precisao(resultadoIdeal, meuResultado)
    for i in prec:
        somaPrec += i
    return somaPrec / len(meuResultado)

def moda(lista):
    hashinho = dict({0: 0,
                     1: 0,
                     2: 0,
                     3: 0})

    for elemento in lista:
        hashinho[elemento] += 1
    maior = -1
    for elemento in hashinho:
        if hashinho[elemento] > maior:
            maior = elemento
        elif hashinho[elemento] == maior:
            if hashinho[maior] < hashinho[elemento]:
                maior = elemento
    return maior

def calculaCG(lista):
    aux = [lista[0]]
    for i in range(1,len(lista)):
        aux.append(lista[i] + lista[i-1])
    return aux

def calculaDCG(lista):
    aux = lista[0]
    for i in range(1,len(lista)):
        aux = lista[i]/math.log(i+1,2) + aux
    return aux

def calculaNDCG(meu,ideal):
    if ideal > 0:
        return meu/ideal
    else:
        return 0

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

interestedTags = ["AU", "TI", "MJ" , "MN" , "AB" , "EX"]          #partes com informações interessantes do texto

#lê o arquivo
for linha in txt:
    linha = linha.strip("\n").split(" ")
    if( linha[0] != ""):
        tag = linha[0]

    if( tag in interestedTags ):
        words += linha
    elif( tag == "PN" and words != []):
        docs.append( [k.strip(string.punctuation).lower() for k in words if( k != "")])
        words = []

# docs.append([k.strip(string.punctuation).lower() for k in words if( k != "")])
# words = []

hashWords = dict({})

i = 1                                                               
#cria a lista invertida
for doc in docs:
    for palavra in doc:
        if (palavra not in stopwords and palavra not in interestedTags and palavra.isalpha()):
            if( not palavra in hashWords):
                hashWords[palavra] = [(i , 1)]
            else:
                achou = False
                lista = hashWords[palavra]
                for k in range( len(lista)):
                    if( lista[k][0] == i):
                        lista[k] = ( lista[k][0] , lista[k][1] + 1)
                        achou = True
                        break
                if( not achou ):
                    lista.append( (i , 1))
                hashWords[palavra] = lista
    i+=1


ndocs = i
hashIdf = dict({})
hashNorma = dict({})

#Para cada elemento no Hash de palavras, calcula o ln de ndocs sobre o tamanho da 
#lista invertida da palavra( em qtos documentos ela aparece)
for x in hashWords:
    hashIdf[x] = math.log( ndocs/len( hashWords[x]))

print("[Pré-calculando normas...]")
normas = open("normas.dat")
normas = normas.readlines()

for i in range( len(normas)):
    hashNorma[i+1] = float( normas[i])

#pega as consultas do cfc e seus resultados ideais
arq = open("cfquery")

txt = arq.readlines()
i = 0

insterestedTags = ["QU", "RD"]
query = []
relevant = []
pesinho = []

hashQueries = dict({})
hashRelevancia = dict({})

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
        pesinho = [relevant[i] for i in range(len(relevant)) if (i % 2 != 0)]
        relevant = [relevant[i] for i in range(len(relevant)) if (i % 2 == 0)]

        # print("Texto da Consulta: \n" , query)
        # print("Relevantes: \n" , relevant)

#Calcula a relevancia de cada documento encontrado no resultado ideal e guarda no hashRelevancia
        for i in range(0,len(relevant)):
            numes = list(pesinho[i])
            for l in range(0,len(numes)):
                numes[l] = int(numes[l])

            hashRelevancia[i] = moda(numes)


        hashQueries[query] = relevant
        query = []
        relevant = []

query = " ".join([x for x in query[1:] if (x != "")])
relevant = [x for x in relevant[1:] if (x != "")]
relevant = [relevant[i] for i in range(len(relevant)) if (i % 2 == 0)]
hashQueries[query] = relevant

#FIM DO PEGA AS CONSULTAS
NDCGs = []
guardaMAPs = 0
meuResult = []
resultIdeal = []
G = [] #guarda a relevância de cada documento na ordem que eles foram retornados

#faz o processo para cada consulta sugerida no arquivo cfquery
for k in hashQueries:
    Result = TermoaTermo(k)             #aplica o termo a termo na cconsulta k, guarda o resultado em result

    for i in Result:
        meuResult.append(i[1])          #meu resultado são os documentos retornados pelo termo a termo

    for i in hashQueries[k]:
        resultIdeal.append(int(i))

#calculo do G, vetor que guarda os valores das relenvacia na ordem que os documentos aparecem
    for l in meuResult:
        if l in hashRelevancia:
            G.append(hashRelevancia[l])
        if l not in hashRelevancia:
            G.append(0)
#calcula CG
    meuCG = calculaCG(G)
#calculando IG, que é o vetor G ideal para o resultado obtido
    IG = G
    insertionSort(IG)
    meuICG = calculaCG(IG)
#calcula o DCG
    DCG = calculaDCG(meuCG)
    IDCG = calculaDCG(meuICG)
#calculando o NDCG
    oNDCG = calculaNDCG(DCG,IDCG)
    NDCGs.append(oNDCG)
    # print("\n\nConsulta: " + k)
    # print("DCG : ")
    # print(DCG)
    # print("Meus resultados: ")
    # print(meuResult)
    # print("Resultados ótimos: ")
    # print(resultIdeal)
    map = MAPi(resultIdeal,meuResult)
    # print("MAP dessa consulta = " + str(map))
    guardaMAPs += map
    meuResult = []
    resultIdeal = []
    G = []
mediaMAPs = guardaMAPs/len(hashQueries)
mediaNDCG = sum(NDCGs)/len(hashQueries)
print("\nMAP médio = " + str(mediaMAPs))
print("NDCG médio = " + str(mediaNDCG))

# while True:
#     query = input("Digite aqui para fazer sua busca:\n")
#     query = query.split(" ")
#
#     query = [ word.strip(".,:)(?!;-").lower() for word in query]
#
#     meus = TermoaTermo( query )


