import budget
from budget import create_spend_chart

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
    accounts["food"] = budget.Category("Food")
    accounts["food"].deposit(1000, "initial deposit")
    accounts["food"].withdraw(10.15, "groceries")
    accounts["food"].withdraw(15.89, "restaurant and more food for dessert")
    accounts["clothing"] = budget.Category("Clothing")
    accounts["food"].transfer(50, accounts["clothing"])
    accounts["clothing"].withdraw(25.55)
    accounts["clothing"].withdraw(100)
    accounts["auto"] = budget.Category("Auto")
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
    accounts[u_input] = budget.Category(u_input)
