import os
import numpy as np
import json

class Miglan():

    def __init__(self, Columns=None, Model=None,DataModel=None) -> None:
        self.Columns = Columns
        self.Model = Model if Model is not None else "./MiglanBase/Actions.json"
        self.ActionsMiglan = {"Show":self.Show}
        self.DataModel = DataModel if DataModel is not None else "./MiglanBase/Data.json"
        self.__Search =None
        
    def ReadActions(self,Actions=None):
        if Actions is not None:
            String_actions = Actions.split(" ")
            String_Response  = []
        if os.path.exists(self.Model):
            with open(self.Model, 'r') as file:
                self.Actions = file.read()
                ActionsRead = json.loads(self.Actions)
                if Actions is not None:
                    for i in String_actions:
                        String_Response.append(ActionsRead.get(i,{i:i}))
                    return self.ActionsMiglan[String_Response[0]["Action"]](String_Response)   
                else:
                    self.Actions = ActionsRead
                return self.Actions
        else:
            raise FileNotFoundError(f"File {self.Model} not found.")
        
        
    def Show(self,Parans):
        # Adiconar a logica pra tratar e mostras os dados
        Terms_of_Search = []
        Value_data = []
        for i in Parans:
            if i.get("Action") == None:
                Terms_of_Search.append(list(i.keys())[0])
        with open(self.DataModel, 'r') as file:
            self.Data = file.read()
            DataRead = json.loads(self.Data)
            for i in DataRead:
                  Value_data =  self.__auxRead__(Terms_of_Search,i)
                  if Value_data != None:
                      break
        return Value_data


    def __auxRead__(self,Obj:list,Value):
        Obj = [item for item in Obj if item not in (None, '')]
        self.__Search = None
        if len(Obj) == 1:
            for i in Value:
                if str(Value[i]) == Obj[0]:
                    self.__Search = Value
            return self.__Search
        elif len(Obj) > 1:
            Obj_compare =""
            for x  in Obj:
                Obj_compare+= str(x+" ")
            for i in Value:
                if str(Value[i]) in Obj_compare:
                    self.__Search = Value
            return self.__Search
  