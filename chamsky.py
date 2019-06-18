import re


class Chamsky:

    def __init__(self, grammer_list):
        self.grammer_list = grammer_list
        self.grammer_dict = {}
        self.add_list = {}
        for line in grammer_list:
            grammer = re.split('->', line, 1)
            left_part = grammer[0]
            right_part = grammer[1].split('|')
            self.add_list[left_part] = []
            r = self.grammer_dict.get(left_part, list())
            r.extend(right_part)
            self.grammer_dict[left_part] = r

    def make_T(self):
        T = {}
        for line in grammer_list:
            terminals = re.findall('[a-z]', line)
        terminals = list(set(terminals))
        for i in terminals:
            T["T" + i] = i
        return T

    def print_grammer(self):
        for key, values in self.grammer_dict.items():
            print(f'{key}->' + ' | '.join(values))
        T = self.make_T()
        for key, value in T.items():
            print(key+'->'+value)

    def replace_sth(self,rule, rep, repwith):
        res = []
        for i in range(0, len(rule)):
            if rule[i] == rep:
                res.append(rule[0:i]+repwith+rule[i+1:len(rule)])
        return  res
    def remove_landa(self):
        flag = False
        temp = None
        have_landa = []
        for key, rules in self.grammer_dict:
            if '#' in rules:
                rules.remove('#')
                have_landa.append(key)
        for key, rules in self.grammer_dict:
            for rule in rules:
                for landa in have_landa:
                    changed_rules = self.replace_sth(rule, landa, '')
                    self.add_list[key].extend(changed_rules)

    def remove_singular(self):
        for i in self.right_part:
            if i.isupper() and len(i) == 1:
                temp = i
                self.right_part.remove(i)

        if temp is not None:
            for i in self.right_part:
                i = i.replace(self.left_part, temp)
                self.add_list.append(i)

    def chamsky(self):
        self.remove_landa()
        self.remove_singular()

        for i in self.right_part:
           for j in range(0, len(i)):
               if i[j].islower():
                   i = i.replace(i[j], "T"+i[j])
                   self.add_list.append(i)
        self.right_part.extend(self.add_list)
        right_part = list(set(self.right_part))
        self.print_grammer(self.left_part, right_part)


filename = input()
file = open(filename, "r")
grammer_list = []
for line in file:
    grammer_list.append(file.readline())

hey = Chamsky(grammer_list)
hey.chamsky()


