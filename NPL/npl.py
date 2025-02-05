import os 
import json
class npl:
    def __init__(self,Model:str="npl"):
        self.model = Model+".json"
        self.ModelAw = Model+"aw.json"

    def ProcessInput(self,text):
            """
             Process the input create default width for the each word.
            Args:
            Text (str): the text for analyse 
            """
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

    def CreateAnswerModel(self):
         Data = {}
         with open(self.ModelAw,'w')  as DataFile:
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
          Data = {GrammarKey:Values,"StopWords_key_data":[]}
          return Data[GrammarKey]
    
    def GenerateTokenModelInput(self,Word,TokenList):
         with open(self.model,'r',encoding="utf-8") as  Model:
              data = json.load(Model)
          
         data[Word] = TokenList

         with open(self.model,'w',encoding="utf-8") as ModelAdd:
              json.dump(data,ModelAdd,indent=4,ensure_ascii=False)
    
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
         """
         Create one list with words , splits for Delimiters
         Args:
             Text (str): Text for split
             Delimiter (str): what delimiter search and spliter
             List (list, optional): Add elements to Exist List . Defaults to [].

         Returns:
             List: ["words"]
         """
         if List!= []:
              for i in Text.split(Delimiter):
                 List.append(i)
              return List
         return Text.split(Delimiter)
    
         
    def GroupByGroup(self,ListWords:list):
         """
          Create and analyze words and group word for group.
         Args:
             ListWords (list): List of words process

         Returns:
             Dicionary: {<group>:<vector words>}
         """
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
    
    def ImportanceKeyForGroup(self,GroupKeys,AnalizeType:int=1):
         """
          Generate list with Max and Min width in each group 
        Args:
            GroupKeys (list): Use the list generate for GroupByGroup function 
            AnalizeType (int): Select type of your dispersion Analyze (0:mod, 1:importance, 2:family,3:group)
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
                    if a[AnalizeType] > MaxGroup:
                         VectorMax = a
                         MaxGroup = a[AnalizeType]
                    if a[AnalizeType] < MinGroup or MinGroup == 0:
                         VectorMin = a
                         MinGroup = a[AnalizeType]
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

    def RemoveNoiseWords(self,Text:str):
         """
         Removes words that are not registered or irrelevant
        Args:
            Text (str): string text

        Returns:
            New String format with only relevant words.
         """
         List_word = Text.split(" ")
         NewString =""
         with open(self.model,"r") as Model:
              JsonModel =json.load(Model)
              for i in List_word:
                   if JsonModel.get(i.lower()) and  i.lower() not in JsonModel.get("StopWords_key_data"):
                        NewString+=" "+i+" "
                    
         return NewString 
    def DispersionGroup(self,GroupKeys,AnalizeType:int=1):
             """
            Generate value of Dispersion your GroupKeys.
        Args:
            GroupKeys (list): Use the list generate for GroupByGroup function 
            AnalizeType (int): Select type of your dispersion Analyze (0:mod, 1:importance, 2:family,3:group)
        Returns:
            int: Value Dispersion
             """
             Max_value = 0
             Min_value = 0
             for i in GroupKeys:
                  if type(i) == list:
                    if Min_value == 0:
                         Min_value = i[AnalizeType]
                    if i[AnalizeType] > Max_value:
                         Max_value = i[AnalizeType]
                    if i[AnalizeType] < Min_value:
                         Min_value = i[AnalizeType]

             return  Max_value-Min_value/10


