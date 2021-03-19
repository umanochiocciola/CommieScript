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



def setline(lin):
    global line
    line = lin
    
def interp(line):
    #print(line)
    global variables

    riga = program[line].replace('\n', '')
    riga = riga.split('#')[0]    #comments
    
    for piece in riga.split(' ' + variables.get('_LINE_SEPARATOR', 'THEN') + ' '):
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
            try:
                exec(f'OUR_{keyword}({args})')
            except:
                error(line, f'invalid sintax, comrade.')
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
#

def OUR_fuck(var):
    if not var in variables:
        error(line, f'the glorious republic doesn\'t have such variable: {var}')
    variables.pop(var)
#

def OUR_listall(dummy='', var=''):
    if dummy = 'return':
        variables[var] = variables
    else:
        for i in variables:
            print(f'{i}: {repr(variables[i]) if type(variables[i])==type("") else variables[i]}')
    

################################################# functions
def OUR_run(target):
    global line, PopLine
    
    PopLine = line
    
    try:
        line = int(funcs[target]) # without -1 because we don't want to exec OUR_work again
    except:  error(line, f'argument must be a declared "work"')
#

def OUR_endwork(dummy='just because you always have an argument don\'t know why :|'):
    global line, PopLine, EXECUTING
    if PopLine==0:
        PopLine = line

    line = PopLine

def OUR_work(name):
    global funcs, line, EXECUTING
    funcs[name] = line
    EXECUTING = 0
    

###############################################################

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

variables = {
    '_LINE_SEPARATOR': 'THEN',
}
funcs = {}

line = 0
PopLine = 0
EXECUTING = 1
while line < len(program):
    #print(program[line].split(' ')[0].split('#')[0].replace('\n', ''))
    #print(EXECUTING)
    
    if EXECUTING: interp(line)
    elif program[line].split(' ')[0].split('#')[0].replace('\n', '')=='endwork': EXECUTING = 1
    line += 1
