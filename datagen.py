import random

basic_binary_ops = [
    {
        "add":[
            "add",
            "additon of",
            "sum of",
        ],
        "sub":[
            "sub",
            "subtract",
            "subtraction of",
            "difference of",
        ],
        "mul":[
            "mul",
            "multiply",
            "multiplication of",
            "product of",
        ],
        "div":[
            "div",
            "divide",
            "division of",
        ],
    },
    [
        "<noise> <keyword> <noise> <var1> and <var2> <noise>",
        "<noise> <keyword> <noise> <var1> to <var2> <noise>",
        "<noise> <keyword> <noise> <var1> by <var2> <noise>",
    ],
    "<op> <var1> <var2>"
]

comparision_ops = [
    {
        "greater": [
            "greater than",
            "bigger than",
            "larger than"
        ],
        "less": [
            "less than",
            "smaller than",
        ],
        "ngreater": [
            "not greater than",
            "not bigger than",
            "not larger than"
        ],
        "nless": [
            "not less than",
            "not smaller than",
        ]
    },
    [
        "<noise> <var1> <keyword> <var2> <noise>",
        "<noise> <var1> is <keyword> <var2> <noise>"
    ],
    "<op> <var1> <var2>"
]

ifconditionals = [
    {
        "greater": [
            "greater than",
            "bigger than",
            "larger than"
        ],
        "less": [
            "less than",
            "smaller than",
        ],
        "ngreater": [
            "not greater than",
            "not bigger than",
            "not larger than"
        ],
        "nless": [
            "not less than",
            "not smaller than",
        ]
    },
    [
        "<noise> if <var1> <keyword> <var2> <noise>",
        "<noise> if <var1> is <keyword> <var2> <noise>",
    ],
    "if <op> <var1> <var2> do"
]

elseifconditionals = [
    {
        "greater": [
            "greater than",
            "bigger than",
            "larger than"
        ],
        "less": [
            "less than",
            "smaller than",
        ],
        "ngreater": [
            "not greater than",
            "not bigger than",
            "not larger than"
        ],
        "nless": [
            "not less than",
            "not smaller than",
        ]
    },
    [
        "<noise> else if <var1> <keyword> <var2> <noise>",
        "<noise> else if <var1> is <keyword> <var2> <noise>",
    ],
    "else if <op> <var1> <var2> do"
]

elseconditionals = [
    {
        "else": [
            "else",
        ]
    },
    [
        "<noise> <keyword> <noise>"
    ],
    "<op>"
]



endifconditionals = [
    {
        "endif": [
            "endif",
            "end if"
        ]
    },
    [
        "<noise> <keyword> <noise>"
    ],
    "<op>"
]

binaryassign = [
    {
        "add":[
            "add",
            "additon of",
            "sum of",
        ],
        "sub":[
            "sub",
            "subtract",
            "subtraction of",
            "difference of",
        ],
        "mul":[
            "mul",
            "multiply",
            "multiplication of",
            "product of",
        ],
        "div":[
            "div",
            "divide",
            "division of",
        ],
    },
    [
        "<noise> set <var1> to <keyword> <var2> and <var3> <noise>",
        "<noise> set <var1> to <keyword> <var2> to <var3> <noise>",
        "<noise> set <var1> to <keyword> <var2> by <var3> <noise>",
        "<noise> let <var1> be <keyword> <var2> and <var3> <noise>",
        "<noise> let <var1> be <keyword> <var2> to <var3> <noise>",
        "<noise> let <var1> be <keyword> <var2> by <var3> <noise>",
    ],
    "<op> <var2> <var3> equ <var1>"
]

assignnum = [
    {
        "<exp>1":[
            "one"
        ],
        "<exp>2":[
            "two"
        ],
        "<exp>3":[
            "three"
        ],
        "<exp>4":[
            "four"
        ],
        "<exp>5":[
            "five"
        ],
        "<exp>6":[
            "six"
        ],
        "<exp>7":[
            "seven"
        ],
        "<exp>8":[
            "eight"
        ],
        "<exp>9":[
            "nine"
        ],
    },
    [
        "<noise> set <noise> <var1> to <keyword> <noise>",
        "<noise> let <noise> <var1> be <keyword> <noise>",
        "<noise> assign <noise> <var1> with value <keyword> <noise>",
        "<noise> assign <noise> <var1> with integer <keyword> <noise>",
        "<noise> assign <noise> <var1> with number <keyword> <noise>",
        "<noise> initialize <noise> <var1> to <keyword> <noise>",
        "<noise> initialize <noise> <var1> with <keyword> <noise>",
        "<noise> initialize <noise> <var1> with value <keyword> <noise>",
        "<noise> assign <noise> <var1> with integer <keyword> <noise>",
        "<noise> assign <noise> <var1> with number <keyword> <noise>",
    ],
    "assign <var1> <op>"
]

def permute(lines):
    keywords = lines[0]
    patterns = lines[1]
    tabline = lines[2]

    output = []
    for kv in keywords.items():
        op = kv[0]
        keys = kv[1]

        for c in range(0,5):
            for b in range(0,5):
                for a in range(0,5):
                    for key in keys:
                        for p in patterns:
                            line = ""
                            noise_ctr = 0
                            for pw in p.split():
                                if pw == "<noise>":
                                    noise_ctr+=1
                                    if not a==0 and noise_ctr==1:
                                        for _ in range(0,a):
                                            line += "<unk> "
                                    elif not b==0 and noise_ctr==2:
                                        for _ in range(0,b):
                                            line += "<unk> "
                                    elif not c==0 and noise_ctr==3:
                                        for _ in range(0,c):
                                            line += "<unk> "
                                elif pw == "<keyword>":
                                    line += key + " "
                                else:
                                    line += pw + " "
                            line += "\t"
                            for tw in tabline.split():
                                if tw == "<op>":
                                    line += op + " "
                                else:
                                    line += tw + " "
                            output.append(line)
    return output

def calc_idx(output):
    res = []
    for o in output:
        s = o.split('\t')[0]
        t = o.split('\t')[1]
        idx = {}
        sline = ""
        for i,w in enumerate(s.split()):
            if w[1:4] == "var":
                idx[w] = i
                sline += "<unk> "
            else:
                sline += w+" "
        tline = ""
        for w in t.split():
            if w in idx:
                tline += str(idx[w]+1)+" "
            else:
                tline += w+ " "
        line = sline+"\t"+tline
        res.append(line)
    return sorted(list(set(res)))

# for p in calc_idx(add_noise(permute(basic_binary_ops))):
#     print(p)

# for p in calc_idx(permute_with_pat_and_noise(comparision_ops)):
#     print(p)

def get_dataset():
    lines = []
    lines = lines + calc_idx(permute(basic_binary_ops))
    lines = lines + calc_idx(permute(comparision_ops))
    lines = lines + calc_idx(permute(ifconditionals))
    lines = lines + calc_idx(permute(endifconditionals))
    lines = lines + calc_idx(permute(binaryassign))
    lines = lines + calc_idx(permute(assignnum))
    lines = lines + calc_idx(permute(elseconditionals))
    lines = lines + calc_idx(permute(elseifconditionals))
    return lines


if __name__ == "__main__":
    # lines = get_dataset()
    # for p in lines:
    #     print(p)
    for b in calc_idx(permute(elseconditionals)):
        print(b)