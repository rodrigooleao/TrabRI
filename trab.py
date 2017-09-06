arq = open("cf74")

txt = arq.readlines()
i = 0
for linha in txt:
    linha = linha.strip("\n").split(" ")
    tag = linha[0]

    if( tag == "PN"):
        print( linha)
        i+=1

print( i )