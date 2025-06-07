print("Good Day! ^_^,Welcome to our restaurant!")
print("*************************************")
print("*              MENU                 *")
print("*************************************")
viand = [
("Mechado",30),
("Adobo",35),
("Sinigang",30),
("Paksiw",25),
("Inihaw",25),
("Ginataan",30),
("Scabitchi",35),
("Prito",25),
("Kalderita",35),
("Soup",35),
("Ginisa",30)
]

index = 0
char = 'A'
number = 1
order = []
quantity = []
total_price = 0
rice_price = 15
total_amount = []
cups = []

for dish,price in viand:
    print(f"{char}. {dish:20} ","*" *20,f" Php {price:.2f}")
    char =  chr(ord(char) + 1)
print("*" * 37)

while True:
    try:
        order_Num = int(input("\nHow many dishes would you like to order?:"))
        if order_Num <= 0:
            print("INVALID. Positive number only :(")
            continue
    except ValueError:
        print("INVALID. Number(s) only :(")
    except NameError:
        print("INVALID. Number(s) only :(")
    else:
        break

number = 1
while True:
    orders = input(f"Enter the letter of your order #{number}:").upper()
    if orders.isdigit():
        print("INVALID. letter only :(")
        continue
    else:
        valid_input = [chr(ord('A') + i) for i in range(len(viand))]
        if orders in valid_input:
            letter_index = ord(orders) - ord('A') + 1
            i = letter_index - 1
            order.append(viand[i])
        elif orders not in valid_input:
            print(f"OPPS! Choose from the MENU :(")
            continue
    while True:
        try:
            q = int(input("How many serve(s):"))
            if q <= 0:
                print("Positive number only :(")
            else:
                quantity.append(q)
                break
        except NameError:
            print("OPPS! NUMBER ONLY :(")
            continue
        except ValueError:
            print("NUMBER ONLY :(")
            continue
    number += 1
    if number == order_Num + 1:
        break

print("\nDuly Noted :)\n")
print("*" * 37)
print("Rice"," " * 19,"*" * 20,f" Php {rice_price:.2f}\n")
while True:
    try:
        rice_cups = int(input("How many cups of rice? \n(Type \"ZERO/0\" if you don't add rice :"))
        if rice_cups > 0:
            cups.append(rice_cups)
            print(f"Noted, we will add {cups[0]} cup(s) of rice to your orders ;)")
            break
        elif rice_cups == 0:
            cups.append(rice_cups)
            print("Noted, we will not include rice to your order ;)")
            break
        else:
            print("Positive number only :(\n")
    except NameError:
        print("Invalid Input :(\n")
    except ValueError:
        print("Number(s) only :(\n")
                                                
print()
print("Thank you and Duly Noted \n");
print("*************************************")
print("*            SUMMARY                *")
print("*************************************")
print("Selected Orders: \n")

i = 0
for viand, price in order:
    total_price  += price * quantity[i]
    print(f"*{viand:20}({quantity[i]})","*" * 20,f" Php {quantity[i] * price:.2f}")
    i += 1
print("*Rice"," " * 14,f"({cups[0]})","*" * 20,f" Php {cups[0] * 15:.2f}")
print(" " * 45,"*" * 11)
print(f"Total payment:"," " * 9,"*" * 20,f" Php {(cups[0] * 15) + total_price:.2f}" )								
print("\nTHANK YOU AND HAPPY EATING :)")