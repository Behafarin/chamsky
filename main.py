import re
txt = input()
T = {}
# finding lowercase
x = re.findall('[a-z]',txt)
x = list(dict.fromkeys(x))
y = re.split("->",txt,1)
z = re.split("\|",y[1])
flag = False
for i in z :
    if i=='#':
        z.remove(i)
        flag = True
if flag:
    for i in z :
        for j in i:
            if j == y[0]:
                index = i.index(j)
                z.append(i[0:index]+i[index+1:len(i)])

z = list(dict.fromkeys(z))
print(x)
for i in x:
    T["T"+i] = i
for i,j in T.items():
    print(i+'->'+j)
for i in z:
    print(i)