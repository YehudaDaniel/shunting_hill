from abc import ABC
from numpy import double
from abc import ABC,abstractmethod

class Expression(ABC):
    @abstractmethod
    def calc(self)->double:
        pass

# implement the classes here
#Num class
class Num(Expression):
    def __init__(self, x:int)-> None:
        super().__init__()
        self.x = x
    def calc(self)->double:
        return self.x
    
#BinExp class
class BinExp(Expression):
    def __init__(self, left:Expression, right:Expression)-> None:
        super().__init__()
        self.left = left
        self.right = right
#Plus class
class Plus(BinExp):
    def __init__(self, left:Expression, right:Expression)-> None:
        super().__init__(left, right)
    
    def calc(self)->double:
        return self.left.calc() + self.right.calc()
#Minus class
class Minus(BinExp):
    def __init__(self, left:Expression, right:Expression)-> None:
        super().__init__(left, right)
    def calc(self)->double:
        return self.left.calc() - self.right.calc()
#Mul class
class Mul(BinExp):
    def __init__(self, left:Expression, right:Expression)-> None:
        super().__init__(left, right)
    def calc(self)->double:
        return self.left.calc() * self.right.calc()
#Div class
class Div(BinExp):
    def __init__(self, left:Expression, right:Expression)-> None:
        super().__init__(left, right)
    def calc(self)->double:
        return self.left.calc() / self.right.calc()

#implement the parser function here
def parser(expression)->double:
    def is_operator(c):
        return c == '+' or c == '-' or c == '*' or c == '/'
    
    #define operator precedence
    precedence = {'+':1, '-':1, '*':2, '/':2}
    negFlag = False
    isNeg = False
    stack = []
    queue = []
    result = 0
    for c in expression:
        if c == '(':
            isNeg = True
            stack.append(c)
        elif c == ')':
            while len(stack) > 0 and stack[len(stack) - 1] != '(':
                queue.append(stack.pop())
            stack.pop()
        elif is_operator(c):
            if c == '-' and (len(stack) > 0 and stack[len(stack) - 1] == '(') and isNeg: #negative number
                negFlag = True
                continue
            while len(stack) > 0 and is_operator(stack[len(stack) - 1]) and precedence[stack[len(stack) - 1]] >= precedence[c]:
                queue.append(stack.pop())
            stack.append(c)
        else: #is a number
            if negFlag and isNeg:
                queue.append('-' + c)
                negFlag = False
                isNeg = False
            #if the last element in the queue is a number, append the current number to it
            elif len(queue) > 0 and not is_operator(queue[len(queue) - 1]) and stack[len(stack) - 1] == '(':
                queue[len(queue) - 1] += c
            else:
                queue.append(c)
    #pop the rest of the stack to the queue ~ last step
    while len(stack) > 0:
        queue.append(stack.pop())
        
    nums = []
    for q in queue:
        if not is_operator(q):
            if negFlag:
                nums.append((-1)*int(q))
                negFlag = False
            nums.append(q)
        if q == '+':
            result = Plus(Num(int(nums.pop())), Num(int(nums.pop()))).calc()
            nums.append(result)
        elif q == '-':
            result = Minus(Num(int(nums.pop())), Num(int(nums.pop()))).calc()
            nums.append((-1)*result)
        elif q == '*':
            result = Mul(Num(int(nums.pop())), Num(int(nums.pop()))).calc()
            nums.append(result)
        elif q == '/':
            result = Div(Num(int(nums.pop())), Num(int(nums.pop()))).calc()
            nums.append(1/result)
            
    return nums.pop()