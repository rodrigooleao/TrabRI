arq = open("cf74")

txt = arq.readlines()

docs = []
words = []

interestedTags = ["TI", "MJ" , "MN" , "AB" , "EX"]
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

i = 1
for doc in docs:
    for palavra in doc:
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

for x in hashWords:
    print( x  , " - " , hashWords[x])


    