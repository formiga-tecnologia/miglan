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
            id_token = 0
            for i in Text_process:                    
                    Data[str(i).lower()] = [0,0,0,0,0,id_token]
                    id_token+=1
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
                            List_data = [float(input("mood ")),float(input("Importance ")),float(input("Family ")),float(input("Group ")),float(input("Gender "))]
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

    def SplitWords(self,Text,Delimiter,List=[]):
         if List!= []:
              for i in Text.split(Delimiter):
                 List.append(i)
              return List
         return Text.split(Delimiter)
         
    def GroupByGroup(self,ListWords:list):

         Groups = {}
         with open(self.model,"r") as Model:
              JsonModel =json.load(Model)
              for i in ListWords:
                   a=JsonModel.get(i)
                   if not a is None:
                        if not Groups.get(round(a[2]))  is None:
                             Groups[round(a[2])].append(a)
                        else:
                             Groups[round(a[2])] = [a] 
         return Groups
    
    def ImportanceKeyForGroup(self,GroupKeys):
         """
          Generate list with Max and Min width in each group 
        Args:
            GroupKeys (list): Use the list generate for GroupByGroup function 

        Returns:
            list: [(Grpup(round value),Max vector Key, Min Vector Key)]
         """
         List_Group_important= []
         MaxGroup = 0
         VectorMax = None
         MinGroup = 0
         VectorMin= None

         for i in GroupKeys:
              for a in GroupKeys[i]:
                    if a[1] > MaxGroup:
                         VectorMax = a
                         MaxGroup = a[1]
                    if a[1] < MinGroup or MinGroup == 0:
                         VectorMin = a
                         MinGroup = a[1]
              List_Group_important.append((i,VectorMax,VectorMin))
              MaxGroup = 0
              VectorMax = None
              MinGroup = 0
              VectorMin= None
         return List_Group_important
    
    def ReturnWord(self,Keys):
          List_words = []
          iterator = 0
          with open(self.model,"r") as Model:
              JsonModel =json.load(Model)
              for i in Keys:
                   iterator = 0
                   for s in JsonModel:
                     iterator+=1
                     if iterator >i:
                        List_words.append(s)
                        break  
          return List_words
                   
    def DispersionGroup(self,GroupKeys):#max - min / 10
             ...

n = npl()
Texto_ = "Eu gosto de macarrao com queijo,mas odeio alface"
#n.ProcessInput("Eu gosto de macarrao com queijo,mas odeio alface")
#n.TokenModel()
#a= n.GroupByGroup(n.SplitWords(Texto_.replace(","," ")," "))
list_a = n.SplitWords(Texto_,",")
a= n.GroupByGroup(n.SplitWords(list_a[0]," "))
ax=n.ImportanceKeyForGroup(a)
n.DispersionGroup(ax)
print(ax)
Words = n.ReturnWord([ax[0][1][4],ax[1][1][5]]) 

print("Eu "+Words[0]+" de " +Words[1])