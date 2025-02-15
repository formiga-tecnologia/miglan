from MigLan import Miglan
import json

Data_miglan = Miglan.Miglan(r"E:\Formiga\Projetos\miglan-1\ChatBot\ModeloVivaVerde",
                              r"E:\Formiga\Projetos\miglan-1\ChatBot\RegrasChatBot",
                              r"E:\Formiga\Projetos\miglan-1\ChatBot\ConfigChatBot","Não sei responder isso")

with open(r"E:\Formiga\Projetos\miglan-1\DataBase\Produtos_VivaVerde.json",'r',encoding='utf-8') as DataBase:
    Data = json.load(DataBase)
    for i in Data["produtos"]:
        for x in i.split(" "):
            Peso_Produto = int(Data["produtos"][i]["preço"])
            print(Peso_Produto-5)
            Data_miglan.GenerateTokenText(x,[2,"pd.",Peso_Produto-10])
    