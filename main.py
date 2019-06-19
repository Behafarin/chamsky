import re


class Chamsky:

    def __init__(self, grammer_list):
        self.grammer_list = grammer_list
        self.grammer_dict = {}
        self.add_list = {}
        self.v_counter = 0
        for line in grammer_list:
            grammer = line.split('->')
            left_part = grammer[0]
            right_part = list(map(lambda x: x.strip(), re.split(r'\|', grammer[1])))
            self.add_list[left_part] = []
            r = self.grammer_dict.get(left_part, list())
            r.extend(right_part)
            self.grammer_dict[left_part] = r

    def rule_len(self,rule):
        return len(re.findall(r'[A-Z]', rule))

    def update_dict(self):
        for key, rules in self.grammer_dict.items():
            rules.extend(self.add_list[key])
            self.grammer_dict[key] = list(set(rules))
            self.add_list[key].clear()

    def make_T(self):
        T = {}
        terminals = []
        for line in self.grammer_list:
            terminals.extend(re.findall('[a-z]', line))
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

    def replace_sth(self, rule, rep, repwith, st=0):
        rule = rule[st:]
        res = []
        try:
            i = rule.index(rep)
            temp = rule[0:i]+repwith+rule[i+1:len(rule)]
            res.append(temp)
            rule_t = list(map(lambda x: f"{rule[:i+1]}{x}", self.replace_sth(rule, rep, repwith, st=i + 1)))
            res.extend(rule_t)
            temp_t = list(map(lambda x: f"{temp[:i+1]}{x}", self.replace_sth(temp, rep, repwith, st=i + 1)))
            res.extend(temp_t)
        except:
            return []
        return res

    def remove_landa(self):
        have_landa = []
        for key, rules in self.grammer_dict.items():
            if '#' in rules:
                rules.remove('#')
                have_landa.append(key)
        for key, rules in self.grammer_dict.items():
            for rule in rules:
                for landa in have_landa:
                    changed_rules = self.replace_sth(rule, landa, '')
                    self.add_list[key].extend(changed_rules)

    def remove_singular(self):
        singular = []
        # have_singular = {}
        for key, rules in self.grammer_dict.items():
            for rule in rules:
                if rule.isupper() and len(rule) == 1:
                    singular.append((key, rule))

        for key, rules in self.grammer_dict.items():
            for rule in rules:
                for sig_key, sig_rule in singular:
                    if sig_key in rule:
                        changed_rules = self.replace_sth(rule, sig_key, sig_rule)
                        self.add_list[key].extend(changed_rules)

        for sig_key, sig_rule in singular:
            self.grammer_dict[sig_key].remove(sig_rule)

    def replace_lower(self):
        for key, rules in self.grammer_dict.items():
            changed_rules = []
            for rule in rules:
                j = 0
                flag = False
                temp = rule
                if len(rule) == 1 and rule.islower():
                    continue
                for i in range(len(rule)):
                    if rule[i].islower() and rule[i-1] != 'T':
                        flag = True
                        temp = temp[:j]+'T'+temp[j]+temp[j+1:]
                        j += 1
                    j += 1
                if flag:
                    changed_rules.append((rule, temp))
            for rule, ch_rule in changed_rules:
                self.grammer_dict[key].remove(rule)
                self.add_list[key].append(ch_rule)

    def make_v(self, rule, key=None, first_time=False):
        new_rule = []
        add_rule = {}
        new_rule.append(rule[1:])
        if self.rule_len(rule) > 2:
            self.v_counter += 1
            v = f'V{self.v_counter}'
            ind = 1 if rule[0] != 'T' else 2
            add_rule.update(self.make_v(rule[ind:], key=v))
            if first_time:
                self.grammer_dict[key].remove(rule)
                self.grammer_dict[key].append(f'{rule[:ind]}{v}')
            else:
                add_rule[key] = [f'{rule[:ind]}{v}']
        else:
            if first_time:
                return {}
            add_rule[key] = [rule]
        return add_rule

    def chamskyfy(self):
        add_rule = {}
        for key, rules in self.grammer_dict.items():
            t_rules = [x for x in rules]
            for rule in t_rules:
                add_rule.update(self.make_v(rule, key, True))
        self.grammer_dict.update(add_rule)

    def chamsky(self):
        self.remove_landa()
        self.update_dict()
        self.remove_singular()
        self.update_dict()
        self.replace_lower()
        self.update_dict()
        self.chamskyfy()
        self.print_grammer()


filename = input()
file = open(filename, "r")
grammer_list = []
for line in file:
    grammer_list.append(line.strip())

hey = Chamsky(grammer_list)
hey.chamsky()