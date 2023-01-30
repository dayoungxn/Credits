#Dayoung Nam, Grace Shi 
#ESC180, Project 1: Credit Cards 

#this function initializes and declares global variable
def initialize(): 
    #cur_balance_owing_recent does not accrue interest. 
    global cur_balance_owing_intst, cur_balance_owing_recent 
    global last_update_day, last_update_month
    global last_country, last_country2
    global account_status

    account_status = "Active"
    cur_balance_owing_intst = 0
    cur_balance_owing_recent = 0
    last_update_day, last_update_month =  0, 0
    last_country = None
    last_country2 = None    
    
#this function updates interest
def update_interest (day, month): 

    #declare global variables
    global cur_balance_owing_intst, cur_balance_owing_recent
    
    if month > last_update_month: 
        cur_balance_owing_intst = cur_balance_owing_intst * 1.05
        cur_balance_owing_intst += cur_balance_owing_recent
        cur_balance_owing_intst *= (1.05 ** (month - last_update_month - 1)) #subtract one so that the current month isn't accounted for twice
        cur_balance_owing_recent = 0

#subpart (a)
def date_same_or_later(day1, month1, day2, month2):
    if day1 == day2 and month1 == month2: 
        return True 
    elif month1 == month2 and day1 > day2: 
        return True
    elif month1 > month2:
        return True 
    else: 
        return False

#subpart (b)
def all_three_different(c1, c2, c3): 
    if c1 == None:
        return False
    if c1 != c2 and c2 != c3 and c1 != c3:
        return True #if true, then card is disable.
    else :
        return False  
    

#subpart (c)
def purchase(amount, day, month, country):
    #declare global variables 
    global last_update_day, last_update_month, last_country, last_country2, cur_balance_owing_intst, cur_balance_owing_recent, account_status
     #if all three countries are different, disable card and return error
    if all_three_different(last_country2, last_country, country) == True : #if card is disabled
        account_status = "Disabled" 
        #update date although card is disabled since purchase attempt was made.
        last_update_day = day 
        last_update_month = month
        return "error" 


    if date_same_or_later(day, month, last_update_day, last_update_month) == False : #there was a purchase later than day, month
        return "error" 


    #if it was previously disabled, return error. 
    if account_status == "Disabled":
        #update date although card is disabled since purchase attempt was made.
        last_update_day = day 
        last_update_month = month
        return "error"

    #update interest 
    update_interest (day, month)

    #add the money spent in cur_balance_owing_recent 
    cur_balance_owing_recent += amount 
    
    #update day and month
    last_update_day = day
    last_update_month = month    

    #update country 
    last_country2 = last_country
    last_country = country

#subpart (d)
def amount_owed(day,month):
    #declare global variables 
    global last_update_day, last_update_month, cur_balance_owing_intst, cur_balance_owing_recent

    #check if day is same or later 
    if not date_same_or_later(day, month, last_update_day, last_update_month) : 
        return "error" 


    #update interest 
    update_interest (day, month) 

    #update day and month
    last_update_day = day
    last_update_month = month

    #return amount owed
    return cur_balance_owing_intst + cur_balance_owing_recent


#subpart e
def pay_bill(amount, day, month): 

    #declare global variables
    global cur_balance_owing_recent, cur_balance_owing_intst, account_status
    global last_update_day, last_update_month

    #check if it is in chronological order
    if date_same_or_later(day, month, last_update_day, last_update_month) == False:
        return "error" 

    #update interest 
    update_interest (day, month)

    #when bill is paid, 'amount' is subtracted from the debt.  
    cur_balance_owing_intst -= amount 
    if cur_balance_owing_intst < 0:
        cur_balance_owing_recent += cur_balance_owing_intst 
        cur_balance_owing_intst = 0  

    #update day and month
    last_update_day = day
    last_update_month = month



if __name__ == '__main__':
    #test cases given
    initialize()
    purchase(80, 8, 1, "Canada")
    print("Now owing:", amount_owed(8, 1))      # 80.0                                    (Test1)
    pay_bill(50, 2, 2)
    print("Now owing:", amount_owed(2, 2))      # 30.0     (=80-50)                       (Test2)
    print("Now owing:", amount_owed(6, 3))      # 31.5     (=30*1.05)                     (Test3)
    purchase(40, 6, 3, "Canada")
    print("Now owing:", amount_owed(6, 3))      # 71.5     (=31.5+40)                     (Test4)
    pay_bill(30, 7, 3)
    print("Now owing:", amount_owed(7, 3))      # 41.5     (=71.5-30)                     (Test5)
    print("Now owing:", amount_owed(1, 5))      # 43.65375 (=1.5*1.05*1.05+40*1.05)       (Test6)
    purchase(40, 2, 5, "France")
    print("Now owing:", amount_owed(2, 5))      # 83.65375                                (Test7)
    print(purchase(50, 3, 5, "United States"))  # error    (3 diff. countries in          (Test8)
                                                #          a row)
                                                
    print("Now owing:", amount_owed(3, 5))      # 83.65375 (no change, purchase           (Test9)
                                                #           declined)
    print(purchase(150, 3, 5, "Canada"))        # error    (card disabled)                (Test10)
    print("Now owing:", amount_owed(1, 6))      # 85.8364375                              (Test11)
                                                # (43.65375*1.05+40)

   
    #more test cases to ensure code runs properly 
    initialize() 
    purchase(60, 6, 2, "France")
    print("Now owing:", amount_owed(6, 2))      # 60.0                                    (Test1)
    pay_bill(50, 2, 2)
    print("Now owing:", amount_owed(2, 2))      # error          (chronological error)    (Test2)
    pay_bill(50, 3, 4)
    print("Now owing:", amount_owed(8, 9))      # 16.5916603125  (60*1.05-50)*1.05^5      (Test3)