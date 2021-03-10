## interpreter
import sys
import os


def error(line, mof):
    print(f'error at line {line+1}:\n{mof}')
    exit(1)

def spaces_only(boi):
    for i in boi:
        if i != ' ':
            return 0
    return 1
#


def parse(st):
    #print(variables)
    a = []
    for i in st.split():
        if i[0] == ';':
            if i.replace(';', '') in variables:
                j = repr(variables[i.replace(';', '')])
            else: error(line, f'the glorious republic doesn\'t have such variable: {i.replace(";", "")}')
        else: j = i
        a.append(str(j))
    
    #print('fff' + ' '.join(a))
    return ' '.join(a)


def interp(line):
    #print(line)
    global variables

    piece = program[line].replace('\n', '')
    piece = piece.split('#')[0]    #comments
    
    keyword = piece.split(' ')[0]
    
    
    if piece == '' or spaces_only(piece):
        return
    
    if keyword == 'our' or keyword in variables:
        boi = piece.split(' = ')
        if len(boi) != 2:
            error(line, 'invalid variable declaration')
        
        name = boi[0].replace('our ', '')
        variables[name] = eval(parse(boi[1]))
    
    else:
        #try:
        pis = piece.replace(f'{keyword} ', '').split(', '); #print(pis, keyword)
        #pis.remove(keyword)
        
        args = []
        for i in pis:
            if i != '': args.append(f'"{parse(i)}"') 
            else: continue


        args = ', '.join(args)
        #print(args)
        #try
        exec(f'OUR_{keyword}({args})')
        #except:
        #    error(line, f'an error occurred while executing this, comrade.')
#
###########################################################
##          OUR FUNCTIONS

def OUR_():
    ## so spaces only
    0

def OUR_strike(what):
    what = what.strip(' ').strip('\t')
    if what == '':
        error(line, "to announce something to the masses, use:\n\tstrike string_variable")
    
    if not(what in variables):
        error(line, f'the glorious republic doesn\'t have such variable: {what} and therefore can\'t announce it to the masses')
    
    print(variables[what], end='')
#
def OUR_get(to, typ='str'):
    global variables
    to = to.replace(',','')
    
    a = input()
    try:
        variables[to] = eval(f'{typ}("{a}")')
    except:
        error(line, f'your input couldn\'t be converted to {typ}, sorry comrade')
#

def OUR_goto(target, condition=1):
    global line
    if eval(parse(condition)):
        try:
            line = int(target)-1
        except:  error(line, f'line argument must be a natural number, obviously')
#
    

def OUR_append(var, what, typ='str'):
    global variables
    if not(var in variables):
        error(line, f'the glorious republic doesn\'t have such variable: {var}')
    if not(type(variables[var])==type([])):
        error(line, f'item can be used only on lists')
    
    try: what=eval(f'{typ}({what})')
    except: error(line, f'{typ} is not a valid type or {what} (type {type(what)}) can\'t be converted to {typ}')
    variables[var].append(what)

####################################################



if len(sys.argv) < 2:
    print('missing argument: file'); exit(1)

file = sys.argv[1]

try:
    with open(file, 'r') as f:
        program = f.readlines()
except:
   print(f'{file} not found in our glorious republic');exit(1)
#

variables = {}

line = 0
while line < len(program):
    interp(line)
    line += 1