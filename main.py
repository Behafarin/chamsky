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

    def update_dict(self):
        for key, rules in self.grammer_dict:
            rules.extand(self.add_list[key])
            rules = list(set(rules))
        return self.grammer_dict

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
        return res

    def remove_landa(self):
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
        singular = []
        for key, rules in self.grammer_dict:
            for rule in rules:
                if rule.isupper() and len(rule) == 1:
                    singular.append(rule)
                    rules.remove(rule)
        for key, rules in self.grammer_dict:
            for rule in rules:
                for rep in singular:
                    for law in self.grammer_dict[rep]:
                        changed_rules = self.replace_sth(rule, rep, law)
                        self.add_list[key].extend(changed_rules)

    def replace_lower(self):
        changed_rules = []
        flag = False
        for key, rules in self.grammer_dict:
            for rule in rules:
                for i in range(0, len(rule)):
                    if rule[i].islower and rule[i-1] != 'T':
                        flag = True
                        temp = rule[0:i]+'T'+rule[i]+rule[i+1:len(rule)]
                if flag:
                    rules.remove(rule)
                    changed_rules.append(temp)
            self.add_list[key].extend(changed_rules)

    def chamsky(self):
        self.remove_landa()
        self.grammer_dict = self.update_dict()
        self.remove_singular()
        self.grammer_dict = self.update_dict()
        self.replace_lower()
        self.grammer_dict = self.update_dict()


filename = input()
file = open(filename, "r")
grammer_list = []
for line in file:
    grammer_list.append(file.readline())

hey = Chamsky(grammer_list)
hey.chamsky()