import re
import math


class Category:
    categories = dict()

    def __init__(self, category):
        self.category = category
        self.ledger = list()
        self.balance = 0.00
        self.withdrawals = 0

    def __str__(self):
        start_str = " " + self.category + " \n"
        string = list()
        lengthOfMax = 31
        newString = ""
        for x in self.ledger:
            string.append(x['description'][:23] + " " +
                          str('{:.2f}'.format(x['amount']))[:7] + "\n")

        asterics = "*"
        length_of_start_str = len(start_str)
        while length_of_start_str < lengthOfMax:
            asterics += "*"
            length_of_start_str += 2
        start_str = re.sub(" ", asterics, start_str)
        if len(start_str) > 31:
            start_str = start_str[1:]

        for x in string:
            regesp = " "
            length_of_str = len(x)
            while length_of_str < lengthOfMax:
                regesp += " "
                length_of_str += 1
            x = re.sub("\s(?=[\d-])", regesp, x)
            newString += x

        return start_str + newString + "Total: " + str(self.balance)

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})
        self.balance = self.balance + amount

    def withdraw(self, amount, description=""):
        if self.check_funds(amount) == True:
            self.ledger.append({"amount": -amount, "description": description})
            self.balance = self.balance - amount
            self.withdrawals += amount
            self.add_withdrawals(amount)

            return True
        if self.check_funds(amount) == False:
            return False

    def get_balance(self):
        return self.balance

    def transfer(self, amount, category):
        if self.check_funds(amount) == True:
            self.withdraw(amount, "Transfer to " + category.category)
            category.deposit(amount, "Transfer from " + self.category)
            return True
        if self.check_funds(amount) == False:
            return False

    def check_funds(self, amount):
        if self.balance >= amount:
            return True
        else:
            return False

    def add_withdrawals(self, amount):
        if self.category in self.categories:
            self.categories[self.category] += amount
        else:
            self.categories[self.category] = amount

def create_spend_chart(categories_list):
    total = 0
    for categ in categories_list:
       total += categ.withdrawals   
    for categ in categories_list:
       categ.withdrawals = math.floor(
            categ.withdrawals * 100 / total / 10) * 10
        #только []  в перебираемом обекте. Точку нельзя, тк х - переменная
    lines = "    --"
    count_categories = 0
    for categ in categories_list:
        count_categories += 1
    while len(lines) < (count_categories - 1) * 3 + 8:
        lines += "-"

    draft_string = "Percentage spent by category\n100| \n 90| \n 80| \n 70| \n 60| \n 50| \n 40| \n 30| \n 20| \n 10| \n  0| \n"

    for categ in categories_list:
        index = draft_string.find(" " + str(categ.withdrawals))
        start_of_draft_str=re.sub("(?<=\d)\|\s\n","|    \n",draft_string[:index])
        start_of_draft_str=re.sub("(?<=\so\s)\s","    ",draft_string[:index])
        start_of_draft_str=draft_string[:index].split('\n')
        
        for st in range(len(start_of_draft_str)):
          if st>0:
           start_of_draft_str[st]+="   "
        start_of_draft_str="\n".join(start_of_draft_str)
        start_of_draft_str=re.sub("\n\s+$","\n",start_of_draft_str)
        string_upd = draft_string[index:].split('\n')
        string_upd.pop()
        for string in range(len(string_upd)):
            if re.search("|\s$", string_upd[string]):
                string_upd[string] += 'o  \n'
            else:
                string_upd[string] += '  o  \n'

        string_upd = ''.join(string_upd)
        if re.search("^ 0",string_upd):
          string_upd=" "+string_upd
        draft_string = start_of_draft_str + string_upd
        
    draft_string = draft_string + lines + "\n"
    end_str = ''
    for categ in categories_list:
        if end_str == '':
            first_x = '     '
            for char in str(categ.category):
                first_x += char + "  \n     "
            end_str += first_x
            end_str = end_str[:-5]
        else:
            end_str = end_str.split('\n')
            end_str.pop()
            for i in range(len(categ.category)):
                if i < len(end_str):
                    end_str[i] += f"{categ.category[i]}  \n"
                else:
                    add_i_to_end_str = ''
                    while len(add_i_to_end_str) < len(end_str[i - 1]) - 4:
                        add_i_to_end_str += " "
                    end_str.append(add_i_to_end_str + categ.category[i] +'  \n')

            for i in range(len(end_str)):
                if i >= len(categ.category):
                    end_str[i] += '   \n'

            for z in range(len(end_str)):
                if re.search('\w$', end_str[z]):
                    end_str[z] += "  \n"

            end_str = ''.join(end_str)

    draft_string = draft_string + end_str
    draft_string = draft_string.split('\n')
    for q in range(len(draft_string)):
      while len(draft_string[q])<14:
       draft_string[q]+=" "
    draft_string.pop()
    draft_string="\n".join(draft_string)
    return draft_string
