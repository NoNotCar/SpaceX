from Lib import Img,Vector
from .Base import Machine,SlotMachine,FixedMachine
from Engine.Items import Placeable,fuels
from Game.Registry import add_recipe,get_recipes
from Game import Research
from . import MUI
V=Vector.VectorX
class Furnace(SlotMachine):
    imgs=Img.imgstripxf("Machines/Furnace",16)
    def __init__(self,c,r,p):
        super().__init__(c,r,p)
        self.processor=MUI.Processor("Smelting",10)
        self.fuel=MUI.FuelSlot()
        self.gui=MUI.MUI("Furnace",[self.processor,self.fuel])
        self.outputslot=self.processor.output
    def input(self,d,i):
        if i.name in fuels:
            return self.fuel.slot.add(i,1)
        return self.processor.input.add(i,1)
    @property
    def img(self):
        return self.imgs[bool(self.processor.progress)]
class AutoCrafter(SlotMachine):
    imgs=Img.imgstripxf("Machines/AutoCrafter",16)
    processor=None
    def __init__(self,c,r,p):
        super().__init__(c,r,p)
        self.electro=MUI.ElectroSlot(self)
        self.gui=MUI.MUI("Select Recipe", [MUI.RSelect(get_recipes(self.p.team,"Crafting"))])
    def gui_trigger(self,*args):
        if args[0]=="Change Recipe" and not (self.processor and any(self.processor.inputs.slots)):
            self.gui.re_init("Select Recipe", [MUI.RSelect(get_recipes(self.p.team,"Crafting"))])
            self.processor = None
        else:
            self.processor=MUI.Crafter(args,sum(q for q in args[0].values())*10,10)
            self.outputslot=self.processor.output
            self.gui.re_init("AutoCrafter",[self.processor,self.electro,MUI.Button("Change Recipe")])
    def input(self,d,i):
        return self.processor and self.processor.inputs.add(i,1)
    def re_own(self,p):
        self.p=p
        self.gui = MUI.MUI("Select Recipe", [MUI.RSelect(get_recipes(self.p.team, "Crafting"))])
    @property
    def img(self):
        return self.imgs[bool(self.processor and self.processor.progress)]
class Generator(FixedMachine):
    imgs=Img.imgstripxf("Machines/Generator")
    working=False
    def __init__(self,c,p):
        super().__init__(c,p)
        self.fuel=MUI.FuelSlot(20)
        self.gui=MUI.MUI("Generator",[self.fuel])
    def update(self, pos, area, events):
        lfl=self.fuel.left
        area.generate(self.fuel.get_power)
        self.working=lfl!=self.fuel.left
    def input(self,d,i):
        if i.name in fuels:
            return self.fuel.slot.add(i,1)
    @property
    def img(self):
        return self.imgs[self.working]
class Lab(FixedMachine):
    imgs=Img.imgstripxf("Machines/Lab")
    working=False
    def __init__(self,c,p):
        super().__init__(c,p)
        self.lab=MUI.Lab(100,10,p.team)
        self.gui=MUI.MUI("LAB",[self.lab,MUI.ElectroSlot(self)])
    def update(self, pos, area, events):
        lp=self.lab.progress
        super().update(pos,area,events)
        self.working=self.lab.progress!=lp
    def input(self,d,i):
        return self.lab.inputs.add(i)
    @property
    def img(self):
        return self.imgs[self.working]
add_recipe({"Stone":5},Placeable(Furnace))
add_recipe({"Iron":10,"Circuit":3},Placeable(AutoCrafter))
add_recipe({"Furnace":1,"Wire":8},Placeable(Generator))
add_recipe({"AutoCrafter":1,"SP1":5},Placeable(Lab))