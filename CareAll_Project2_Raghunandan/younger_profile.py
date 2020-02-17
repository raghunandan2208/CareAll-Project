from db import *

class YoungerProfile():
    def __init__(self, email, password):
        self.email = email
        self.password = password
        try:
            sql = f'SELECT PK_user_id, name FROM users WHERE email = "{self.email}" '
            mycursor.execute(sql)
            user_id = mycursor.fetchone()
            self.user_id = user_id[0]
            self.younger_name = user_id[1]
            sql = f'SELECT PK_younger_id FROM youngers WHERE FK_user_id={self.user_id}'
            mycursor.execute(sql)
            younger_id = mycursor.fetchone()
            self.younger_id=younger_id[0]
            sql = f'SELECT FK_younger_id from caretaking where FK_younger_id = {self.user_id}'
            mycursor.execute(sql)
            self.youngerCount = mycursor.fetchall()
        except TypeError:
            print("This email is not registered with us. Please register or try again with other one")
            print("-"*50)
            import index

    def log_in(self):
        #retrieving passwords for registered mobile no from both table
        sql = f'SELECT password FROM users WHERE email= "{self.email}" '
        mycursor.execute(sql)
        user_info = mycursor.fetchone()     # fetchall provides empty list if record does not exists
        if user_info==[]:
            print(f'{self.email} ot registered. Please try to register first')
            import index      # due to mutual importing we are importing here just before method calling
        elif self.password==user_info[0]:
            print("Logged IN")
            self.dashboard_younger()
        else:
            print("Wrong email and password")
            import index

    def dashboard_younger(self):
        elderCount = len(self.youngerCount)
        print(f'Currentlty you are taking care of {elderCount} Elders\nYou can request for {4-elderCount} more elders to take care of.\n1.View list of Available elders to take care of.\n2.Give review and rating for a elder\n3.Check Account Balance\n4.LogOut')
        choice = int(input())
        if choice==1:
            self.request_elder()
        elif choice==2:
            self.review()
        elif choice==3:
            self.account_balance()
        elif choice==4:
            self.log_out()

    # user should be able to see list of available elder and sent them request. NOTE:- 1 user can't sent request to same elder twice
    def request_elder(self):
        elderCount = len(self.youngerCount)
        if elderCount < 4:                  # Checks the count of elders that younger is taking care of (not exeding 4 elders)
            sql = f'SELECT * FROM elders WHERE available = True'
            mycursor.execute(sql)
            available_list = mycursor.fetchall()
            sql1 = "select fk_younger_id, fk_elder_id from request"
            mycursor.execute(sql1)
            sent_request = mycursor.fetchall()
            FK_el_id = []
            for id in available_list:
                new_id = id[1]
                rating = (0 if id[5] == None else id[5])
                available_sql = "select pk_user_id,name,mobile from users where pk_user_id = {}".format(new_id)
                mycursor.execute(available_sql)
                list_items = mycursor.fetchall()
                FK_el_id.append(list_items[0][0])
                print("Elder-id: {}\t  Name: {}\t  Contact: {}\t Rating: {}".format(list_items[0][0],list_items[0][1],list_items[0][2],rating))
                print("-"*50)

            while True:         # if a user select wrong option it will ask again to select option
                request = int(input("Enter Elder ID whom you want to take care: "))
                if (self.user_id,request) not in sent_request:      #Checks weather younger sent request to selected elder or not.
                    if request in FK_el_id:             #Checks if selected yelder in list or not
                        sql = "INSERT INTO request (FK_younger_id,FK_elder_id,request_status) VALUES ({},{},{})".format(self.user_id,request,True)
                        mycursor.execute(sql)
                        mydb.commit()
                        print("Your request is been accepted and under process...")
                        self.dashboard_younger()
                        break
                    else:
                        print("Invalid option, please select from above choices")
                else:
                    print("You have already sent request for this elder")

        else:
            print("You are already taking care of 4 elders. So, you are not eligible to send another request.")
        self.dashboard_younger()

    # younger can give rating and rating to elders
    def review(self):
        print("Kindly provide your review and rating for the Elder whoom you taken care of...")
        review_id = int(input("Enter Elder ID: "))
        review_user = input("Provide your review: ")
        rating_user = int(input("Provide rating on a scale of 1 to 5: "))
        sql = "INSERT INTO reviews (FK_user_id,review,rating,review_by) VALUES ({},'{}',{},'{}')".format(review_id,review_user,rating_user,self.younger_name)
        mycursor.execute(sql)
        mydb.commit()
        sql2 = "select rating from reviews where FK_user_id = {}".format(review_id)
        mycursor.execute(sql2)
        rating_list = mycursor.fetchall()
        lst = [rating[0] for rating in rating_list]
        avg_rating = round(sum(lst)/len(lst),1)         # Calculates average rating of particular elder
        sql3 = "UPDATE elders SET rating = {} WHERE FK_user_id = {}".format(avg_rating,review_id)
        mycursor.execute(sql3)
        mydb.commit()
        print("Thankyou for sharing your valuble feedback...")
        print("-"*50)
        self.dashboard_younger()

# Younger can check his account balance
    def account_balance(self):
        sql = "select balance from younger_money where FK_younger_id = {}".format(self.user_id)
        mycursor.execute(sql)
        balance = mycursor.fetchone()
        print("Your current account balance is Rs.{}".format(balance[0]))
        self.dashboard_younger()

    def log_out(self):
        import index
