from collections import defaultdict,Counter
recipes=[]
def add_recipe(inputs,output):
    #FORMAT: dict str:int inputs, (item,quantity) or item output
    if isinstance(output,tuple):
        recipes.append((inputs, output))
    else:
        recipes.append((inputs,(output,1)))
    recipes.sort(key=lambda r:sum(r[0].values()))
processing_recipes=defaultdict(list)
def add_process_recipe(rtype,input,output,energy):
    #FORMAT: (str,int) for both
    processing_recipes[rtype].append((input,output,energy))