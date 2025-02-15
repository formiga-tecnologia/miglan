from MigLan import Miglan

ChatBot_base =  Miglan.Miglan(r"E:\Formiga\Projetos\miglan-1\ChatBot\ModeloVivaVerde",
                              r"E:\Formiga\Projetos\miglan-1\ChatBot\RegrasChatBot",
                              r"E:\Formiga\Projetos\miglan-1\ChatBot\ConfigChatBot","Não sei responder isso")

#ChatBot_base.GenerateTokenText("lapis")
# ChatBot_base.GroupWords(["prod.","ac.","per."])
# ChatBot_base.StopWords(["de"])
#print(ChatBot_base.ReturnRuleContext("suplemento vitamínico"))
def ProcurarProduto(Produto):
    print(Produto)

Resposta = ChatBot_base.ReturnProcessResponse("suplemento de magnésio","{@}")
Acao = {"return_Produto":ProcurarProduto}

Acao_dev=Acao.get(Resposta)

if Acao_dev != None:
    Acao_dev("suplemento de magnésio")
else:
    print(Resposta)