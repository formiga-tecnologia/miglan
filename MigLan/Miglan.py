import json
import os

class Miglan:
    def __init__(self,ModelData="Model",RuleProcess="Rule"):
        def InjectExtension(Model):
             if not os.path.exists(Model+".json"):
                 with open(Model+".json",'w',encoding="utf-8") as ModelData:
                    json.dump({},ModelData,indent=2,ensure_ascii=False)
             return Model+".json"
        self.Model = InjectExtension(ModelData)
        self.RuleData = InjectExtension(RuleProcess)
        self.Encoding = 'utf-8'


    def GenerateTokenText(self,Text:str):
        with open(self.Model,'r',encoding=self.Encoding) as ModelData:
            model_data = json.load(ModelData)

        model_data[Text.lower()] = [0,None,0]

        with open(self.Model,'w',encoding=self.Encoding) as ModelData:
            json.dump(model_data,ModelData,indent=2,ensure_ascii=False)
        
        return "OK"
    
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
        return str(ListRule+str(ModData))
    
    def ResponseData(self,Rule:str):
        with open(self.RuleData,"r",encoding=self.Encoding) as Respost:
            Data_reader = json.load(Respost)
            for i in Data_reader:
                if Rule == i:
                    return Data_reader[i]
    
    def GetClassWord(self,Text:str,type:str):
        DataText = Text.split(" ")
        with open(self.Model,"r",encoding=self.Encoding) as Respost:
            Data_reader = json.load(Respost)
            for i in Data_reader:
                for x  in DataText:
                    if i == x:
                        if type == Data_reader[i][1]:
                            return x

    def ReturnProcessResponse(self,Text:str,ReplaceText:str,ClassWord:str):
        ReturnData = self.ResponseData(self.ReturnRuleContext(Text))
        WordData = self.GetClassWord(Text,ClassWord)
        return ReturnData[0].replace(ReplaceText,WordData)