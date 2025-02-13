import json
import os

class Miglan:
    def __init__(self,ModelData="Model",RuleProcess="Rule",ModelConfig="config",BadResponse="I don't know how to answer that"):
        def InjectExtension(Model):
             if not os.path.exists(Model+".json"):
                 with open(Model+".json",'w',encoding="utf-8") as ModelData:
                    json.dump({},ModelData,indent=2,ensure_ascii=False)
             return Model+".json"
        self.Model = InjectExtension(ModelData)
        self.RuleData = InjectExtension(RuleProcess)
        self.config = InjectExtension(ModelConfig)
        self.Encoding = 'utf-8'
        self.BadResponse = BadResponse


    def GenerateTokenText(self,Text:str,Elements:list = [0,None,0] ):
        with open(self.Model,'r',encoding=self.Encoding) as ModelData:
            model_data = json.load(ModelData)

        model_data[Text.lower()] = Elements

        with open(self.Model,'w',encoding=self.Encoding) as ModelData:
            json.dump(model_data,ModelData,indent=2,ensure_ascii=False)
        
        return "OK"
    
    def StopWords(self,StopWordsList:list):
        with open(self.config,'r',encoding=self.Encoding) as ModelData:
            model_data = json.load(ModelData)

        model_data["StopWords_MiglanConfig"] = StopWordsList

        with open(self.config,'w',encoding=self.Encoding) as ModelData:
            json.dump(model_data,ModelData,indent=2,ensure_ascii=False)
        
        return "OK"
    
    def RemoveStopWords(self,TextProcess:str):
        with open(self.config,'r',encoding=self.Encoding) as ModelData:
            model_data = json.load(ModelData)
        List_avaliable = TextProcess.split(" ")
        for i in model_data["StopWords_MiglanConfig"]:
            if i in List_avaliable:
                List_avaliable.remove(i)
        TextProcess = ""
        for x in List_avaliable:
            TextProcess+=x+" "
        return TextProcess

    def ReturnStopWords(self):
          with open(self.config,'r',encoding=self.Encoding) as ModelData:
            model_data = json.load(ModelData)
          return model_data["StopWords_MiglanConfig"]
    
    def ReturnRuleContext(self,Text:str):
        TextInput = Text.lower().split(" ")
        ListRule = ""
        ModData = 0
        with open(self.Model,"r",encoding=self.Encoding) as Data:
            DataReader = json.load(Data)
            for i in DataReader:
                for x in TextInput:
                    if x == i:
                        ListRule+=DataReader[i][1]
                        ModData+= DataReader[i][0]
        if ModData > 0:
            ModData = 1
            
        else:
            ModData = 0
        # print(ModData)
        # print(ListRule)

        return str(ListRule+str(ModData))
    
    def ResponseData(self,Rule:str):
        with open(self.RuleData,"r",encoding=self.Encoding) as Respost:
            Data_reader = json.load(Respost)
            for i in Data_reader:
                if Rule.split(".") == i.split("."):
                    return Data_reader[i]
            return False
    
    def GetClassWord(self,Text:str,type:str):
        DataText = Text.split(" ")
        with open(self.Model,"r",encoding=self.Encoding) as Respost:
            Data_reader = json.load(Respost)
            for i in Data_reader:
                for x  in DataText:
                    if i == x:
                        if type == Data_reader[i][1]:
                            return x

    def ReturnProcessResponse(self,Text:str,ReplaceText:str):
        ReturnData = self.ResponseData(self.ReturnRuleContext(Text))
        if ReturnData == False:
            return self.BadResponse
        WordData = self.GetClassWord(Text,ReturnData[1])
        return ReturnData[0].replace(ReplaceText,WordData)