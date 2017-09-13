arq = open("cf74")

txt = arq.readlines()

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
        docs.append( [k.strip(".,:)(").lower() for k in words if( k != "")])
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

for x in hashWords:
    print( x  , " - " , hashWords[x])


    