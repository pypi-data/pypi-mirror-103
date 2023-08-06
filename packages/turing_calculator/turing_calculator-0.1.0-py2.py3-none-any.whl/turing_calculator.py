''' Simple calculator in python'''

__version__ = "0.1.0"

class Calculator:
    ''' Simple calculator (+, -, ×, ÷, nth root)
    
        For example:
            >>> calc = Calculator()
            >>> calc.add(2)
            >>> calc.multiply(3)
            >>> calc.val
            6.0
    '''
    def __init__(self):
        self.val = 0.0
    
    def reset(self):
        ''' Reset current value to zero
            For example:
                >>> calc = Calculator()
                >>> calc.add(10)
                >>> calc.reset()
                >>> calc.val
                0.0
        '''
        self.val = 0.0
    
    def add(self, n: float):
        ''' Add n to current value
            For example:
                >>> calc = Calculator()
                >>> calc.add(4)
                >>> calc.val
                4.0
        '''
        self.val += n
    
    def subtract(self, n: float):
        ''' Subtract n from current value
            For example:
                >>> calc = Calculator()
                >>> calc.subtract(4)
                >>> calc.val
                -4.0
        '''
        self.val -= n

    def multiply(self, n: float):
        ''' Multiply current value by n
            For example:
                >>> calc = Calculator()
                >>> calc.add(3)
                >>> calc.multiply(2)
                >>> calc.val
                6.0
        '''
        self.val *= n
    
    def divide(self, n: float):
        ''' Divide current value by n
            For example:
                >>> calc = Calculator()
                >>> calc.add(10)
                >>> calc.divide(5)
                >>> calc.val
                2.0
        '''
        if n == 0:
            raise ZeroDivisionError(n)
        self.val /= n
    
    def root(self, n: float):
        ''' Calculate nth root of current value
            For example:
                >>> calc = Calculator()
                >>> calc.add(125)
                >>> calc.root(3)
                >>> calc.val
                5.0
        '''
        if self.val < 0:
            raise NegativeRootError(n)
        elif n == 0:
            raise ZeroDivisionError(n)
        self.val **=(1 / n)
        
class NegativeRootError(ValueError):
    '''Custom Error for when user tries to find the nth root of a negative number'''
    pass