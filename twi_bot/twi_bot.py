# coding: utf-8
import parser

# event loop
# uniti

def runtime_load(filename):
    with open(filename) as f:
        bytecode = parser.suite(f.read()).compile()
        eval(bytecode)
        code ()

b'd\x00\x00Z\x00\x00d\x01\x00d\x02\x00\x84\x00\x00Z\x01\x00e\x02\x00d\x03\x00\x83\x01\x00\x01d\x04\x00S'
runtime_load('example_rule.py')

print(b)
print(function())
