#!/usr/bin/python
'''
Created on Jul 5, 2015

@author: luodichen
'''

import sys

class BrMemoryError(Exception):
    pass

class BrNotMatch(Exception):
    pass

class Machine(object):
    def __init__(self):
        self.code = []
        self.memory = [0, ]
        self.stack = []
        self.cp = 0
        self.mp = 0
        self.vector = {}
        
    def ck_mp(self):
        if self.mp < 0 or self.mp >= len(self.memory):
            raise BrMemoryError("halt: cannot access address %d.\n" % (self.mp, ))
        return self.mp
        
    def next(self):
        self.mp += 1
        if len(self.memory) == self.mp:
            self.memory.append(0)
    
    def back(self):
        self.mp -= 1
        
    def vplus(self):
        self.memory[self.ck_mp()] += 1
        
    def vminus(self):
        self.memory[self.ck_mp()] -= 1
        
    def output(self):
        sys.stdout.write(chr(self.memory[self.ck_mp()]))
    
    def input(self):
        self.memory[self.ck_mp()] = ord(sys.stdin.read(1))
        
    def jumpforward(self):
        if 0 == self.memory[self.mp]:
            self.cp = self.vector[self.cp]
        else:
            self.stack.append(self.cp)
        
    def jumpback(self):
        if 0 != self.memory[self.mp]:
            self.cp = self.stack[-1]
        else:
            self.stack.pop()
            
    def load(self, source):
        self.code = [c for c in open(source).read() if c in "><+-.,[]"]
        vtstack = []
        index = 0
        
        for c in self.code:
            if '[' == c:
                vtstack.append(index)
            elif ']' == c:
                if 0 == len(vtstack):
                    raise BrNotMatch("] not matched at %d" % (index, ))
                self.vector[vtstack.pop()] = index
            index += 1
        
        if 0 != len(vtstack):
            raise BrNotMatch("[ not matched at %d" % (vtstack.pop(), ))
        
    def run(self):
        while self.cp < len(self.code):
            {
                '>':self.next, '<': self.back, '+':self.vplus, '-':self.vminus,
                '.':self.output, ',':self.input, 
                '[':self.jumpforward, ']':self.jumpback
            }[self.code[self.cp]]()
            self.cp += 1

def main(argv):
    if len(argv) > 1:
        m = Machine()
        m.load(argv[1])
        m.run()
    else:
        sys.stderr.write("where is the source file?\n")
        sys.exit(1)
    
if "__main__" == __name__:
    main(sys.argv)
