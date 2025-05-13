import os
import numpy as np
import json
import xml.etree.ElementTree as ET

class Miglan():

    def __init__(self, Columns=None, Model=None,DataModel=None) -> None:
        self.Columns = Columns
        self.Model = Model if Model is not None else "./MiglanBase/Actions.json"
        self.ActionsMiglan = {"show":self.Show,"append":self.Add,"where":self.WhereData}
        self.DataModel = DataModel if DataModel is not None else "./MiglanBase/Data.json"
        self.__Search =None
        
    def ReadActions(self, Actions=None):
       
        if Actions is not None:
            tokens = Actions.split(" ")
            return_data = []
            current_command = None
            current_args = []

        if os.path.exists(self.Model):
            with open(self.Model, 'r') as file:
                self.Actions = file.read()
                ActionsRead = json.loads(self.Actions)

                if Actions is not None:
                    for token in tokens:
                        if token.upper() in ActionsRead:
                            
                            if current_command:
                                action_info = ActionsRead
                                if "Action" in action_info[current_command.upper()]:
                                    result = self.ActionsMiglan[action_info[current_command.upper()]["Action"].lower()](current_args)
                                    return_data.append(result)
                                current_args = [] 
                            current_command = token  
                        else:
                            current_args.append(token)

                   
                    if current_command and current_args:
                        if "Action" in ActionsRead[current_command.upper()]:
                            action_info = ActionsRead
                            result = self.ActionsMiglan[action_info[current_command.upper()]["Action"].lower()](current_args)
                            return_data.append(result)

                    return return_data

                else:
                    self.Actions = ActionsRead
                    return self.Actions

        else:
            raise FileNotFoundError(f"File {self.Model} not found.")

        
        
    def Show(self,Parans:list):
        # Adiconar a logica pra tratar e mostras os dados
        Terms_of_Search = []
        Total_values = 0
        Parans = [item for item in Parans if item not in (None, '')]
        with open(self.DataModel, 'r') as file:
            self.Data = file.read()
            DataRead = json.loads(self.Data)
            self.__Search = []

            for i in DataRead:
                if dict(i).get(Parans[0]) != None:
                    self.__Search.append(dict(i).get(Parans[0]))
                if Total_values == len(Parans):
                    self.__Search = i
                    break
                for y in i:
                    for x in Parans:
                        if x in str(i[y]):
                            Terms_of_Search.append(x)
                            Total_values += 1
                if Total_values == len(Parans):
                    self.__Search = i
                    break
        return self.__Search
    
    def Add(self,Parans):
        Parans = [item for item in Parans if item not in (None, '')]
        return Parans

    def UpdateActions(self):
        xml_path = "./Documetation.xml"
        tree = ET.parse(xml_path)
        root = tree.getroot()
        actions = {}
        for action in root.findall('Action'):
            name = action.get('Name').upper()
            actions[name] = {
                "Action": str(action.findtext('Command', default=name)).upper(),
                "Direction": int(action.findtext('Direction', default="1")),
                "attach": action.findtext('attach', default="")
            }
        with open(self.Model, 'w', encoding='utf-8') as f:
            json.dump(actions, f, indent=4, ensure_ascii=False)
        return actions

    def WhereData():
        pass

        
  