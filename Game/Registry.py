from collections import defaultdict,Counter
recipes={}
default_recipes=defaultdict(list)
def add_recipe(inputs,output,type="Crafting",team="Base"):
    #FORMAT: dict str:int inputs, (item,quantity) or item output
    rlist=default_recipes[type] if team is "Base" else get_recipes(team,type)
    if isinstance(output,tuple):
        rlist.append((inputs, output))
    else:
        rlist.append((inputs,(output,1)))
    rlist.sort(key=lambda r:sum(r[0].values()))
processing_recipes=defaultdict(list)
def add_process_recipe(rtype,input,output,energy):
    #FORMAT: (str,int) for both
    processing_recipes[rtype].append((input,output,energy))
def get_recipes(team,type):
    if team in recipes:
        return recipes[team][type]
    else:
        recipes[team]=defaultdict(list)
        for k,v in default_recipes.items():
            recipes[team][k]=v[:]
        return recipes[team][type]