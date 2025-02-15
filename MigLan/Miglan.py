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


    def GroupWords(self,GroupWord:list):
        with open(self.config,'r',encoding=self.Encoding) as ModelData:
            model_data = json.load(ModelData)

        model_data["GroupWords_MiglanConfig"] = GroupWord

        with open(self.config,'w',encoding=self.Encoding) as ModelData:
            json.dump(model_data,ModelData,indent=2,ensure_ascii=False)
        
        return "OK"
    
    def ReturnGroupWords(self):
          with open(self.config,'r',encoding=self.Encoding) as ModelData:
            model_data = json.load(ModelData)
          return model_data["GroupWords_MiglanConfig"]

    def GenerateNewMemory(self,MemoryData):
         with open(self.config,'r',encoding=self.Encoding) as ModelData:
            model_data = json.load(ModelData)

         model_data["Memory_MiglanConfig"] = MemoryData

         with open(self.config,'w',encoding=self.Encoding) as ModelData:
            json.dump(model_data,ModelData,indent=2,ensure_ascii=False)
        
         return "OK"

    
    def ReturnMemoryData(self):
        with open(self.config,'r',encoding=self.Encoding) as ModelData:
            model_data = json.load(ModelData)
        return model_data["Memory_MiglanConfig"]
    
    
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
    
    def ResponseData(self,Rule:str,Debug=True):
        with open(self.RuleData,"r",encoding=self.Encoding) as Respost:
            Data_reader = json.load(Respost)
            print(Rule)
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
                        
    def GetClassToken(self,Text:str):
        DataText = Text.split(" ")
        ClassTokens =[]
        with open(self.Model,"r",encoding=self.Encoding) as Respost:
            Data_reader = json.load(Respost)
            for i in Data_reader:
                for x  in DataText:
                    if i == x:
                        ClassTokens.append(Data_reader[i][1])
        return ClassTokens
                        
    def GetWordByClass(self,type:str,Felling:int=None):
        with open(self.Model,"r",encoding=self.Encoding) as Respost:
            Data_reader = json.load(Respost)
            for i in Data_reader:
                    if Felling is  None:
                        if type == Data_reader[i][1]:
                            return i
                    else:
                        if Felling <= 0:
                           if type == Data_reader[i][1] and Data_reader[i][0] <= Felling:  
                                return i
                        elif type == Data_reader[i][1] and Data_reader[i][0] >= Felling:
                            return i
            return ""

    def ReturnProcessResponse(self,Text:str,ReplaceText:str,GetClassModel:str=None,ByFelling=False,MemoryUse=False):
        Text = self.RemoveStopWords(Text)
        ReturnData = self.ResponseData(self.ReturnRuleContext(Text))
        if ReturnData == False:
            return self.BadResponse
        if not GetClassModel  is None:
            WordData = ""
            List = ReturnData[1].split(" ")
            for i in List:
                #print(i)
                #print(List)
                if ByFelling == True:
                    print(self.FeelingProcess(Text))
                    WordData+= self.GetWordByClass(i,self.FeelingProcess(Text))+" "
                else:
                    WordData+= self.GetWordByClass(i)+" "
        else:
            WordData_0 = ""
            ListReturn = list(ReturnData[1].split("."))
            ListReturn.remove('')
            for i in ListReturn:
                Test_Word_class =  self.GetClassWord(Text,i+".")
                if Test_Word_class is not None:
                    WordData_0 += Test_Word_class+" "
                else:
                    ...
                    #Seach  for the Class in the context
            WordData = WordData_0
        if MemoryUse ==True:
            a = self.MemoryDataReturn(ReplaceText)[1]
            if a is not None:
                return a+" "+ReturnData[0].replace(ReplaceText,WordData)
        return ReturnData[0].replace(ReplaceText,WordData)
    
    def FeelingProcess(self,text):
         List_text = text.split(" ")
         Fellings = 0
         with open(self.Model,"r",encoding=self.Encoding) as Respost:
            Data_reader = json.load(Respost)
            for i in Data_reader:
                if i in List_text:
                    Fellings+=Data_reader[i][0]
         return Fellings
    
    def MemoryDataReturn(self,Replace,IndexBase=None):
        if  IndexBase == None:
            return (self.FeelingProcess(self.ReturnMemoryData()),self.ReturnProcessResponse(self.ReturnMemoryData(),Replace))
        else:
            Data = self.ReturnMemoryData()
            return (self.FeelingProcess(Data[IndexBase]),self.ReturnProcessResponse(Data[IndexBase],Replace))

    def SearchByReturnResponseContext(self,WordSearchRule:str,ClassWord:str,Felling=False,Importance=2):
        # Return the wor by importance or felling, and both avaliates
        ...

    def ReturnDataSetence(self,TextInput:str):
        Results = {}
        with open(self.Model,'r',encoding=self.Encoding) as importModel:
            importModel_dta = json.load(importModel)
            ListString = TextInput.lower().split(" ")
            for i in importModel_dta:
                if  i in ListString:
                    Results[i] = importModel_dta[i]
        return Results
    
    def ProcessByImportanceWord(self,TextInput:str):
        Data_analyse = self.ReturnDataSetence(TextInput)
        MaxValue = 0 
        Token = ""

        for i in Data_analyse:
            if Data_analyse[i][2] > MaxValue:
                Token = i
                MaxValue = Data_analyse[i][2]
        
        return (Token,MaxValue)

                    