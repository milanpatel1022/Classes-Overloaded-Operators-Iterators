from collections import defaultdict
from goody import type_as_str
import prompt
from copy import deepcopy

class Bag:
    def __init__(self, *args):
        self.dic = defaultdict(int)
        if len(args) > 0:
            for value in args[0]:
                self.dic[value] += 1
    
    def __repr__(self) -> str:
        lst = []
        for key in self.dic.keys():
            for i in range(self.dic[key]):
                lst.append(key)
        return 'Bag({})'.format(lst)

    def __str__(self) -> str:
        compact = ['{}[{}]'.format(k,v) for k, v in self.dic.items()]
        return 'Bag('+', '.join(item for item in compact)+')'
        
    def __len__(self) -> int:
        return sum(self.dic.values())
    
    def unique(self) -> int:
        return len(self.dic.keys())
    
    def __contains__(self, value) -> bool:
        return value in self.dic
    
    def count(self, value) -> int:
        return self.dic[value] if value in self.dic else 0
    
    def add(self, value):
        self.dic[value] += 1 if value in self.dic else 1
            
    def __add__(self, other_bag):
        if type(other_bag) is not Bag:
            return NotImplemented
        else:
            new_lst = []
            for key in other_bag.dic.keys():
                for i in range(other_bag.dic[key]):
                    new_lst.append(key)
            for key in self.dic.keys():
                for i in range(self.dic[key]):
                    new_lst.append(key)
            return Bag(new_lst)
    
    def remove(self, value) -> None:
        if value not in self.dic:
            raise ValueError('{} could not be removed'.format(value))
        else:
            self.dic[value] -= 1
            if self.dic[value] == 0:
                self.dic.pop(value)
                
    def __eq__(self, other_bag) -> bool:
        if type(other_bag) is not Bag:
            return False
        else:
            return sorted(self.dic.keys()) == sorted(other_bag.dic.keys()) and sorted(self.dic.values()) == sorted(other_bag.dic.values())
        
    def __ne__(self, other_bag) -> bool:
        if type(other_bag) is not Bag:
            return True
        else:
            return sorted(self.dic.keys()) != sorted(other_bag.dic.keys()) or sorted(self.dic.values()) != sorted(other_bag.dic.values())
    
    def __iter__(self):
        def gen(dic):
            for key in dic.keys():
                for i in range(dic[key]):
                    yield key
        original_dic = deepcopy(self.dic)
        return gen(original_dic)

    
if __name__ == '__main__':
    
    #Simple tests before running driver
    #Put your own test code here to test Bag before doing the bsc tests
    #Debugging problems with these tests is simpler

    b = Bag(['d','a','d','b','c','b','d'])
    print(repr(b))
    print(all((repr(b).count('\''+v+'\'')==c for v,c in dict(a=1,b=2,c=1,d=3).items())))
    #for i in b:
    #    print(i)

    b2 = Bag(['a','a','b','x','d'])
    #print(repr(b2+b2))
    #print(str(b2+b2))
    #print([repr(b2+b2).count('\''+v+'\'') for v in 'abdx'])
    b = Bag(['a','b','a'])
    print(repr(b))
    print()
    
    import driver
    driver.default_file_name = 'bscp21S19.txt'
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
#     driver.default_show_traceback = True
    driver.driver()
