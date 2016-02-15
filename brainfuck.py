import sys
import string
import VanillaBF
from datetime import datetime

def microseconds():
    current_time = datetime.now()
    current_time = current_time.microsecond \
                   + current_time.second * 1000000 \
                   + current_time.minute * 1000000 * 60 \
                   + current_time.hour * 1000000 * 60 * 60 + current_time.day * 1000000 * 60 * 60 * 24
    return current_time


class brainfuck:

    def __init__(self, code, test=False, bfinput=0):
        # primitives which can directly be handled
        self.dictionary = {'>': VanillaBF.Syntax._gt,
                           '<': VanillaBF.Syntax._lt,
                           '+': VanillaBF.Syntax._pls,
                           '-': VanillaBF.Syntax._min,
                           '.': VanillaBF.Syntax._dot,
                           ',': VanillaBF.Syntax._comma}
        # simulate the cells with a list
        self.tape = [0]*(3*10**4)
        # the data pointer
        self.ptr = 0
        #determine if run as by pc or manual (=True)
        self.test = test
        self.bfinput = bfinput
        self.output = []
        self.__eval_bf(code)

    def __eval_bf(self, code):
        # get '[' and ']' scopes
        loop = self.__parse(code)
        # initialize program counter
        pc =0
        # stack to store pc for loops
        stack = []
        # save time to variable
        start_time = microseconds()
        while pc < len(code):
            if microseconds() - start_time > 1000 and not self.test:
                raise(ValueError("Too long!"))
            instruction = code[pc]
            # handle directly
            if instruction in self.dictionary:
                function_to_call = self.dictionary[instruction]
                if function_to_call.__name__ == '_comma':
                    function_to_call(self, self.bfinput)
                else:
                    function_to_call(self)
            elif instruction in string.digits:
                i = 1
                digits = [instruction]
                while code[pc + i] in string.digits:
                    digits.append(code[pc + i])
                    i += 1
                else:
                    if code[pc + i] in '[,]':
                        raise ValueError("Cant multiply loops")
                    self.dictionary[code[pc + i]](self, int(''.join(map(str, digits))))
                    pc += i
            elif instruction == "[":
                # if loop condition is fulfilled
                # enter loop block
                if self.tape[self.ptr] > 0:
                    stack.append(pc)
                else: # else go to the end of the block
                    pc = loop[pc]
            elif instruction == "]":
                # jump back where you came from!
                pc = stack.pop() - 1
            pc += 1
        self.time = microseconds() - start_time

    def __parse(self, code):
        """ maps the "["s to the corresponding "]"s """
        # stack to contain the indices of the opening brackets
        opening = []
        # dict which maps the indices of the opening brackets
        # to the closing brackets
        loop = {}
        for i, c in enumerate(code):
            if c == "[":
                opening.append(i)
            elif c == "]":
                try:
                    begin = opening.pop()
                    loop[begin] = i
                except IndexError:
                    raise ValueError("Supplied string isn't balanced, too many ]s!")
        # if the stack isn't empty, the string cannot be balanced
        if opening:
            raise ValueError("Supplied string isn't balanced, too many [s")
        else:
            return loop

if __name__ == '__main__':
    code = '10+[>7+>10+>3+>+4<-]>++3.>+.7+..3+.>++.<<15+.>.3+.6-.8-.>+.>.'
    code = '54,..,113,-'
    code = sys.argv[1]
    program = brainfuck(code, test=True)
    print(program.output)
    print(program.time)
