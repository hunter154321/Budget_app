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
