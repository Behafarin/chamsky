import re
txt = input()
T = {}
# finding lowercase
x = re.findall('[a-z]', txt)
x = list(dict.fromkeys(x))
y = re.split("->", txt, 1)
z = re.split("\|", y[1])
flag = False
temp = None
for i in z:
    if i == '#':
        z.remove(i)
        flag = True
if flag:
    for i in z:
        for j in i:
            if j == y[0]:
                index = i.index(j)
                z.append(i[0:index]+i[index+1:len(i)])
for i in z:
    if i.isupper() and len(i) == 1:
        temp = i
        z.remove(i)
if temp is not None:
    for i in z:
        for j in range(0, len(i)):
            if i[j] == y[0]:
                z.append(i[0:j]+temp+i[j+1:len(i)])
z = list(dict.fromkeys(z))
for i in x:
    T["T"+i] = i
for i in z:
    if i != '' and i != y[0]:
        print(y[0]+'->'+i)
for i, j in T.items():
    print(i+'->'+j)