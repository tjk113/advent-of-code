import re

def mul(a, b):
    return a * b

with open('input.txt', 'r') as file:
    text = file.read()
    sum = sum([eval(i) for i in re.findall(r'mul\(\d+,\d+\)', text)])
    print(f'Part 1: {sum}')
    sum = 0
    do = True
    for i in range(len(text)):
        if re.match(r'do\(\)', text[i:]) != None:
            do = True
        if re.match(r"don't\(\)", text[i:]) != None:
            do = False
        res = re.match(r'mul\(\d+,\d+\)', text[i:])
        if res != None and do:
            sum += eval(res.group(0))
    print(f'Part 2: {sum}')
