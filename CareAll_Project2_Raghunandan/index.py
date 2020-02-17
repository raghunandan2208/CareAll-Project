from db import *
from profile import User
from younger_profile import YoungerProfile
from elder_profile import ElderProfile

# welcome note and giving option to login or register
def welcome():
    print("-"*50)
    print("**************************************WELCOME TO CARE-ALL PROJECT******************************************")
    print("-"*50)
    print("Please select your option\n1. Login as Elder \n2. Login as Younger\n3. Register\n4. View all youngers who are taking care\n5. View who is taking care of older couple\n6. Exit")
    task = int(input())
    if task==1:
        email = input("Welcome Elder\nEnter Your Email: ")
        password = input("Enter Your Password: ")
        user = ElderProfile(email, password)
        user.log_in()

    elif task==2:
        email = input("Welcome younger\nEnter Your Email: ")
        password = input("Enter Your Password: ")
        user = YoungerProfile(email, password)
        user.log_in()

    elif task==3:
        name = input("Register Yourself\nEnter Your Full Name: ")
        email = input("Enter your email: ")
        mobile = input("Enter Your Mobile Number: ")
        password = input("Enter Your Password: ")

        # if a user select wrong option it will ask again to select option
        while True:
            role = int(input("select your role:\n1. Elder\n2. Younger\n"))
            try:
                if role==1:
                    role="elder"
                    break
                elif role==2:
                    role="younger"
                    break
            except:
                print(f'option not Valid! Please try again')

        user_signup = User(name, email, password, mobile, role)
        user_signup.user_registration()

    # display name of youngers who are taking care of
    elif task==4:
        sql = "select FK_user_id, rating from youngers"
        mycursor.execute(sql)
        fk_id = mycursor.fetchall()
        for id in fk_id:
            new_id = id[0]
            rating = id[1]
            available_sql = "select pk_user_id,name,mobile from users where pk_user_id = {}".format(new_id)
            mycursor.execute(available_sql)
            list_items = mycursor.fetchall()
            print("Younger-id: {}\t  Name: {}\t  Contact:{}\t Rating: {} ".format(list_items[0][0],list_items[0][1],list_items[0][2],rating))
        print("-"*50)
        option = int(input("Choose your choice: \n1. Main Menu\n2. Exit\n"))
        if option == 1:
            import index
        else:
            exit()

    # enter elder's email and password here to display their take care name
    elif task==5:
        print("Please enter Elder registered Email-ID and Password: ")
        email = input("Email-ID: ")
        pwd = input("Password: ")
        elder = ElderProfile(email,pwd)
        elder.take_care_name()
        print("-"*50)
        option = int(input("Choose your choice: \n1. Main Menu\n2. Exit\n"))
        if option == 1:
            import index
        else:
            exit()

    elif task==6:
        exit()

welcome()
