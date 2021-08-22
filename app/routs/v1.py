from fastapi import FastAPI, Body, HTTPException, Header, Depends, APIRouter, Query
from typing import Optional
from app.models.users import User
from app.models.groups import Group
from app.models.expense import TypeofExpense, Expense
from starlette.status import HTTP_201_CREATED
from typing import List
import json

# App version : v1
app_v1 = APIRouter()


# Defining in memory solution
user_name_list = []
balance_list = dict()
group_list = dict()

# --------------- user's CURD operations -----------------------
@app_v1.post("/user/createUser", status_code=HTTP_201_CREATED, description="It creates New user", tags=["Users"])
async def create_user(user: User):
    if user.name in user_name_list:
        return {"Error" : f"Please give some unique user name . This user {user.name} does already exist"}
    user_name_list.append(user.name)
    return {"unique user created ": user.name}


@app_v1.get("/user/getAllUsers", status_code=201, description="Retuns All user List", tags=["Users"])
async def get_all_users_list():
    return {"userList" : [*user_name_list]}



# -------------- Group CURD operations -------------------------------

@app_v1.post("/group/create/{group_name}", status_code=HTTP_201_CREATED, description="It creates New Group , just pass userlist values", tags=["Group"])
async def create_group(group : Group):
    print(len(group.userlist))
    if group.userlist is None or len(group.userlist)-1 == 0:
        return {"Not None Error" : "Group Can not created without members , atleast add one memeber!"}
    elif group.name in group_list.keys():
        return {"Duplicate group error" : "Following group already exist, please provide some unique name"}
    else:
        group_list[group.name] = group.userlist
        return {"Group created ": f"{group.name}"}

@app_v1.get("/group/name/{group_name}", description="It returns the availble group name", tags=["Group"])
async def get_group_name(name : str):
    for existgroup, members in group_list.items():
        if name == existgroup:
            return {"Group exists with following members" : f"{members}"}
    return {"Not Found Error" : "Following group name not found"}

@app_v1.post("/group/delete/name/{group_name}", status_code=201, description="It delete the group entry", tags=["Group"])
async def delete_group(name : str):
    if name in group_list.keys():
        del group_list[name]
        return {"Following group is deleted" : f"{name}"}
    return {"Not Found Error" : "Following group name not exist"}

# ----------------- Expense CURD Operations ------------------------------

expense_db = [{}]

@app_v1.post("/expense/createExpense/", status_code=201, description="It creates new expenses", tags=["Expense"])
async def create_expense(user: list, amount : float , paidBy : User, expensetype : TypeofExpense):
    if paidBy.name in user_name_list:
        temp = {
            "user" : user, #[ mahima, soni , user1 ]
            "amount" : amount,
            "paidBy" : paidBy,
            "expensetype" : expensetype
        }
        expense_db.append(temp)
        split_amount = calculate_split_ammount(expensetype, len(temp['user']), amount)
        #print("----------------->" , split_amount)
        for owed_users in temp['user']:
            if owed_users not in balance_list:
                balance_list[owed_users] = split_amount
            else:
                # amount will get add
                balance_list[owed_users] += split_amount
        return {"Expense has created" : f"{temp}"}
    return {"Not Found Error" : "Following paidBy user name not exist. please check if user exist"}


@app_v1.get("/expense/getExpense/{user_name}", description="It returns the new expense", tags=["Expense"])
async def get_user_expense(user_name : str):
    if user_name in balance_list:
        return {"The total expense on user is" : f"{balance_list[user_name]}"}
    return {"Not found Error" : "The following user doesn't exist"}


#-------------------- Settlement CURD API----------------------------------

@app_v1.post("/settlement/user/{user_name}", description="It settle the balance between userA to userB", tags=["Settlement"])
async def settle_balance(fromUser : User, ToUser : User, ammount : float):
    if ToUser.name in user_name_list:
        ammount = settle_from_usera_to_userb(fromUser.name, ToUser.name, ammount)
        return {"Success " : f"The due ammount is {ammount}"}
    return {"ToUser Not found" : f"The user not found in db {ToUser}"}



# ------------------------------------- 
def cal_percentage(amount, val = list()):
    n = len(val)
    quotient = 1 / n
    percentage = quotient * 100
    return percentage

def calculate_split_ammount(expensetype, values, ammount):
    print(expensetype, values, ammount)
    a = str(expensetype)
    a = a.split('.')[1]
    ans = 0
    if a == "PERCENTAGE":
        if values:
            ans = cal_percentage(ammount, len(values))
    if a == "EQUALS":
        ans = ammount / (values+1)
        
    return ans

def settle_from_usera_to_userb(user_who_want_to_pay, user_to_whom_pay, ammount):
    for exist_user in expense_db[1:]:
        s1 = json.dumps(exist_user['paidBy'].__dict__)
        s1 = json.loads(s1)
    
        if s1['name'] == user_to_whom_pay:
            balance_list[user_who_want_to_pay] -= ammount
            if balance_list[user_who_want_to_pay] == 0:
                print("The balance is settled")
                return 0
            else:
                return balance_list[user_who_want_to_pay]
        else:
            return Exception("User doesn't exist")
