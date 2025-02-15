from MigLan import Miglan
import json

Data_miglan = Miglan.Miglan(r"E:\Formiga\Projetos\miglan-1\ChatBot\ModeloVivaVerde",
                            r"E:\Formiga\Projetos\miglan-1\ChatBot\RegrasChatBot",
                            r"E:\Formiga\Projetos\miglan-1\ChatBot\ConfigChatBot", "Não sei responder isso")

def PesosTokenRepository():
    with open(r"E:\Formiga\Projetos\miglan-1\DataBase\Produtos_VivaVerde.json", 'r', encoding='utf-8') as DataBase:
        Data = json.load(DataBase)
        for i in Data["formas_de_pagamento"]:
            # for x in i.split(" "):
            #     Peso_Produto = int(Data["produtos"][i]["preço"])
            #     print(Peso_Produto-5)
            Data_miglan.GenerateTokenText(i, [2, "pag.", 20])


def ProcurarProdutoRepository(Produto):
    Lista_produtos = []
    with open(r"E:\Formiga\Projetos\miglan-1\DataBase\Produtos_VivaVerde.json", 'r', encoding='utf-8') as DataBase:
        Data = json.load(DataBase)
        for i in Data["produtos"]:
            if i == Produto.strip():
                return (Data["produtos"][i],i)
            elif Produto in i:
                Lista_produtos.append((i,Data["produtos"][i]))

    return Lista_produtos
