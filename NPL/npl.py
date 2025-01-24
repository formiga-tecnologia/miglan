import os 
import json
class npl:
    def __init__(self,Model:str="npl.json"):
        self.model = Model
        pass

    def ProcessInput(self,text):
            Data = {}
            Text_process = text.split(" ")
            Data["Grammar_key_data"] = self.GrammarProcess()
            self.GrammarProcess()
            for i in Text_process:                    
                    Data[str(i).lower()] = [0,0,0,0,0]
            with open(self.model,'w')  as DataFile:
                json.dump(Data, DataFile, ensure_ascii=False, indent=4, separators=(",", ": "))

    def TokenModel(self):
          DataModel_ =""
          with open(self.model,'r') as DataModelFile:
                DataModel_ = json.load(DataModelFile)
                for i in DataModel_:
                      if i not in "Grammar_key_data"  and DataModel_[i][0] == 0 :
                            print("  **  ")
                            print(i)
                            List_data = [int(input("mood ")),int(input("Importance ")),int(input("Family ")),int(input("Group ")),int(input("Gender "))]
                            DataModel_[i] = List_data
                with open(self.model,'w')  as DataFile:
                    json.dump(DataModel_, DataFile, ensure_ascii=False, indent=4, separators=(",", ": "))

    def GrammarProcess(self,GrammarKey="Grammar_key_data",Values=[ 0,1,2,2.1,3]):
          Data = {GrammarKey:Values}
          return Data[GrammarKey]
    
    def ProcessKeyWord(self,Text):
        """
        Process the most important Key in the setence.
        Args:
            Text (str): the text for analyse 

        Returns:
            Str: Tuple with keyWord and Value
        """
        List_text = Text.split(" ")
        with open(self.model,'r') as fileWord:
               DataModel_ = json.load(fileWord)
               KeyWord_value = 0
               Key_ = "a"
               for  i in List_text:
                    Value =DataModel_.get(i.lower())
                    if Value != None:
                        if Value[1] > KeyWord_value:
                            KeyWord_value = Value[1]
                            Key_ = i
        return (KeyWord_value,Key_)



n = npl()
#n.ProcessInput("Eu gosto de macarrao com queijo,mas odeio alface")

print(n.ProcessKeyWord("voce gosta de queijo ou alface ?"))