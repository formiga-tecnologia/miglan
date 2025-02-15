from MigLan import Miglan
from Alimentar_Token import ProcurarProdutoRepository,PesosTokenRepository

ChatBot_base =  Miglan.Miglan(r"E:\Formiga\Projetos\miglan-1\ChatBot\ModeloVivaVerde",
                              r"E:\Formiga\Projetos\miglan-1\ChatBot\RegrasChatBot",
                              r"E:\Formiga\Projetos\miglan-1\ChatBot\ConfigChatBot","Não sei responder isso")

#ChatBot_base.GenerateTokenText("lapis")
# ChatBot_base.GroupWords(["prod.","ac.","per."])
# ChatBot_base.StopWords(["de"])
#print(ChatBot_base.ReturnRuleContext("suplemento vitamínico"))
PesosTokenRepository()
def ProcurarProduto(Produto):
    
    #print(RetornarResposta)
    Valor = ChatBot_base.RemoveStopWords(Produto)
    Valor = ProcurarProdutoRepository(Produto)

    if isinstance(Valor,list):
        RetornarResposta = ChatBot_base.ReturnProcessResponse("equivalenteproduto","{@}")
        for i in Valor:
            print("VerdiBot: "+RetornarResposta.replace("{#1}",i[0]).split(",")[0])
    else:
        RetornarResposta = ChatBot_base.ReturnProcessResponse("buscarproduto equivalenteproduto","{@}")
        Valor_final = RetornarResposta.replace("{#1}",Valor[1]).replace("{#2}",str(Valor[0]["preço"])).replace("{#3}",Valor[0]["categoria"])
        print("VerdiBot: "+Valor_final)

    if Valor == []:
            Value  = ChatBot_base.GetClassToken(Produto)
            Valor = ProcurarProdutoRepository(ChatBot_base.GetClassToken(Produto)[0][1])
            RetornarResposta = ChatBot_base.ReturnProcessResponse("equivalenteproduto","{@}")
            for i in Valor:
                print("VerdiBot: "+RetornarResposta.replace("{#1}",i[0]).split(",")[0])

while(True):
    Input_1 = input("Digite sua msg > ")

    Resposta = ChatBot_base.ReturnProcessResponse(Input_1,"{@}")
    Acao = {"return_Produto":ProcurarProduto}

    Acao_dev=Acao.get(Resposta)

    if Acao_dev != None:
        Acao_dev(Input_1)
    else:
        print("VerdiBot: "+Resposta)