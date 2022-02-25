class Category:
    def __init__(self, type):
        self.type = type
        self.ledger = []

    def deposit(self, amount, description=""):
        try:
            self.ledger.append({
                "amount": amount,
                "description": description
            })
            return True
        except:
            return False

    def withdraw(self, amount, description=""):
        if amount < 0:
            if self.check_funds(amount):
                self.ledger.append({
                "amount": amount,
                "description": description
            })
                return True
        return False

    def transfer(self, amount, another_category):
        withdraw_op = self.withdraw(-amount, f"Transfer to {another_category.type.title()}")
        deposit_op = another_category.deposit(amount, f"Transfer from {self.type}")
        return withdraw_op and deposit_op

    def get_balance(self):
        return sum([i["amount"] for i in self.ledger])

    def check_funds(self, amount):
        return self.get_balance() >= abs(amount)

    def get_statement(self):
        initial_deposit = sum([i["amount"] for i in list(filter(lambda x: x["amount"] > 0 and "Transfer" not in x["description"], self.ledger))])
        statement = f'''*************{self.type.title()}*************\n'''
        statement += f'''initial deposit {'%6s' % float(initial_deposit)}\n'''
        for i in list(filter(lambda x: x["amount"] <= 0, self.ledger)):
            statement += f'''{i["description"]} {'%6s' % float(i["amount"])}\n'''
        for i in list(filter(lambda x: "Transfer from" in x["description"], self.ledger)):
            statement += f'''{i["description"]} {'%6s' % float(i["amount"])}\n'''
        statement += f'''Total: {self.get_balance()}'''
        return statement

food = Category("food")
clothes = Category("clothes")
food.deposit(1000, "salary")
food.withdraw(-120, "Speeding Ticket")
# food.transfer(120, clothes)
clothes.withdraw(-90, "balmain")
auto = Category("auto")
auto.deposit(500)
auto.withdraw(-200, "repair")

def create_spend_chart(*args):
    result = {

    }

    for i in args:
        calc = (int((i.get_balance() / (sum([i["amount"] for i in list(filter(lambda x: x["amount"] > 0, i.ledger))]) if sum([i["amount"] for i in list(filter(lambda x: x["amount"] > 0, i.ledger))]) != 0 else 1) * 10) % 10))
        result[i.type] = 100 - (calc * 10) if (calc * 10) != 0 else 0

    for (key, value) in result.items():
        result[key] = [i * 10 for i in range(value // 10 + 1)]
    for i in range(0, 11):
        turn = 100 - (i * 10)
        ok = len([n for n in result.values() if turn in n])
        print('%6s' % f"  {turn}|" + "o    " * ok)
    print('      ' + ("-" * round(len(args) * 3)))
    names = []
    final_name = ""
    def sort_names(name):
        return result[name.lower()][-1]
    name_list = [i.type.title() for i in args]
    name_list.sort(key=sort_names)
    for i in name_list:
        names.append([n for n in i])
    for i in range(max([len(i) for i in names])):
        for n in range(len(names)):
            try:
                final_name += '%6s' % f"{names[n][i]}"
            except:
                final_name +=  '%6s' % f"  "
        final_name += '%6s' % "\n"

    print('%6s' % f'{final_name}')

create_spend_chart(food, auto, clothes)



