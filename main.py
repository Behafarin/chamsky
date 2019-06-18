import re


class Chamsky:

    def __init__(self, txt):
        self.txt = txt

    def make_T(self):
        T = {}
        terminals = re.findall('[a-z]', txt)
        terminals = list(set(terminals))
        for i in terminals:
            T["T" + i] = i
        return T

    def print_grammer(self, left_part, right_part):
        for i in right_part:
            if i != '' and i != left_part:
                print(left_part+'->'+i)
        T = self.make_T()
        for i, j in T.items():
            print(i+'->'+j)

    def chamsky(self):
        grammer = re.split('->', self.txt, 1)
        left_part = grammer[0]
        right_part = grammer[1].split('|')
        flag = False
        temp = None
        add_list = []
        for i in right_part:
            if i == '#':
                right_part.remove(i)
                flag = True
        if flag:
            for i in right_part:
                i = i.replace(left_part, '')
                add_list.append(i)

        for i in right_part:
            if i.isupper() and len(i) == 1:
                temp = i
                right_part.remove(i)

        if temp is not None:
            for i in right_part:
                i = i.replace(left_part, temp)
                add_list.append(i)
#        for i in right_part:
#            for j in range(0, len(i)):
#                if i[j].islower():
#                    i = i.replace(i[j], "T"+i[j])
#                    add_list.append(i)
        right_part.extend(add_list)
        right_part = list(set(right_part))
        self.print_grammer(left_part, right_part)


txt = input()
hey = Chamsky(txt)
hey.chamsky()
