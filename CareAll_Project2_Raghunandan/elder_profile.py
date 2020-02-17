from db import *

class ElderProfile():
    def __init__(self, email, password):
        self.email = email
        self.password = password
        try:
            sql = "SELECT PK_user_id, name FROM users WHERE email = '{}'".format(self.email)
            mycursor.execute(sql)
            user_id = mycursor.fetchone()
            self.user_id = user_id[0]
            self.elder_name = user_id[1]
            sql = "SELECT PK_elder_id FROM elders WHERE FK_user_id={}".format(self.user_id)
            mycursor.execute(sql)
            elder_id = mycursor.fetchone()
            self.elder_id=elder_id[0]
            sql = "select FK_user_id from elders where PK_elder_id = {}".format(self.elder_id)
            mycursor.execute(sql)
            fk_id = mycursor.fetchone()
            self.FK_e_id = fk_id[0]
        except TypeError:
            print("This email is not registered with us. Please register or try again with other one")
            print("-"*50)
            import index

    def log_in(self):
        #retrieving passwords for registered email
        sql = f'SELECT password FROM users WHERE email= "{self.email}" '
        mycursor.execute(sql)
        user_info = mycursor.fetchone()     # fetchall provides empty list if record does not exists
        if user_info==[]:
            print(f'{self.email} not registered. Please try to register first')
            import index      # due to mutual importing we are importing here just before method calling
        elif self.password==user_info[0]:
            print("Logged IN")
            print("-"*50)
            self.dashboard_elder()
        else:
            print("Wrong email and password")
            import index
# Dashboard of elder
    def dashboard_elder(self):
        sql = f'SELECT available FROM elders where PK_elder_id = {self.elder_id}'
        mycursor.execute(sql)
        user_info = mycursor.fetchone()
        if user_info[0]==1:
            print("-"*50)
            print("You are currently Available to take care of.\n1.Make Unavailable\n2.Fund\n3.Request care taker\n4.Take Care Name\n5.Give review and rating for a care taker\n6.Pay Younger or Free-up Younger\n7. LogOut")
            choice = int(input())
            if choice==1:
                self.change_status()
                self.dashboard_elder()
            elif choice==2:
                self.allocate_fund()
            elif choice==3:
                self.show_request()
            elif choice==4:
                self.take_care_name()
            elif choice==5:
                self.review()
            elif choice==6:
                self.free_caretaker()
            elif choice==7:
                self.log_out()

        else:
            print("You are currently Unavailable to take care of.\n1.Change Status\n2.Log Out")
            choice = int(input())
            if choice==1:
                self.change_status()
                self.dashboard_elder()
            elif choice==2:
                self.log_out()

    # elder should be able to allocate fund
    def allocate_fund(self):
        amount = int(input("Enter amount:"))
        sql1 = "select fund from elders where PK_elder_id = {}".format(self.elder_id)
        mycursor.execute(sql1)
        current_balance = mycursor.fetchone()[0]
        if current_balance != None:
            update_balance = current_balance + amount   #Updates existing balance
            sql = "UPDATE elders SET fund = {} WHERE PK_elder_id = {}".format(update_balance,self.elder_id)
            mycursor.execute(sql)
            mydb.commit()
            print("Amount added successfully")
        else:
            sql = "UPDATE elders SET fund = {} WHERE PK_elder_id = {}".format(amount,self.elder_id)
            mycursor.execute(sql)
            mydb.commit()
            print("Amount added successfully")
        sql2 = "select fund from elders where PK_elder_id = {}".format(self.elder_id)
        mycursor.execute(sql2)
        present_balance = mycursor.fetchone()[0]
        print("Your current account balance is Rs.{}".format(present_balance))      #Displays current balance
        print("-"*50)
        option = int(input("Choose your choice: \n1. Dashboard\n2. Main menu\n"))
        if option == 1:
            self.dashboard_elder()
        else:
            import index


# Bill will be generated after elder availing services/free up younger
    def bill_section(self,amount):
        self.amount = amount
        sql1 = "select fund from elders where PK_elder_id = {}".format(self.elder_id)
        mycursor.execute(sql1)
        current_balance = mycursor.fetchone()[0]
        new_balance = current_balance - amount
        sql = "UPDATE elders SET fund = {} WHERE PK_elder_id = {}".format(new_balance,self.elder_id)
        mycursor.execute(sql)
        mydb.commit()
        print("Your bill amount Rs.{} has been debited from your account. Your current account balance is Rs.{}".format(amount, new_balance))
        print("-"*50)
        print("""*************HOPE YOU ENJOYED OUR SERVICES***************
                ******************THANK YOU**************""")
        print("-"*50)

    # elder can change their status
    def change_status(self):
        status = ''
        choice = int(input("Enter your status:\n1. Available \n2. Unavailable \nEnter your option: "))
        if choice == 1:
            status = True
        elif choice == 2:
            status = False
        sql = "UPDATE elders SET available = {} WHERE PK_elder_id = {}".format(status,self.elder_id)
        mycursor.execute(sql)
        mydb.commit()
        print("Status changed")
        print("-"*50)
        self.dashboard_elder()

    # elder can see requests and accept whome they trus only 1 request can be accepted by elder
    def show_request(self):
        sql1 = "select fund from elders where PK_elder_id = {}".format(self.elder_id)
        mycursor.execute(sql1)
        acc_balance = mycursor.fetchone()[0]
        sql3 = "SELECT * FROM request WHERE FK_elder_id = {} and request_status = True".format(self.FK_e_id)
        mycursor.execute(sql3)
        available_list = mycursor.fetchall()

        for id in available_list:
            new_id = id[1]
            available_sql = "select pk_user_id,name,mobile from users where pk_user_id = {}".format(new_id)
            mycursor.execute(available_sql)
            list_items = mycursor.fetchall()
            sql = "select rating from youngers where FK_user_id = {}".format(new_id)
            mycursor.execute(sql)
            rating = mycursor.fetchone()
            result = [0 if rating == None else rating[0]]
            print("User-id: {}\t Name: {}\t Contact: {}\t Rating: {}".format(list_items[0][0], list_items[0][1], list_items[0][2], result))
        print("-"*50)
        request = int(input("Choose youngstar ID whom you like to have: "))
        if acc_balance == None or acc_balance < 5000:           # Checks for the account balance of elder to raise request (Minimum bal. Rs.5000)
            print("You are not eligible to avail our services due to insufficient funds. Please make sure that your minimum account balance is Rs. 5000.")
            print("-"*50)
            self.allocate_fund()        # Redirects to allocate fund if there is no sufficient balance.
        else:
            sql4 = "INSERT INTO caretaking (FK_elder_id,FK_younger_id) VALUES ({},{})".format(self.FK_e_id,request)
            mycursor.execute(sql4)
            mydb.commit()
            sql5 = "DELETE FROM request where fk_younger_id = {} and fk_elder_id ={}".format(request,self.FK_e_id) #younger request will be deleted after hiring
            mycursor.execute(sql5)
            mydb.commit()
            print("Your request is been accepted")
            print("-"*50)
            self.dashboard_elder()

    # elder can see name of younger who is taking care of them
    def take_care_name(self):
        sql1 = "select FK_younger_id from caretaking where FK_elder_id = {}".format(self.FK_e_id)
        mycursor.execute(sql1)
        available_list = mycursor.fetchall()
        if len(available_list) != 0:
            for id in available_list:
                new_id = id[0]
                available_sql = "select pk_user_id,name,mobile from users where pk_user_id = {}".format(new_id)
                mycursor.execute(available_sql)
                list_items = mycursor.fetchall()
                print("Younger-id: {}\t Name: {}\t Contact:{} ".format(list_items[0][0],list_items[0][1],list_items[0][2]))
        else:
            print("You have not choosen any younger to take care of you")
            print("-"*50)

    # elder can give review and rating to youngers
    def review(self):
        self.take_care_name()
        print("Kindly provide your review and rating for the Younger who taken care of you...")
        review_id = int(input("Enter younger ID: "))
        review_user = input("Provide your review: ")
        rating_user = int(input("Provide rating on a scale of 1 to 5: "))
        sql = "INSERT INTO reviews (FK_user_id,review,rating,review_by) VALUES ({},'{}',{},'{}')".format(review_id,review_user,rating_user,self.elder_name)
        mycursor.execute(sql)
        mydb.commit()
        sql2 = "select rating from reviews where FK_user_id = {}".format(review_id)
        mycursor.execute(sql2)
        rating_list = mycursor.fetchall()
        lst = [rating[0] for rating in rating_list]
        avg_rating = round(sum(lst)/len(lst),1)         # Converts to average rating
        sql3 = "UPDATE youngers SET rating = {} WHERE FK_user_id = {}".format(avg_rating,review_id)
        mycursor.execute(sql3)
        mydb.commit()
        print("Thankyou for sharing your valuble feedback...")
        print("-"*50)

# To free up care taker and bill will be generated to elder
    def free_caretaker(self):
        print("-"*50)
        self.take_care_name()
        print("-"*50)
        print("Choose your option:\n1) Pay Younger\n2) Free up younger\n3) Return to Dashboard")
        option = int(input("Enter your option: "))
        if option == 1:
            pay_younger_id = int(input("select user-id of Younger whoom you want to pay: "))
            amount = int(input("Enter amount to pay younger: "))
            print("-"*50)
            self.bill_section(amount)
            sql1 = "select balance from younger_money where FK_younger_id = {}".format(pay_younger_id)
            mycursor.execute(sql1)
            current_balance = mycursor.fetchone()[0]
            new_balance = current_balance + amount
            sql = "UPDATE younger_money SET balance = {} WHERE FK_younger_id = {}".format(new_balance,pay_younger_id)
            mycursor.execute(sql)
            mydb.commit()
            self.dashboard_elder()

        elif option == 2:
            free_up_id = int(input("select user-id of Younger whoom you want to leave: "))
            print("-"*50)
            self.review()
            print("-"*50)
            sql = "DELETE FROM caretaking where fk_younger_id = {} and fk_elder_id ={}".format(free_up_id,self.FK_e_id)
            mycursor.execute(sql)
            mydb.commit()
            sql1 = "DELETE FROM request where fk_younger_id = {} and fk_elder_id ={}".format(free_up_id,self.FK_e_id)
            mycursor.execute(sql1)
            mydb.commit()
            print("Your request is been accepted")
            print("-"*50)
            self.dashboard_elder()

        elif option == 3:
            self.dashboard_elder()

        else:
            print("Please choose correct option")
            self.free_caretaker()

    def log_out(self):
        import index
