import sys
import string

class Syntax:
    def _gt(self, digits=1):
        """ Performs a '>', lower-than.
        Increases the data pointer (next cell to the right). """
        if self.ptr >= 3*10**4 - 1:
            raise ValueError("Segmentation fault! (pointer lower than tape")
        self.ptr += 1 * digits

    def _lt(self, digits=1):
        """ Performs a '<', lower-than.
        Decreases the data pointer (previous cell to the left). """
        if self.ptr <= 0:
            raise ValueError("Segmentation fault! (pointer greater than tape")
        self.ptr -= 1 * digits

    def _pls(self, digits=1):
        """ Performs a '+', plus.
         Increments the byte at the pointer.
         '% 256' is done to be sure the byte stays in range 0, 255. On overflow, it goes to zero """
        self.tape[self.ptr] = (self.tape[self.ptr] + 1 * digits) % 256

    def _min(self, digits=1):
        """ Performs a '-', minus.
         Decrements the byte at the pointer.
        '% 256' is done to be sure the byte stays in range 0, 255. On underflow, it goes to 255 """
        self.tape[self.ptr] = (self.tape[self.ptr] - 1 * digits) % 256

    def _dot(self, digits=1):
        """ Performs a '.', dot.
        Outputs the byte at the pointer (in ASCII)."""
        #sys.stdout.write(chr(self.tape[self.ptr]))
        self.output.append(self.tape[self.ptr])

    def _comma(self, bfinput, digits=1):
        """ Performs a ',', comma.
        Replaces byte at the pointer with input.
        No ctrl-z (ASCII-26), because the user should be able to quit"""
        if self.test:
            c = sys.stdin.read(1)
            if c in string.digits:
                c = int(c)
            else:
                c = ord(c)
        else:
            c = bfinput
        if c != 26:
            self.tape[self.ptr] = c
