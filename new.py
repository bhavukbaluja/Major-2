import bcrypt


def welcome():
    print("Welcome to the Dashboard!!")


def gainAccess(id=None, p=None):
    id = input("Enter your username:")
    p = input("Enter your Password:")

    if not len(id or p) < 1:
        if True:
            db = open("database.txt", "r")
            d = []
            f = []
            for i in db:
                a, b = i.split(",")
                b = b.strip()
                c = a, b
                d.append(a)
                f.append(b)
                data = dict(zip(d, f))
            try:
                if id in data:
                    hashed = data[id].strip('b')
                    hashed = hashed.replace("'", "")
                    hashed = hashed.encode('utf-8')

                    try:
                        if bcrypt.checkpw(p.encode(), hashed):

                            print("Login success!")
                            print("Hi", id)
                            welcome()
                        else:
                            print("Wrong Password!")

                    except:
                        print("Incorrect Password or Username")
                else:
                    print("Username doesn't exist")
            except:
                print("Password or username doesn't exist")
        else:
            print("Error logging into the system")

    else:
        print("Please attempt login again")
        gainAccess()

    print("Do you want to continue?")
    option = input("Yes/No?")
    if option == "Yes" or option=="y" or option=="Y":
        home()
    else:
        print("Thank you for using this application!")
    # b = b.strip()


# accessDb()

def register(id=None, P1=None, P2=None):
    id = input("Enter a username:")
    P1 = input("Create password:")
    P2 = input("Confirm Password:")
    db = open("database.txt", "r")
    d = []
    for i in db:
        a, b = i.split(",")
        b = b.strip()
        c = a, b
        d.append(a)
    if not len(P1) <= 3:
        db = open("database.txt", "r")
        if not id == None:
            if len(id) < 1:
                print("Please provide a username")
                register()
            elif id in d:
                print("Username exists")
                register()
            else:
                if P1 == P2:
                    P1 = P1.encode('utf-8')
                    P1 = bcrypt.hashpw(P1, bcrypt.gensalt())

                    db = open("database.txt", "a")
                    db.write(id + ", " + str(P1) + "\n")
                    print("User created successfully!")
                    print("Please login to proceed!")


                # print(texts)
                else:
                    print("Passwords do not match!")
                    register()
    else:
        print("Password too short")
    print("Do you want to continue?")
    option = input("Yes/No?")
    if option == "Yes" or option=="y" or option=="Y":
        home()
    else:
        print("Thank you for using this application!\nHave a Nice Day!")


def home(option=None):
      print("Welcome, Please select an option")
      option = input("Select:\n1: Login\n2: Signup\n")
      if option == "1":
          gainAccess()
      elif option == "2":
          register()
      else:
          print("Please enter a valid parameter, this is case-sensitive")
          home()
