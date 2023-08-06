import os

def Statement_Writeln(text):
    print(text)


def Statement_Write(text):
    print(text, end='')


def If_these_equals_then(thing, thatthing, function_if):
    if thing == thatthing:
        function_if()


def WhenREALrun(function_while):
    while True:
        function_while()


def Loop_func_inRange(range_capacity, function_range):
    for i in range(int(range_capacity)):
        function_range()
    
def Code_Rewrite_with(fro ,code, rewritten):
    rewritten = fro.replace(code, rewritten)
    return rewritten


def Reverse_text(needed_to_reverse):
    needed_to_reverse = needed_to_reverse[::-1]
    return needed_to_reverse

def User_Input_Get(getting):
    getting = input(getting)
    return getting

def intTOstring(codes):
    codes = str(codes)
    return codes

def stringToint(codek):
    codek = int(codek)
    return codek


def Init_op_System(command):
    os.system(command)
