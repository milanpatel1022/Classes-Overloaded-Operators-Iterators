from goody import irange, type_as_str
import math

class Rational:
    @staticmethod
    # Called as Rational._gcd(...); no self parameter
    # Helper method computes the Greatest Common Divisor of x and y
    def _gcd(x : int, y : int) -> int:
        assert type(x) is int and type(y) is int and x >= 0 and y >= 0,\
          'Rational._gcd: x('+str(x)+') and y('+str(y)+') must be integers >= 0'
        while y != 0:
            x, y = y, x % y
        return x
    
    @staticmethod
    # Called as Rational._validate_arithmetic(..); static, so no self parameter
    # Helper method raises exception with appropriate message if type(v) is not
    #   in the set of types t; the message includes the values of the strings
    #   op (operator), lt (left type) and rt (right type)
    # An example call (from my __add__ method), which checks whether the type of
    #   right is a Rational or int is...
    # Rational._validate_arithmetic(right, {Rational,int},'+','Rational',type_as_str(right))
    def _validate_arithmetic(v : object, t : {type}, op : str, left_type : str, right_type : str):
        if type(v) not in t:
            raise TypeError('unsupported operand type(s) for '+op+
                            ': \''+left_type+'\' and \''+right_type+'\'')        

    @staticmethod
    # Called as Rational._validate_relational(..); static, so no self parameter
    # Helper method raises exception with appropriate message if type(v) is not
    #   in the set of types t; the message includes the values of the strings
    #   op (operator), and rt (right type)
    def _validate_relational(v : object, t : {type}, op : str, right_type : str):
        if type(v) not in t:
            raise TypeError('unorderable types: '+
                            'Rational() '+op+' '+right_type+'()') 
                   

   # Put all other methods here
    def __init__(self, numerator=0, denominator=1):
        assert type(numerator) is int, 'Rational.__init__ numerator is not int: '+str(numerator)+''
        assert type(denominator) is int, 'Rational.__init__ denominator is not int: '+str(denominator)+''
        assert denominator != 0, 'Rational.__init__ denominator is not int: '+str(denominator)+''
        if numerator == 0:
            self.num, self.denom = 0, 1
        if numerator != 0 and denominator < 0:
            gcd = Rational._gcd(abs(numerator), abs(denominator))
            self.num, self.denom = -(numerator//gcd), -(denominator//gcd)
        elif numerator != 0 and denominator > 0:
            gcd = Rational._gcd(abs(numerator), abs(denominator))
            self.num, self.denom = (numerator//gcd), (denominator//gcd)
        
    def __str__(self):
        return ''+str(self.num)+'/'+str(self.denom)+''
    
    def __repr__(self):
        return 'Rational('+str(self.num)+','+str(self.denom)+')'
    
    def __bool__(self):
        return self.num != 0

    def __neg__(self):
        return Rational(-self.num, self.denom)
    
    def __pos__(self):
        return Rational(self.num, self.denom)
    
    def __abs__(self):
        return Rational(abs(self.num), self.denom)
    
    def __getitem__(self, index):
        if type(index) not in [int, str]:
            raise TypeError('Rational.__getitem__ index('+str(index)+') is not an int or str')
        elif type(index) is int:
            if index == 0: return self.num
            elif index == 1: return self.denom
            else:
                raise TypeError('Rational.__getitem__ index('+str(index)+') is not a valid int (0 or 1)')
        else:
            if index.lower() in 'numerator' and len(index) >= 1: return self.num
            elif index.lower() in 'denominator' and len(index) >= 1: return self.denom
            else:
                raise TypeError('Rational.__getitem__ index('+str(index)+') is not a valid str (not prefix of numerator or denominator')
    
    def __add__(self, right):
        Rational._validate_arithmetic(right, {Rational,int},'+','Rational',type_as_str(right))
        if type(right) is int:
            right = Rational(right, 1)
        return Rational(((self.num*right.denom)+(right.num*self.denom)), (self.denom * right.denom))
            
    
    def __radd__(self, left):
        Rational._validate_arithmetic(left, {Rational,int},'+','Rational',type_as_str(left))
        if type(left) is int:
            left = Rational(left, 1)
        return Rational(((self.num*left.denom)+(left.num*self.denom)), (self.denom))
    
    def __sub__(self, right):
        Rational._validate_arithmetic(right, {Rational,int},'-','Rational',type_as_str(right))
        if type(right) is int:
            right = Rational(right, 1)
        return Rational(((self.num*right.denom)-(right.num*self.denom)), (self.denom * right.denom))
    
    def __rsub__(self, left):
        Rational._validate_arithmetic(left, {Rational,int},'-','Rational',type_as_str(left))
        if type(left) is int:
            left = Rational(left, 1)
        return Rational(((left.num*self.denom)-(self.num*left.denom)), (self.denom))
    
    def __mul__(self, right):
        Rational._validate_arithmetic(right, {Rational,int},'*','Rational',type_as_str(right))
        if type(right) is int:
            right = Rational(right, 1)
        return Rational((self.num*right.num),(self.denom * right.denom))
    
    def __rmul__(self, left):
        Rational._validate_arithmetic(left, {Rational,int},'*','Rational',type_as_str(left))
        if type(left) is int:
            left = Rational(left, 1)
        return Rational((self.num*left.num),(self.denom))
    
    def __truediv__(self, right):
        Rational._validate_arithmetic(right, {Rational,int},'/','Rational',type_as_str(right))
        if type(right) is int:
            right = Rational(right, 1)
        return Rational((self.num*right.denom), (self.denom*right.num))
    
    def __rtruediv__(self, left):
        Rational._validate_arithmetic(left, {Rational,int},'/','Rational',type_as_str(left))
        if type(left) is int:
            left = Rational(left, 1)
        return Rational((left.num*self.denom), (self.num))
    
    def __pow__(self, right):
        if type(right) is not int:
            raise TypeError('Rational.__pow__ power('+str(right)+') is not of type int')
        if right > 0:
            return Rational((self.num**right),(self.denom**right))
        elif right < 0:
            return Rational((self.denom**-right),(self.num**-right))
        elif right == 0:
            return Rational(1, 1)
        
    def __eq__(self, right):
        Rational._validate_relational(right, {Rational,int}, '==', type_as_str(right))
        if type(right) is int:
            right = Rational(right, 1)
        return (self.num == right.num and self.denom == right.denom)
    
    def __lt__(self, right):
        Rational._validate_relational(right, {Rational,int}, '<', type_as_str(right))
        if type(right) is int:
            right = Rational(right, 1)
        return (self.num/self.denom) < (right.num/right.denom)
    
    def __le__(self, right):
        Rational._validate_relational(right, {Rational,int}, '<=', type_as_str(right))
        if type(right) is int:
            right = Rational(right, 1)
        return (self.num/self.denom) <= (right.num/right.denom)
    
    def __gt__(self, right):
        Rational._validate_relational(right, {Rational,int}, '>', type_as_str(right))
        if type(right) is int:
            right = Rational(right, 1)
        return (self.num/self.denom) > (right.num/right.denom)
    
    def __ge__(self, right):
        Rational._validate_relational(right, {Rational,int}, '>=', type_as_str(right))
        if type(right) is int:
            right = Rational(right, 1)
        return (self.num/self.denom) >= (right.num/right.denom)
    
    def __call__(self, num_digits):
        if type(num_digits) is not int:
            raise TypeError('Rational.__call__ num_digits('+str(num_digits)+') is not of type int')
        integer_part = self.num//self.denom
        if num_digits == 0: return '{}'.format(integer_part)
        dividend = (self.num % self.denom) * 10
        decimals = ''
        while len(decimals) < num_digits:
            if self.denom > dividend:
                dividend *= 10
                decimals += '0'
            else:
                decimal = dividend//self.denom
                decimals += '{}'.format(decimal)
                remainder = dividend % self.denom
                dividend = remainder * 10
        return '{}.{}'.format(integer_part, decimals)
    
    def __setattr__(self, name, value):
        if name not in self.__dict__ and (name == 'num' or name == 'denom'):
            self.__dict__[name] = value
        else:
            raise NameError('Rational.__setattr__ attribute('+str(name)+') cannot be changed/created')
        
                    
# e ~ 1/0! + 1/1! + 1/2! + 1/3! + ... + 1/n!
def compute_e(n):
    answer = Rational(1)
    for i in irange(1,n):
        answer += Rational(1,math.factorial(i))
    return answer

# Newton: pi = 6*arcsin(1/2); see the arcsin series at http://mathforum.org/library/drmath/view/54137.html
# Check your results at http://www.geom.uiuc.edu/~huberty/math5337/groupe/digits.html
#   also see http://www.numberworld.org/misc_runs/pi-5t/details.html
def compute_pi(n):
    def prod(r):
        answer = 1
        for i in r:
            answer *= i
        return answer
    
    answer = Rational(1,2)
    x      = Rational(1,2)
    for i in irange(1,n):
        big = 2*i+1
        answer += Rational(prod(range(1,big,2)),prod(range(2,big,2)))*x**big/big       
    return 6*answer


if __name__ == '__main__':
    #Run simple tests before running driver

    x = Rational(8,29) 
    #print(x+x)
    #print(2*x)
    #print(x(30))
    
    print()
    import driver    
    driver.default_file_name = 'bscp22S19.txt'
#     driver.default_show_exception=True
#     driver.default_show_exception_message=True
#     driver.default_show_traceback=True
    driver.driver()
