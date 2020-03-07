#!/usr/bin/env python
# coding: utf-8

# In[2]:


import string
import random


# In[3]:


def gen_def():
    lines = []
    keywords = ["define","declare"]
    datatypes = ["","integer","float","string"]
    datatypesIL = ["","int","flt","str"]
    for i in range(0,2):
        for j in range(0,2):
            for v in range(1,6):
                line = keywords[j] + " "
                tab = "\t"
                a = 1
                for vv in range(0,v):
                    line += datatypes[i]+" <unk> "
                    a += 1
                    if i>0:
                        a += 1
                    b = a
#                     if vv != v-1:
#                         line+= ", "
#                         a +=1
                    tab += "def "+datatypesIL[i]+" "+str(b)+" "
                lines.append(line+tab)
    return lines


# In[4]:


ops = {
        "add" : [
            "add",
            "addition of",
            "sum of"
        ],
        "sub" : [
            "subtract",
            "substract",
            "subtraction of",
            "substraction of",
            "difference of"
        ],
        "mul" : [
            "multiply",
            "multiplication of",
            "product of"
        ],
        "div" : [
            "divide",
            "division of"
        ]
    }
and_phrase = "<unk> and <unk>"
def gen_op():
    lines = []
    for k in ops.keys():
        for o in ops[k]:
            line = o+" "+and_phrase
            b = len(o.split())
            tab = "\t"+k+" "+str(b+1)+" "+str(b+3)
            lines.append(line+tab)
    return lines


# In[5]:


def gen_op_equ():
    lines = []
    post = [
        "store in <unk>",
        "store the result in <unk>",
        "store the value in <unk>",
        "then store the value in <unk>",
        "and then store the value in <unk>",
        "and store the value in <unk>"
    ]
    pre = [
        "initialize <unk> with",
        "set <unk> to"
    ]
    for k in ops.keys():
        for o in ops[k]:
            for p in post:
                line = o+" "+and_phrase+" "+p
                b = len(o.split())
                tab = "\t"+k+" "+str(b+1)+" "+str(b+3)+" equ "+str(b+3+len(p.split()))
                lines.append(line+tab)
    for k in ops.keys():
        for o in ops[k]:
            for p in pre:
                line = p+" "+o+" "+and_phrase
                b = len(o.split())+len(p.split())
                tab = "\t"+k+" "+str(b+1)+" "+str(b+3)+" equ "+str(2)
                lines.append(line+tab)
    return lines


# In[6]:


def get_dataset():
    return gen_def()+gen_op()+gen_op_equ()+gen_def()+gen_op()+gen_op_equ()+gen_def()+gen_op()+gen_op_equ()


# In[7]:


with open("test1.dataset","w") as f:
    for l in get_dataset():
        f.write(l)


# In[ ]:




