import sys
import microseconds as ms

class BrainFuck:
    def __init__(self, code=None, input_=None):
        """ Initializes i/o, pointer and tape.
        """
        # define instruction set
        self.instruction_set = {'>': self.gt,
                                '<': self.lt,
                                '+': self.pls,
                                '-': self.min,
                                '.': self.dot,
                                ',': self.comma,
                                '[': self.lbracket,
                                ']': self.rbracket}
        # simulate cells with a list
        self.tape = [0] * (2 ** 15)

        # set the data pointer
        self.ptr = 0

        # set up stack to match brackets
        self.bracket_stack = []

        # set program counter
        self.pc = 0

        # initialize input buffer and output buffer
        self.input = input_
        self.input_counter = 0
        self.output = []

        # makes code a class variable
        if code:
            self.code = code
        else:
            self.code = list(sys.argv[1])

        # run the code
        self.duration = ms.microseconds()
        self.eval_bf()
        self.duration = ms.microseconds() - self.duration

    def eval_bf(self):
        """ Runs the brainfuck code. """
        while self.pc < len(self.code):
            if ms.microseconds() - self.duration > 500:
                return
            instruction = self.code[self.pc]
            self.instruction_set[instruction]()
            self.pc += 1

    def gt(self, times=1):
        """ Performs a '>', greater-than.
        Increases the data pointer (next cell to the right). """
        if self.ptr >= 2 ** 15 - 1:
            # raise ValueError("Segmentation fault! (pointer greater than tape)")
            return
        self.ptr += 1 * times

    def lt(self, times=1):
        """ Performs a '<', lower-than.
        Decreases the data pointer (previous cell to the left). """
        if self.ptr <= 0:
            # raise ValueError("Segmentation fault! (pointer lower than tape)")
            return
        self.ptr -= 1 * times

    def pls(self, times=1):
        """ Performs a '+', plus.
         Increments the byte at the pointer.
         '% 256' is done to be sure the byte stays in range 0, 255. On overflow, it goes to 0. """
        self.tape[self.ptr] = (self.tape[self.ptr] + 1 * times) % 256

    def min(self, times=1):
        """ Performs a '-', minus.
         Decrements the byte at the pointer.
        '% 256' is done to be sure the byte stays in range 0, 255. On underflow, it goes to 255. """
        self.tape[self.ptr] = (self.tape[self.ptr] - 1 * times) % 256

    def dot(self, times=1):
        """ Performs a '.', dot.
        Outputs the byte at the pointer (in ASCII)."""
        # sys.stdout.write(chr(self.tape[self.ptr]))
        self.output.append(self.tape[self.ptr])

    def comma(self, times=1):
        """ Performs a ',', comma.
        Replaces byte at the pointer with input. """
        self.tape[self.ptr] = self.input[self.input_counter]
        self.input_counter += 1

    def lbracket(self, times=1):
        if self.tape[self.ptr] == 0:
            nested_loops = 0
            while self.pc < len(self.code):
                self.pc += 1
                if self.code[self.pc] == '[':
                    nested_loops += 1
                if self.code[self.pc] == ']':
                    if nested_loops == 0:
                        return
                    else:
                        nested_loops -= 1

    def rbracket(self, times=1):
        if self.tape[self.ptr] != 0:
            nested_loops = 0
            while self.pc >= 0:
                self.pc -= 1
                if self.code[self.pc] == ']':
                    nested_loops += 1
                if self.code[self.pc] == '[':
                    if nested_loops == 0:
                        return
                    else:
                        nested_loops -= 1

if __name__ == '__main__':
    testcode = list(",++[++.>,+[<")
    testinput = [1, 4]
    output = BrainFuck(input_=testinput, code=testcode)
    for number in output.output:
        print(int(number))
