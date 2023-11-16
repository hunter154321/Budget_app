class Category:
  def __init__ (self, group):
    self.ledger = []
    self.entries = []
    self.group = group
  
  def __repr__ (self):
    #makes title
    title = '*' * 30
    slice1, slice2 = int(15-(len(self.group)/2)), int(15+(len(self.group)/2))
    title = title[:slice1] + self.group + title[slice2:] + '\n'
    
    #adds ledger to title
    for entry in self.ledger:
      if len((entry['description'])) <= 23:
        num_spaces = (int(len(entry['description'])) + int(len("{0:7.2f}".format(entry['amount'])))) 
        spaces = (30 - num_spaces) * ' '
        title = title + entry['description'] + spaces + "{0:7.2f}".format(entry['amount']) + '\n'
      else:
        num_spaces = (23) + int(len("{0:7.2f}".format(entry['amount']))) 
        spaces = (29 - num_spaces) * ' '
        modilfied_entry = entry['description']
        title = title + modilfied_entry[:23] + spaces + "{0:7.2f}".format(entry['amount']) + '\n'
      
    #generate and add total to title

    title = title + 'Total:' + str("{0:7.2f}".format(self.get_balance()))
      
    return(title + "\n\n")
  def deposit(self, amount, description = ""):
    entry = {"amount":amount, 'description':description}
    self.ledger.append(entry)
    return()

  def withdraw(self, amount, description = ""):
    if self.get_balance() >= amount:
      entry = {"amount":-amount, 'description':description}
      self.ledger.append(entry)
      return(True)
    else:
      return(False)

  def get_balance(self):
    balance = 0.00
    for item in self.ledger:
      balance = balance + item['amount']
    return(round(balance, 2))

  def transfer(self, amount, other_cat):
    if self.get_balance() >= amount:
      self.withdraw(amount, "Transfer to " + str(other_cat.group))
      other_cat.deposit(amount, "Transfer from " + self.group)
      return(True)
    else:
      return(False)

  def check_funds(self, amount):
    if self.get_balance() >= amount:
      return(True)
    else:
      return(False)


def create_spend_chart(categories): 
  all_withdraws = {}
  x = 0
  groups = []
  for cat in categories:
    groups.append(cat.group)
    all_withdraws[x] = 0
    withdraws = 0
    for entry in cat.ledger:
      if entry['amount'] < 0:
        withdraws = withdraws + entry['amount']
    all_withdraws[x] = "{0:6.2f}".format(withdraws)
    x = x + 1
    total = 0
    for key in all_withdraws:
      total = total + float(all_withdraws[key])
    percentage = {}
    for key in all_withdraws:
      percentage[key] = rounding((float(all_withdraws[key]) / total) * 100, 10)
  
  chart = "Percentage spent by category\n"
  num = 100
  lines = '    -'
  while num >= 0:
    if num == 100:
      chart = chart + str(num) + '| '
    elif num < 100 and num > 0:
      chart = chart + ' ' + str(num) + '| '
    else:
      chart = chart + '  ' + str(num) + '| '
    runs = 0
    for key in percentage:
      if percentage[key] >= num:
        chart = chart + 'o  '
      else:
        chart = chart + '   '
      if runs == len(groups)-1:
        chart = chart + '\n'
      runs = runs + 1
    num = num - 10


    
  for word in groups:
    lines = lines + '---'
  chart = chart + lines + '\n'
  letters = ''
  runs = 0
  for word in groups:
    while len(word) < len(max(groups, key=len)):
      word = word + ' '
    groups[runs] = word
    runs = runs + 1
  runs = 0
  x = 0
  for i in range(len(max(groups, key=len))):
    for j in range(len(groups)):
      letters = letters + groups[j][i] + '  '
    if x <= 11:
      chart = chart + '     ' + (letters) + '\n'
    else:
      chart = chart + '     ' + (letters)
    letters = ""
    x = x + 1
  
  return(chart)

def rounding(num, divisor):
    return num - (num%divisor)
# import budget
# from budget import create_spend_chart
# from unittest import main

def test_data():
  food = Category("Food")
  food.deposit(1000, "initial deposit")
  food.withdraw(10.15, "groceries")
  food.withdraw(15.89, "restaurant and more food for dessert")
  clothing = Category("Clothing")
  food.transfer(50, clothing)
  clothing.withdraw(25.55)
  clothing.withdraw(100)
  auto = Category("Auto")
  auto.deposit(1000, "initial deposit")
  auto.withdraw(15)

accounts = {}
print("Welcome to Hunter's Budget Program!")
print("From here you can see your spending chart or navigate to a spending category (Enter x to load test data)")
run = True
while run == True:
  if (bool(accounts)):
    print("Current Categories:",  ", ".join(accounts))
  else:
    print("No existing accounts")
  u_input = input("Enter existing or new Category name, 'Spending Chart', or exit to end program: ")
  u_input = u_input.lower()
  if (u_input == "spending chart"):
    print(create_spend_chart(accounts.values()))
  elif (bool(u_input) == False):
    print("No input entered\n\n")
  elif (u_input == "x"):
    accounts["food"] = Category("Food")
    accounts["food"].deposit(1000, "initial deposit")
    accounts["food"].withdraw(10.15, "groceries")
    accounts["food"].withdraw(15.89, "restaurant and more food for dessert")
    accounts["clothing"] = Category("Clothing")
    accounts["food"].transfer(50, accounts["clothing"])
    accounts["clothing"].withdraw(25.55)
    accounts["clothing"].withdraw(100)
    accounts["auto"] = Category("Auto")
    accounts["auto"].deposit(1000, "initial deposit")
    accounts["auto"].withdraw(15)
  elif (u_input in accounts.keys()):
    print("What would you like to do in", u_input +"?")
    action = input("Enter 'view', 'withdraw', 'deposit', 'transfer', or 'back': ")
    action = action.lower()
    if (action == 'view'):
      print(accounts[u_input])
    elif (action == 'withdraw'):
      amount = float(input("How much to Withdraw?: "))
      note = input("What is the note for the withdrawal?: ")
      accounts[u_input].withdraw(amount, note)
    elif (action == 'deposit'):
      amount = float(input("How much to Deposit?: "))
      note = input("What is the note for the deposit?: ")
      accounts[u_input].deposit(amount, note)
    elif (action == 'transfer'):
      print(", ".join(accounts))
      transfer = input("Which account should we transfer money to?: ")
      amount = float(input("How much to transfer?: "))
      accounts[u_input].transfer(amount, accounts[transfer])
    else:
      print("Going back...\n\n")
  elif (u_input == "exit"):
    run = False
  else:
    accounts[u_input] = Category(u_input)
