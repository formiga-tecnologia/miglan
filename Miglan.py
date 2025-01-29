import os
import numpy as np

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
           Value_=0
           if isinstance(value,tuple) or isinstance(value,np.ndarray):
               #Numpy Case

               if(isinstance(value,np.ndarray)):
                   try:
                        for value_sum in value:
                            for i in value_sum:
                                Value_+=i
                        return Value_
                   except:
                       for sum_value in value:
                           Value_+=sum_value
                       return Value_
               for value_sum in value:
                   Value_+=int(value_sum)
               return Value_
                #End Numpy Case

           #List Case
           if(isinstance(value,type([]))):
               for value_sum in value:
                    Value_+=int(value_sum)
               return Value_
           
           #End List Case

       ActionsValids = {"soma":soma}  
       action_function = ActionsValids.get(ActionName[0])
       FilterCols = None
       if(len(ActionName[1])>=1):   
            if("#" in ActionName[1][1]):
                FilterCols = str(ActionName[1][1]).replace("#","")
                FilterCols = FilterCols.split(",")

       if(FilterCols == None and len(ActionName) >=2):
           ValueList = list(ActionName[1])
           ValueList.pop(0)
           return action_function(ValueList)
           
       if action_function:
            if isinstance(Values,tuple)  or isinstance(Values,np.ndarray) :  
                if(len(FilterCols)==1):
                    return action_function(Values[FilterCols[0]])
                if(len(FilterCols) > 1):
                    return action_function(Values[FilterCols[0]][FilterCols[1]])
                return action_function(Values)
            if isinstance(Values, type([])):
                if(len(FilterCols)==1):
                    return action_function(Values[int(FilterCols[0])])
                if(len(FilterCols) > 1):
                    return action_function(Values[int(FilterCols[0])][int(FilterCols[1])])
                return action_function(Values)
            return action_function(ActionName[1])

    def ExecuteModel(self,ModelName,ValueBase=None):
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
                break
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
            if(ValueBase is not None and len(ValueBase) >0):
                Value = self.ExecuteAction(Action_base,ValueBase)
                Results.append(Value)
            else:
                Value = self.ExecuteAction(Action_base)
                Results.append(Value)
        return Results

