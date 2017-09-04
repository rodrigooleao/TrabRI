arq = open("cf74")

txt = arq.readlines()
inAB = False

docs = []
abstract = []
for linha in txt:
    linha = linha.strip("\n").split(" ")
    tag = linha[0]

    if( tag == "AB"):
        inAB = True
    elif( tag != "" and inAB):
        inAB = False
        docs.append( [k.strip(".,") for k in abstract if( k != "")])
        abstract = []
        

    if( inAB ):
        abstract += linha
hashWords = dict({})

for doc in docs:
    for palavra in doc:
        if( not palavra in hashWords):
            hashWords[palavra] = 1
        else:
            hashWords[palavra] += 1

for x in hashWords:
    print( x  , " - " , hashWords[x])


    