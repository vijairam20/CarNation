import os
import sys
import csv
import time
import pickle
import getpass
import webbrowser
import smtplib
import random
from decimal import Decimal
#Files
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
CARS = os.path.join(THIS_FOLDER, 'mtcars.csv')
USERS = os.path.join(THIS_FOLDER,'user.csv')
#Internet Connection
InternetConnection = False
class User:
    def __init__(self,name , username ,password , email):
        self.name = name
        self.username = username
        self.password = password
        self.email = email
    def __repr__(self) :
        return self.name
    def printDetails(self):
        print("Name     : "+self.name)
        print("Usename  : "+self.username)
        print("Password : "+self.password)
        print("Email    : "+self.email)
class Car:
    def __init__(self,manuf , model, type , price , mpg , cyl , hp , ft , pas , length , width , weight ,stock ):
        self.manuf = manuf
        self.model = model
        self.type = type
        self.price = price
        self.mpg = mpg
        self.hp = hp
        self.cyl = cyl
        self.ft = ft
        self.pas = pas
        self.length = length
        self.width = width
        self.weight = weight
        self.stock = stock
        self.interst = 0
    def __repr__(self) :
        str = self.manuf + " " + self.model
        return str
    def printDetails(self):
         print("Manufacturer : "+self.manuf)
         print("Model        : "+self.model)
         print("Type         : "+self.type)
         print("Price        : $"+str(self.price*1000))
         print("Milelage     : "+str(self.mpg))
         print("Horse Power  : "+str(self.hp))
         print("Cylinders    : "+str(self.cyl))
         print("Fuel Tank    : "+str(self.ft))
         print("Length       : "+str(self.length))
         print("Width        : "+str(self.width))
         print("Weigth       : "+str(self.weight))

         if self.stock > 0 :
          print("Stock        : "+str(self.stock))
         else :
          print("Stock : Not Available\n")
    def getStock(self) :
        count = 0
        orders = []
        file = open("orders.pickle",'rb')
        try :
            while True :
                orders.append(pickle_load(file))
        except :
            file.close()
        for order in orders :
            if str(order.car) == str(self) :
                 count += 1
        if count >= self.stock :
            return 0
        return self.stock - count
class Cart :
    def __init__(self,car,user):
        self.car = car
        self.user = user
        try :
            file = open("cart.pickle",'ab')
        except IOError :
            print("UNABLE to open file")
        else :
            pickle.dump(self,file)
            file.close()
    def __repr__(self):
        return str(self.user)+":"+str(self.car)
class Order :
    def __init__(self,short) :
        self.car = short.car
        self.user = short.user
        self.buyTime = time.asctime(time.localtime(time.time()))
        try :
            file = open("orders.pickle",'ab')
        except IOError :
            print("UNABLE to open file")
        else :
            pickle.dump(self,file)
            file.close()

def printHeader() :
    print("\n\n\t\t\t\t\t<<<CarNation>>>")
    print("\t\t\t\t\t\t\t\t\t\t\t  -Lulu for cars")
def init():
    os.system("cls")
    printHeader()
    print("\n\n\t1.Login")
    print("\n\t2.Create New User")
    print("\n\t3.Exit")
    print("\n\n\tEnter your options:\t")
    flag = int(input())
    while flag < 1 or flag > 3 :
        print("Please enter again :")
        flag = int(input())
    if(flag == 1):
        os.system("cls")
        printHeader()
        user = None
        user = authenticate()
        if user == None :
            init()
        os.system("cls")
        nation(user)
    elif(flag == 2):
        os.system("cls")
        obj = create_user()
        print("User Created")
        init()
    elif(flag == 3):
        print("Quitting")
        time.sleep(3)
        os.system('cls')
        sys.exit()
def aldreadyExist(types , pos) :
     for i in range(pos) :
        if types[i] == types[pos] :
            return True
     return False
def removeDuplicates(types) :
    Ntypes =[]
    Ntypes.append(types[0])
    i = 1
    while i < len(types) :
        if not (aldreadyExist(types , i)) :
           Ntypes.append(types[i])
        i += 1
    return Ntypes
def getDetails(n , spec ="" , a = 0):
    types = []
    file = open(CARS, "r", newline='')
    if spec == "" :
        with file :
            reader = csv.reader(file)
            for row in reader :
                types.append(row[n])
    else :
        with file :
            reader = csv.reader(file)
            for row in reader :
                if spec == row[a] :
                   types.append(row[n])
    types = removeDuplicates(types)
    return types
#authenticate Returnning User
def authenticate():
    os.system('cls')
    print("Enter Username :")
    username = input()
    password = getpass.getpass(prompt="Enter Password : ")
    file = open(USERS,'r',newline='')
    flag = False
    with file:
        reader = csv.reader(file)
        for row in reader:
            user = row[1]
            passw = row[2]
            if user == username and password == passw :
                print("Login Successful")
                u = User(row[0],row[1],row[2],row[3])
                flag = True
                break
        if not flag :
            print("Right. Off you go. peasant")
            return None
    return u
#Create Users
def create_user():
    print("Enter Name :")
    name = input()
    print("Enter Username : ")
    username = input()
    i = 0
    while True :
        if i > 0 :
            print ("Password does not match , Please try again")
        print("Enter Password : ")
        password1 = input()
        print("Confirm Password :")
        password2 = input()
        if password1 == password2 :
            break;
        i+=1
    password = password1
    print("Enter Email :")
    email = input()
    if InternetConnection :
        verifyMail(name,email)
    obj = User(name, username, password,email)
    file = open(USERS,'a',newline='')
    data =[[name,username,password,email]]
    with file:
        writer = csv.writer(file)
        writer.writerows(data)
    print("Welcome to CarNation ,  "+name)
    print("Press any key to econtinue")
    input()
    return obj
#Purchase
def nation(user):
    os.system("cls")
    printHeader()
    print("Welcome back "+ str(user))
    print("1.Browse")
    print("2.Dashboard")
    print("3.Back")
    flag =(int)(input())
    while flag < 1 or flag > 3 :
        print("Please Enter Again")
        flag = (int)(input())
    if flag == 1 :
        os.system("cls")
        car = buy(user)
        print("Press anykey to continue")
        input()
        nation(user)
    elif flag == 2  :
        dashboard(user)
    elif flag == 3 :
        os.system("cls")
        init()
#Geting cars -Pickle
def readCars():
    file = open("cars.pickle",'rb')
    cars = []
    try :
        while True :
            cars.append(pickle.load(file))
    except EOFError :
        file.close()
    return cars

def getManufacturers():
    brands = getDetails(0)
    i = 0
    inp = 0
    c = 1
    while inp == 0 :
        while i < 5 :
            print(str(c) +":" +brands[c-1])
            c += 1
            i += 1
        i = 0
        print("Press NUM for Brand ")
        print("Press 0 for more")
        inp = int(input())
    return brands[inp-1]
def getType(man ="") :
    if not (man == "") :
        types = getDetails(2,man)
    else :
        types = getDetails(2)
    i = 1
    for t in types:
        print(str(i) + ":" + t)
        i+=1
    print("Press number for type")
    inp = int(input())
    return types[inp-1]
def getCar(man = "", type ="") :
    file = open(CARS, 'r', newline='')
    cars =[]
    flag_1 = True
    flag_2 = True
    if man == "" :
        flag_1 = False
    if type == "":
        flag_2 =False
    with file :
        reader = csv.reader(file)
        for row in reader :
            if flag_1 and flag_2 :
                if row[0] == man and row[2] == type :
                    cars.append(Car(row[0],row[1],row[2],Decimal(row[3])+Decimal(row[4]),int(row[5]),int(row[6]),Decimal(row[7]),Decimal(row[8]),Decimal(row[9]),Decimal(row[10]),Decimal(row[12]),Decimal(row[13]),int(row[14])))
            elif flag_1 :
                if row[0] == man :
                    cars.append(Car(row[0],row[1],row[2],Decimal(row[3])+Decimal(row[4]),int(row[5]),int(row[6]),Decimal(row[7]),Decimal(row[8]),Decimal(row[9]),Decimal(row[10]),Decimal(row[12]),Decimal(row[13]),int(row[14])))
            elif flag_2 :
                if row[2] == type :
                    cars.append(Car(row[0],row[1],row[2],Decimal(row[3])+Decimal(row[4]),int(row[5]),int(row[6]),Decimal(row[7]),Decimal(row[8]),Decimal(row[9]),Decimal(row[10]),Decimal(row[12]),Decimal(row[13]),int(row[14])))
    return cars
def buy(user):
    printHeader()
    print("Enter Option")
    print("1.Search parameters :")
    print("2.Sort By parameters :")
    print("3.Check Trending")
    print("4.Back")
    flag = int(input())
    while flag < 1 or flag > 4 :
        flag = int(input())
    if flag == 1 :
        os.system("cls")
        printHeader()
        print("1.Manufacturer")
        print("2.Type")
        print("3.Both")
        manuf = ""
        Type = ""
        flag = int(input())
        if flag == 1:
            manuf = getManufacturers()
        elif flag == 2:
            Type = getType()
        elif flag ==3 :
            manuf = getManufacturers()
            Type  = getType(manuf)
        cars = getCar(manuf,Type)
        Bcar = getBuyCar(cars)
        flag = 0
    elif flag == 2 :
        os.system("cls")
        printHeader()
        print("Sort By")
        print("1.Price")
        print("2.Mileage")
        print("3.Horse Power")
        print("4.Fueltank")
        flag = int(input())
        params = ["price","mileage","horse power" ,"fueltank"]
        symbols =["$","L/100km","HP","L"]
        if flag :
            printHeader()
            os.system("cls")
            print("By "+params[flag-1])
            cars = readCars()
            cars = sortBy(cars,flag) #Remember to add sort for all parameters
            print("Select:")
            print("1.Ascending")
            print("2.Descending")
            fl = (int)(input())
            if fl == 2 :
                cars.reverse()
            i = 1
            print (cars)
            for car in cars :
                if flag == 1 :
                    print(str(i)+":"+str(car)+" $"+str(car.price))
                elif flag == 2 :
                    print(str(i)+":"+str(car)+" "+str(car.mpg)+"L/100km")
                elif flag == 3 :
                    print(str(i)+":"+str(car)+" "+str(car.hp)+"HP")
                elif flag == 4 :
                    print(str(i)+":"+str(car)+" "+str(car.ft)+"L")
                i+=1
            flag = int(input("Enter NUM for Car"))
            Bcar = cars[flag-1]
            flag = 0
    elif flag == 3 :
        os.system("cls")
        printHeader()
        i = 1
        print("Trending Cars")
        cars = checkTrending()
        for car in cars :
            if findInterest(car) == 0 :
                break
            print(str(i)+" : "+str(car))
            i+=1
        print("Please Enter which car : ")
        print("Press 0 to go back")
        flag = int(input())
        if flag == 0 :
            buy(user)
        Bcar = cars[flag-1]
    elif flag == 4 :
        return None
    print("Do you want more deatils of the car :")
    print("yes or no")
    while True :
        ans = input()
        if  ans.lower() == "yes" :
            viewCar(Bcar)
            break
        elif ans.lower() == "no" :
            break
    print("Do you want add it to  the shortlist :")
    print("yes or no")
    while True :
        ans = input()
        if  ans.lower() == "yes" :
            cart = Cart(Bcar,user)
            print(str(Bcar)+" has been added to the cart")
            break
        elif ans.lower() == "no" :
            print(str(Bcar)+" has not been added to the shortlist")
            Bcar = None
            break
    return Bcar
def getBuyCar(cars) :
    i = 0
    inp = 0
    c = 1
    while inp == 0:
        while i < 5 and c-1 < len(cars):
            print(str(c) + ":" + str(cars[c - 1]))
            c += 1
            i += 1
        i = 0
        print("Press NUM for Car ")
        print("Press 0 for more")
        inp = int(input())
    return cars[inp-1]
def sortBy(cars,param) :
    size = len(cars)
    t = param
    minI = 0
    if param == 1 :
        for i in range(0, size) :
            d = i + 1
            for d in range(d, size) :
                if cars[d].price < cars[minI].price:
                    minI = d
            cars[i], cars[minI] = cars[minI], cars[i]  #  Swapping Two variables
    elif param == 2 :
        for i in range(0, size) :
            d = i + 1
            for d in range(d, size) :
                if cars[d].mpg < cars[minI].mpg:
                    minI = d
            cars[i], cars[minI] = cars[minI], cars[i]  #  Swapping Two variables
    elif t == 3 :
        for i in range(0, size) :
            d = i + 1
            for d in range(d, size) :
                if cars[d].hp < cars[minI].hp:
                    minI = d
            cars[i], cars[minI] = cars[minI], cars[i]  #  Swapping Two variables
    elif t == 4 :
        for i in range(0, size) :
            d = i + 1
            for d in range(d, size) :
                if cars[d].ft < cars[minI].ft:
                    minI = d
            cars[i], cars[minI] = cars[minI], cars[i]  #  Swapping Two variables
    return cars
def readCart(userS) :
    file = open("cart.pickle",'rb')
    items =[]
    try :
        while True :
             items.append(pickle.load(file))
    except :
        file.close()
    uitems =[]
    for item in items :
        if item.user.username == userS.username :
            uitems.append(item)
    return uitems
def readOrder(user) :
    file = open("orders.pickle",'rb')
    orders = []
    username = user.username
    try :
        while True :
            orders.append(pickle.load(file))
    except EOFError :
        file.close()
    i = 1
    print("Name                             : Time of Purchase")
    for order in orders :
        if order.user.username == username :
         carS = order.car
         print(str(i)+":"+str(carS)+" "+"               : "+str(order.buyTime))
         i += 1
def dashboard(user):
    os.system("cls")
    printHeader()
    print("Dashboard")
    print("1:Account Details")
    print("2.View Shortlist")
    print("3.View Purchases")
    print("4.Back")
    print("Enter your Options :")
    flag = int(input())
    if flag == 1 :
        os.system("cls")
        printHeader()
        user.printDetails()
        print("Any key to go back")
        input()
        dashboard(user)
    elif flag == 2 :
        os.system("cls")
        printHeader()
        items = readCart(user)
        if len(items) > 0  :
            print("Select Car : ")
            print("Enter 0 to go back ")
            i = 1
            for item in items :
                print(str(i)+" : "+str(item.car))
                i += 1
            flag = int(input())
            if not  flag == 0 :
                if getStock(item.car) > 0 :
                    removeShortlist(items[flag-1])
                    checkout(items[flag-1])
                    print("Car Bought")
                else :
                    print("Car Not in stock")
                    dashboard(user)
            else :
                dashboard(user)
        else :
            print("NO Cars in shortlist")
        print("Any key to go back")
        input()
        dashboard(user)
    elif flag == 3 :
        os.system("cls")
        printHeader()
        readOrder(user)
        print("Any key to go back")
        input()
        dashboard(user)
    elif flag == 4 :
        nation(user)
        time.sleep(10)
        print("Any key to go back")
        input()
        dashboard(user)
def removeShortlist(carte) :
    file = open("cart.pickle",'rb')
    items = []
    try :
        while True :
            items.append(pickle.load(file))
    except EOFError :
        file.close()
    for item in items  :
        if str(item.car) == str(item.car) and item.user.username == carte.user.username :
            items.remove(item)
            break
    file = open("cart.pickle",'wb')
    for item in items :
        pickle.dump(item,file)
#INTEREST
def findInterest(carS) :
    file = open("cart.pickle",'rb')
    wishes = []
    try :
        while True :
            wishes.append(pickle.load(file))
    except EOFError :
        file.close()
    i = 0
    for wish in wishes :
        if str(wish.car) == str(carS) :
            i += 1
    return i

'''
def rePickle () :
    file = open(CARS,'r',newline ='')
    cars = []
    with file :
        reader = csv.reader(file)
        for row in reader :
            cars.append(Car(row[0],row[1],row[2],Decimal(row[3])+Decimal(row[4]),int(row[5]),int(row[6]),Decimal(row[7]),Decimal(row[8]),Decimal(row[9]),Decimal(row[10]),Decimal(row[12]),Decimal(row[13]),int(row[14])))
    file = open("cars.pickle",'wb')
    for car in cars :
        pickle.dump(car,file)
rePickle()
'''
cars = readCars()
for car in cars :
    if not car.stock == car.getStock() :
        print(str(car))
#init()
def sendPurchaseMail(order):
    content = "Dear "+str(order.user)+"\n Car : "+str(order.car)+"\n"+"Price "+str(order.car.price)
    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login('carsnation9@gmail.com','kaizoku123')
    mail.sendmail('carsnation9@gmail.com',''+order.user.email, content)
    print("mail sent")
    mail.close()
def verifyMail(name,email) :
        passcode = random.randint(1000,9999)
        os.system("cls")
        printHeader()
        print("To confirm the account , check your email for the passcode :")
        content = "Dear "+str(name)+"\n PassCode :  "+str(passcode)+"\n"+"Regards \n CarsNation"
        mail = smtplib.SMTP('smtp.gmail.com',587)
        mail.ehlo()
        mail.starttls()
        mail.login('carsnation9@gmail.com','kaizoku123')
        mail.sendmail('carsnation9@gmail.com',email, content)
        print("mail sent")
        mail.close()
        print("Please Enter the code ")
        if int(input()) == passcode :
            return True
        print("Please try again another code has been sent")
        verifyMail(name,email)
def checkTrending() :
    cars = readCars()
    minI = 0
    for i in range(len(cars)) :
        minI = i
        for j in range(len(cars)) :
            if findInterest(cars[j]) < findInterest(cars[minI]) :
                minI = j
        cars[minI],cars[i] = cars[i],cars[minI]
    return cars
def inputValidate(start,end,inp) :
    if not type(inp) == "int" :
        return False
        inp = (int) (inp)
    if inp < start or inp > end :
        return False
    return True
#View details of the car
def viewCar(car) :
    os.system("cls")
    printHeader()
    print()
    car.printDetails()
    print()
    if InternetConnection :
        print("View More :")
        url = "https://www.google.co.uk/search?q={}".format(str(car))
        webbrowser.open_new_tab(url)
def checkout(item) :
    print (str(item.car))
    print("$ "+str(item.car.price))
    print(" Do you wish to buy this car: ")
    print(" Yes or No")
    userChoice = input()
    if userChoice.lower() == "yes":
        print (" Enter name as it appears in the credit card ")
        userName = input()
        print (" Enter your Credit Card Type")
        cardType = input()
        print (" Enter your credit card number ")
        cardNumber = int(input())
        while True :
            if validate(cardNumber) :
                break
            print("Incorrect CreditCard Number Type Again")
            cardNumber = int(input())
        print(" enter you credit card expiry date ")
        cardExpiry = input()
        order = Order(item)
        if InternetConnection :
            sendPurchaseMail(order)
            print("Mail Has been sent")
        return Order(item)
    else :
        return None
#4556737586899855
#Luhn's Formula
def validate(cardnumber) :
    cardDigits = []
    digit = 0
    while cardnumber > 0 :
        digit = cardnumber % 10
        cardDigits.append(digit)
        cardnumber = int(cardnumber/10)
    checkdigit = cardDigits[0]
    del cardDigits[0]
    for a in range(0,len(cardDigits)):
        if a % 2 == 0 :
                if (cardDigits[a] * 2 ) > 9 :
                    cardDigits[a]=(cardDigits[a]*2)-9
                else :
                    cardDigits[a] *= 2
    sum = 0
    for z in range (len(cardDigits)) :
  	   sum += cardDigits[z]
    if (sum) % 10  == checkdigit :
  	     return True
    else :
        return False
def getStock(car) :
    Stock = car.stock
    file = open("orders.pickle",'rb')
    orders = []
    try :
        while True :
            orders.append(pickle.load(file))
    except EOFError :
        file.close()
    for order in orders :
        if str(order.car) == str(car) :
            Stock -= 1
    if Stock <= 0 :
        return 0
    return Stock
init()
