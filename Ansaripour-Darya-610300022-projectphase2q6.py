import re
import copy

def char_to_num(char):
    num=ord(char)-ord('A')+1
    return(num)

def string_to_num(string):
    num=0
    p=26**(len(string))
    for char in string:
        p//=26
        num+=char_to_num(char)*p
    return(num)


def num_to_char(num):
    char=chr(num+ord('A')-1)
    return(char)

def num_to_string(num):
    string=''
    r=0
    while num>0 :
        r=num%26
        if r==0:
            string+='Z'
            num-=1
        else:
            string+=num_to_char(r)
        num//=26
    return(string[::-1])

def evalStr1(string):
    pattern=re.compile(r"(\d+)([*/+\-])(\d+)")
    matches=list(pattern.finditer(string))
    if matches[0].group(2)=="+":
        return(int(float(matches[0].group(1))+float(matches[0].group(3))))
    elif matches[0].group(2)=="-":
        return(int(float(matches[0].group(1))-float(matches[0].group(3))))
    elif matches[0].group(2)=="*":
        return(int(float(matches[0].group(1))*float(matches[0].group(3))))
    elif matches[0].group(2)=="/":
        return(int(float(matches[0].group(1))/float(matches[0].group(3))))


def checkmatch(string):
    p0=re.compile(r"(\d+)\s*([+\-])\s*(\")([A-Z]+)(\")\s*")
    p1=re.compile(r"(\")([A-Z]+)(\")\s*([+\-])\s*(\d+)\s*")
    p2=re.compile(r"(\d+\.?\d*)\s*([+\-])\s*(\d+\.?\d*)\s*")
    p3=re.compile(r"(\")(.*)(\")\s*(\+)\s*(\")(.*)(\")\s*")
    if re.search(p0, string):
        matches=list(p0.finditer(string))
        if matches[0].group(2)=="+":
            return(str(string_to_num(matches[0].group(4))-1+int(matches[0].group(1))))
        else:
            return(str(int(matches[0].group(1))-(string_to_num(matches[0].group(4))-1)))

    elif re.search(p1, string):
        matches=list(p1.finditer(string))
        if matches[0].group(4)=="+":
            return("\""+num_to_string(string_to_num(matches[0].group(2))-1+int(matches[0].group(5))+1)+"\"")
        else:
            return("\""+num_to_string(string_to_num(matches[0].group(2))-1-int(matches[0].group(5))+1)+"\"")
        
    
    elif re.search(p2, string):
        matches=list(p2.finditer(string))
        if matches[0].group(2)=="+":
            return(int(float(matches[0].group(1))+float(matches[0].group(3))))
        elif matches[0].group(2)=="-":
            return(int(float(matches[0].group(1))-float(matches[0].group(3))))


    elif re.search(p3, string):
        matches=list(p3.finditer(string))
        return("\""+str(matches[0].group(2))+str(matches[0].group(6))+"\"")

    else:
        return("unsupported operand")


def evalStr(string):
    pattern1=re.compile(r"(\s*\"?[^\"\-+*/]*\"?\s*[+\-]\s*\"?[^\"\-+*/]*\"?\s*)")
    anspattern=re.compile(r"(\"?-?[^\"\-+*/]+\"?)")
    while re.search(r"\d+[*/]\d+", string):
        pattern=re.compile(r"\d+[*/]\d+")
        matches=list(pattern.finditer(string))
        pat=matches[0].group(0)
        string=re.sub(r"\d+[*/]\d+", str(evalStr1(pat)), string, 1)

    ansmatches=list(anspattern.finditer(string))
    if ansmatches[0].group(1)==string:
        return(string)

    matches=list(pattern1.finditer(string))
    res=checkmatch(str(matches[0].group(1)))
    string=string.replace(str(matches[0].group(1)),'',1)
    string=str(res)+string
    return(evalStr(string))


########################### CODE HAYE MARBUT BE EVALSTR2, BARAYE MOHASEBE KAFIST evalStr() RA SEDA BEZANID #######################


def listString(string):
    i=0
    l=[]
    substr=''
    while i<len(string):

        if re.search(r'[*+/\-\[\]]' , string[i]):
            l.append(string[i])
            substr=''
            i+=1
            
        else:
            while i<len(string) and not re.search(r'[*+/\-\[\]]' , string[i]):
                substr+=string[i]
                i+=1
            l.append(substr)
    return(l)


def checkmatch2(string, matrix=[[]]):
    p0=re.compile(r'^\s*([A-Z]+)(\d+)\s*$')
    p1=re.compile(r'^\s*([a-z]+[^/*+\-\" ]*)\s*$')
    n=len(matrix)
    m=len(matrix[0])

    if re.search(p0, string):
        matches=list(p0.finditer(string))
        
        if int(matches[0].group(2))-1<n and int(string_to_num(matches[0].group(1)))-1<m:
            return(matrix[int(matches[0].group(2))-1][int(string_to_num(matches[0].group(1)))-1])
        else:
            return("unsupported operand")
    
    elif re.search(p1, string):
        matches=list(p1.finditer(string))

        if matches[0].group(1) in variables:
            return(variables[matches[0].group(1)])
        else:
            return("unsupported operand")

    else:
        return(string)



def evalStr3(string, matrix=[[]]):
    n=len(matrix)
    m=len(matrix[0])
    l=listString(string)
    l2=[]*len(l)

    evaluated=''
    for something in l:
        if not  re.search(r'[*+/\-\[\]]' , something):
            l2.append(checkmatch2(something, matrix))
        else:
            l2.append(something)
    

    for substr in l2:
        evaluated+=str(substr)


    while re.search(r'\[\s*([^\[\]]+)\s*\]\[\s*([^\[\]]+)\s*\]', evaluated):
        
        cellpat=re.compile(r'\[\s*([^\[\]]+)\s*\]\[\s*([^\[\]]+)\s*\]')
        matches=list(cellpat.finditer(evaluated))
        
        i=int(evalStr(matches[0].group(2)))-1
        j=string_to_num(evalStr(matches[0].group(1))[1:-1])-1
        if i<n and j<m:
            evaluated=re.sub(cellpat, matrix[i][j] , evaluated, 1)
        else:
            return("unsupported operand")

    return(evaluated)


def evalString(string, matrix=[[]]):
    return(evalStr(evalStr3(string, matrix)))

################################ CODE HAYE MARBUT BE EVALSTRING3, BARAYE MOHASEBE KAFIST evalString() RA SEDA BEZANID ###########################
def convert(string):
    try:
        num=int(string)
        return(num)
    except ValueError:
        return(string)



exppattern=re.compile(r'\s*([^<>=]+[^ =]*)\s*([<>=]+)\s*([^<>=]+[^ ]*)\s*')


def expCalc(string,matrix=[[]]): 
    if re.search(exppattern, string):
        matches=list(exppattern.finditer(string))
        exp1=evalString(matches[0].group(1),matrix)
        exp2=evalString(matches[0].group(3),matrix)
        if ("\"" in exp1 and "\"" in exp2) or ("\"" not in exp1 and "\"" not in exp2) and 'unsupported operand' not in exp1 and 'unsupported operand' not in exp2:
            exp1=convert(exp1)
            exp2=convert(exp2)
            if matches[0].group(2)=="<":
                return("true" if exp1<exp2 else "false")
            elif matches[0].group(2)==">":
                return("true" if exp1>exp2 else "false")
            else:
                return("true" if exp1==exp2 else "false")
        else:
            raise ValueError

    elif re.search(r'true', string):
        return("true")
    elif re.search(r'false', string):
        return("false")


def boolCalc(string,matrix=[[]]):
    
    pat1=re.compile(r'\s*(true|false|typeError)\s*')
    pat2=re.compile(r'\s*(and|or)\s*')
    pat3=re.compile(r'\s*(true|false)\s*(and|or)\s*(true|false)')
    patmatches=pat1.findall(string)

    if 'typeError' in string or patmatches[0]==string:
        if 'typeError' in string:
            return('typeError')
        else:
            return(string)
        
    
    pat1m=list(pat1.finditer(string))
    b1=pat1m[0].group(1)
    b2=pat1m[1].group(1)
    pat2m=list(pat2.finditer(string))
    l=pat2m[0].group(1)
    if l=='and':
        if b1=='true' and b2=='true':
            string=re.sub(pat3, 'true', string, 1)
            return(boolCalc(string,matrix))
        else:
            string=re.sub(pat3, 'false', string, 1)
            return(boolCalc(string,matrix))
    if l=='or':
        if b1=='true' or b2=='true':
            string=re.sub(pat3, 'true', string, 1)
            return(boolCalc(string,matrix))
        else:
            string=re.sub(pat3, 'false', string, 1)
            return(boolCalc(string,matrix))



def mainfunc(mylist,string,matrix=[[]]):
    mylist2=[]
    for exp in mylist:
        mylist2.append(expCalc(exp,matrix))

    for i in range(len(mylist)):
        string=string.replace(str(mylist[i]), str(mylist2[i]), 1)

    return(string)

def checkcondition(string, matrix=[[]]):
    andorpat=re.compile(r' and | or ')
    list1=re.split(andorpat, string)
    finalstring=mainfunc(list1, string)
    return(boolCalc(finalstring, matrix))

######################################## CODE HAYE MARBUT BE MOHASEBE EBARAT HAYE BOOLEAN, BARAYE MOHASEBE AZ checkcondition() ESTEFADE KONID###########################################

def display(mat):
    mat2=copy.deepcopy(mat)
    mat2=[[str(i+1)] + mat[i] for i in range(len(mat))]
    firstrow=[[str(0)]+[num_to_string(i) for i in range(1,len(mat2[0]))]]
    mat2=firstrow+mat2
    lens = [max(map(len, col)) for col in zip(*mat2)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in mat2]
    print('\n'.join(table))

def counter(lst,startind):
    c=1
    endind=startind

    for cmnd in lst:
        if c!=0:
            if "{" in cmnd:
                c+=1
            elif "}" in cmnd:
                c-=1
            endind+=1
        else:
            break
    return(endind)



class Table():
    def __init__(self, tablename, column, row):
        self.table=[['None' for _ in range(column)] for _ in range(row)]
        tables[tablename]=self

    def setcell(self, c, r, v):
        column=int(string_to_num(c))-1
        row=int(r)-1
        value=v
        self.table[row][column]=value

    def setFunc(self, c, r, formula):
        column=int(string_to_num(c))-1
        row=int(r)-1
        self.table[row][column]=formula

    def update(self):
        f=0
        updatedtable=copy.deepcopy(self.table)
        for i in range(len(updatedtable)):
            for j in range(len(updatedtable[i])):
                while re.search(cellpat2, updatedtable[i][j]):
                    matches1=list(cellpat2.finditer(updatedtable[i][j]))
                    i2=int(matches1[0].group(2))-1
                    j2=int(string_to_num(matches1[0].group(1)))-1
                    if self.table[i2][j2]=='None':
                        updatedtable[i][j]='None'
                        break
                    else:
                        f=1
                        updatedtable[i][j]=re.sub(cellpat2,  self.table[i2][j2], updatedtable[i][j], 1)
                if f==1:
                    updatedtable[i][j]=evalString(updatedtable[i][j], self.table)
                f=0
        return(updatedtable)
                    



tables={}
variables={}
currentTable=None

cellpat1=re.compile(r'\[\s*([^\[\]]+)\s*\]\[\s*([^\[\]]+)\s*\]')
cellpat2=re.compile(r'([A-Z]+)(\d+)\s*')

varassignpat=re.compile(r'^([a-z]+[^/*+\-\"= \[\]]*)\s*=\s*([^=]+)$')
cellassignpat1=re.compile(r'^\[\s*([^\[\]]+)\s*\]\[\s*([^\[\]]+)\s*\]\s*=\s*([^=]+)$')
cellassignpat2=re.compile(r'^([A-Z]+)(\d+)\s*=\s*([^=]+)$')
createpat=re.compile(r'^create\(([^,]+),(\d+),(\d+)\)$')
contextpat=re.compile(r'^context\((.+)\)$')
printpat=re.compile(r'^print\((.*)\)$')
displaypat=re.compile(r'^display\((.+)\)$')
setFuncpat=re.compile(r'^setFunc\(([^,]+),([^,]+)\)$')
whilepat=re.compile(r'^while\(([^\(\)]+)\)\{$')
ifpat=re.compile(r'^if\(([^\(\)]+)\)\{$')
commentpat=re.compile(r'\s*\$.*')


def readcommand(cmndlist):
    ind=-1
    for cmnd in cmndlist:
        ind+=1
        try:
            if re.search(whilepat, cmnd):
                startind=ind
                endind=counter(cmndlist[startind+1:], startind)
                newcmndlist=[command[4:] for command in cmndlist[startind+1:endind]]
                matches=list(whilepat.finditer(cmnd))
                condition=matches[0].group(1)
                while(checkcondition(condition)=="true"):
                    readcommand(newcmndlist)

            elif re.search(ifpat, cmnd):
                startind=ind
                endind=counter(cmndlist[startind+1:], startind)
                newcmndlist=[command[4:] for command in cmndlist[startind+1:endind]]
                matches=list(ifpat.finditer(cmnd))
                condition=matches[0].group(1)
                if(checkcondition(condition)=="true"):
                    readcommand(newcmndlist)

            elif re.search(createpat, cmnd):
                matches=list(createpat.finditer(cmnd))
                key=matches[0].group(1)
                column=int(matches[0].group(2))
                row=int(matches[0].group(3))
                table=Table(key, column, row)
                tables[key]=table

            elif re.search(contextpat, cmnd):
                global currentTable
                matches=list(contextpat.finditer(cmnd))
                currentTable=tables[matches[0].group(1)] 

            elif re.search(varassignpat, cmnd):
                matches=list(varassignpat.finditer(cmnd))
                key=matches[0].group(1)
                value=matches[0].group(2)
                if currentTable!=None:
                    newtable=currentTable.update()
                    variables[key]=evalString(value, newtable)
                else:
                    variables[key]=evalString(value)

            elif re.search(cellassignpat1, cmnd) or re.search(cellassignpat2, cmnd) :
                if re.search(cellassignpat1, cmnd):
                    newtable=currentTable.update()
                    matches=list(cellassignpat1.finditer(cmnd))
                    column=evalString(matches[0].group(1), newtable)[1:-1]
                    row=evalString(matches[0].group(2), newtable)
                    value=evalString(matches[0].group(3),  newtable)
                    currentTable.setcell(column,row,value)
                else:
                    newtable=currentTable.update()
                    matches=list(cellassignpat2.finditer(cmnd))
                    column=evalString(matches[0].group(1), newtable)
                    row=evalString(matches[0].group(2), newtable)
                    value=evalString(matches[0].group(3),  newtable)
                    currentTable.setcell(column,row,value)

            elif re.search(printpat, cmnd):
                matches=list(printpat.finditer(cmnd))
                if currentTable!=None:
                    newtable=currentTable.update()
                if matches[0].group(1)=="\"\"":
                    print("out:\"\"")
                else:
                    if re.search(cellpat1, matches[0].group(1)) or re.search(cellpat2, matches[0].group(1)):
                        out=evalString(matches[0].group(1), newtable)
                        print("out:",end="")
                        print(out)
                    else:
                        out=evalString(matches[0].group(1))
                        print("out:",end="")
                        print(out)

            elif re.search(setFuncpat, cmnd):
                matches=list(setFuncpat.finditer(cmnd))
                cell=matches[0].group(1)
                formula=matches[0].group(2)
                if re.search(cellpat1, cell):
                    matches=list(cellpat1.finditer(cmnd))
                    column=evalString(matches[0].group(1), currentTable.table)[1:-1]
                    row=evalString(matches[0].group(2), currentTable.table)
                elif re.search(cellpat2, cell):
                    matches=list(cellpat2.finditer(cmnd))
                    column=matches[0].group(1)
                    row=matches[0].group(2)

                if re.search(cellpat1, formula):
                    while re.search(cellpat1, formula):
                        matches2=list(cellpat1.finditer(formula))
                        column2=evalString(matches2[0].group(1), currentTable.table)[1:-1]
                        row2=evalString(matches2[0].group(2), currentTable.table)
                        formula=re.sub(cellpat1, str(column2+row2) , formula, 1)
                currentTable.setFunc(column,row,formula)

            elif re.search(displaypat, cmnd):
                matches=list(displaypat.finditer(cmnd))
                t=tables[matches[0].group(1)]
                newtable=t.update()
                display(newtable)


        except:
            print("Error")
            quit()




n=int(input())
commands=[None]*n
for i in range(n):
    command=input()
    if re.search(commentpat, command):
        command=re.sub(commentpat, "", command)
    commands[i]=command
readcommand(commands)
