class uint32:
    def __init__(self,number):
        number &= 0xFFFFFFFF
        if number < 0:
            number += 0x100000000
        self.value = number
    
    def __add__(self,other):
        try:
            return uint32(self.value+other.value)
        except:
            return uint32(self.value+other)
        
    def __sub__(self,other):
        try:
            return uint32(self.value-other.value)
        except:
            return uint32(self.value-other)
            
    def __and__(self,other):
        try:
            return uint32(self.value & other.value)
        except:
            return uint32(self.value & other)
        
    def __gt__(self,other):
        try:
            return self.value > other.value
        except:
            return self.value > other
            
    def __ge__(self,other):
        return self > other - 1
        
    def __lt__(self,other):
        try:
            return self.value < other.value
        except:
            return self.value < other
    
    def __le__(self,other):
        return self < other + 1
        
    def __rshift__(self,other):
        try:
            return uint32(self.value >> other.value)
        except:
            return uint32(self.value >> other)
        
    def __int__(self):
        return self.value
        
    def __str__(self):
        return str(self.value)
        
    def __repr__(self):
        return hex(self.value)
        
class int32:
    def __init__(self,number):
        number &= 0xFFFFFFFF
        if number & 0x80000000:
            number -= 0x10000000
        self.value = number
    
    def __add__(self,other):
        try:
            return uint32(self.value+other.value)
        except:
            return uint32(self.value+other)
        
    def __sub__(self,other):
        try:
            return uint32(self.value-other.value)
        except:
            return uint32(self.value-other)
            
    def __and__(self,other):
        try:
            return uint32(self.value & other.value)
        except:
            return uint32(self.value & other)
        
    def __gt__(self,other):
        try:
            return self.value > other.value
        except:
            return self.value > other
            
    def __ge__(self,other):
        return self > other - 1
        
    def __lt__(self,other):
        try:
            return self.value < other.value
        except:
            return self.value < other
    
    def __le__(self,other):
        return self < other + 1
        
    def __rshift__(self,other):
        try:
            return uint32(self.value >> other.value)
        except:
            return uint32(self.value >> other)
        
    def __int__(self):
        return self.value
        
    def __str__(self):
        return str(self.value)
        
    def __repr__(self):
        return hex(self.value)
        
if __name__ == '__main__':
    a = uint32(5)
    b = uint32(6)
    print(a+b)
    print(int(a))
    a -= 2
    print(a)
