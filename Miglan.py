import os

class Miglan():
    """
    Tool for Machine Learning and Data Science Analitycs
    param: Columns of dataframe type: Vector,
    Model tou pass name of model you want execute.
    """
    def __init__(self,Columns=None,Model=None) -> None:
        self.PathFile = os.getcwd()
        self.Path = "//MiglanBase"
        self.model_file = Model
        self.baseFile = os.path.join(self.PathFile+self.Path,"base.migl")
        
    def ExecuteAction(self,ActionName,Values=None):
       
       def soma(value):
           #sum values
           value.pop(0)
           Value_=0
           for value_sum in value:
               Value_+=int(value_sum)
           return Value_
       ActionsValids = {"soma":soma}  
       action_function = ActionsValids.get(ActionName[0])
       if action_function:   
            return action_function(ActionName[1])

    def ExecuteModel(self,ModelName):
        """
        Execute your model, when return create new values to your
        database.
        Args:
            ModelName (str): Name of your model name
        """
        with open(self.baseFile, "r") as ModelBase:
            comands = ModelBase.readlines()
        ExecuteActions = []
        Results = []
        Model_find = False
        for  i in comands:
            if(i[0] !="@" and Model_find == True):
                return 0
            if("model:"+ModelName in i ):
                modelName = i.replace("model:","").replace("/n","").strip()
                if(modelName == ModelName):
                    Model_find = True
            if(i[0] =="@" and Model_find == True):
                ExecuteActions.append(i.replace("\n","").replace("@",""))
        for action in ExecuteActions:          
            Param = action.strip()
            Param = Param.split(" ")
            Action_base = (Param[0],Param)
            Value = self.ExecuteAction(Action_base)
            Results.append(Value)
        return Results
            


import numpy as np
            

#Ml = Miglan()
#print(Ml.ExecuteModel("soma"))

DataBase = [[12,23,45,56],[34,56,67,78]]
Data = np.random.randn(3,3)
data2 = Data[Data >=0]
print(data2[2])


#Matriz= [[12,34,56,78,90,45],[23,34,54,56,56,67]]

# 12,34,56,78,90,45,s
# 23,34,54,56,56,67,s
# S, s ,s ,s , s ,s