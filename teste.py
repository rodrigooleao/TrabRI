import math

arq = open("cf74")
arq1 = open("cf75")
arq2 = open("cf76")
arq3 = open("cf77")
arq4 = open("cf78")
arq5 = open("cf79")

txt = arq.readlines()
# txt += arq1.readlines() #Para fazer a lista com todos os docs descomentar esta parte
# txt += arq2.readlines() # Comentado por motivos de: demora pra testar
# txt += arq3.readlines()
# txt += arq4.readlines()
# txt += arq5.readlines()

docs = []
words = []

interestedTags = ["AU","TI", "MJ" , "MN" , "AB" , "EX"]          #partes com informações interessantes do texto

for linha in txt:
    linha = linha.strip("\n").split(" ")
    if( linha[0] != ""):
        tag = linha[0]

    if( tag in interestedTags ):
        words += linha
    elif( tag == "PN" and words != []):
        docs.append( [k.strip(".,:)(?!;-").lower() for k in words if( k != "")])
        words = []

hashWords = dict({})

i = 1                                                           #i é o numero do documento atual que está sendo verificado

for doc in docs:                                                #para cada documento da lista de documentos
    for palavra in doc:                                         #para cada palavra no documento atual
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

# for x in hashWords:
#     print( x  , " - " , hashWords[x])

ndocs = i
hashIdf = dict({})

for x in hashWords:
    hashIdf[x] = math.log( ndocs/len( hashWords[x]))          #Para cada elemento no Hash de palavras, calcula o log10 de ndocs sobre o tamanho da 
                                                                #lista invertida da palavra( em qtos documentos ela aparece)
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
    result = 0
    for word in hashWords:
        result += (weight( doc , word) ** 2)
    
    return math.sqrt( result )

def filterHash( query ): #Filtra o hash para palavras que tem na consulta
    result = dict({})

    for word in query:
        if( word in hashWords):
            result[word] = hashWords[word]
    
    return result

def TermoaTermo( query ):
    hashQuery = filterHash( query )

    acums = [0 for x in range( ndocs )]

    for term in hashQuery:
        for doc,freq in hashQuery[term]:
            acums[doc-1] += freq * idf( term )**2


    for i in range( len(acums)):
        acums[i] = acums[i]/(norma(i + 1) + 1)

    print(acums)

query = input("\n\nDigite aqui para fazer sua busca:\n")
query = query.split(" ")

query = [ word.strip(".,:)(?!;-").lower() for word in query]

TermoaTermo( query )





