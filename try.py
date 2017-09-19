def precisao (resultadoIdeal, meuResultado):
    numIguais = 0
    conta = 1
    precisoes = []
    prec = 0
    for elemento in meuResultado:
        if elemento in resultadoIdeal:
            numIguais += 1
        prec = numIguais / conta
        precisoes.append(round(prec*100,2))
        conta += 1
    return precisoes

print(precisao([3,5,9,25,39,44,56,71,89,123],[123,84,56,6,8,9,511,129,187,25,38,48,250,113,3]))
print(precisao([3,56,129],[425,87,56,32,124,615,512,129,4,130,193,715,810,5,3]))