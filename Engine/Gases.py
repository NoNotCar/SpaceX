
K_PRESSURE_PUSH=1
class FloatCounter(dict):
    def __getitem__(self, item):
        return self.get(item,0)
    def __add__(self, other):
        new=FloatCounter(self)
        new.add_ip(other)
        return new
    def __sub__(self, other):
        new = FloatCounter(self)
        new.sub_ip(other)
        return new
    def __mul__(self, other):
        return FloatCounter({k: v * other for k, v in self.iteritems()})
    def __truediv__(self, other):
        return FloatCounter({k:v/other for k,v in self.iteritems()})
    def add_ip(self,other):
        for k,v in other.iteritems():
            self[k]+=v
    def sub_ip(self,other):
        for k,v in other.iteritems():
            self[k]-=v
class Space(object):
    def __init__(self,volume,contents=None):
        self.v=volume
        self.c=contents if contents else FloatCounter()
    @classmethod
    def filled(cls,vol,gmix,pressure):
        return Space(vol,FloatCounter(gmix)*pressure*vol)
    def sample(self,vol):
        s=self.slice(vol)
        self.c-=s
        return s
    def slice(self,vol):
        return self.c*(min(vol/self.v,1))
    def mix(self,other,aperture=1):
        big,small=(self,other) if self.pressure>other.pressure else (other,self)
        bp,bm,sp,sm=big.pressure,big.moles,small.pressure,small.moles
        bs=big.sample(aperture+min((bp-sp)*K_PRESSURE_PUSH*aperture,
                                   (bp*small.v-sm)*bm/(sm+bm)))
        ss=small.sample(aperture)
        big.c+=ss
        small.c+=bs
    def __getitem__(self, item):
        return self.c[item]/self.moles
    @property
    def pressure(self):
        return sum(self.c.itervalues())/self.v
    @property
    def moles(self):
        return sum(self.c.itervalues())
    @property
    def percent(self):
        return self.c/self.moles

