import os
import random
import logging
import helper.msg
from sys import exit
import logging.config
from typing import List
from user.user import User
from datetime import datetime
from product.products import Product
from helper.msg import DISCOUNT_CODES
from shopping_list.shopping_list import ShoppingList
from helper.msg import (CommandsMsg,
ListMsg, 
ProductMsg, 
InfoMsg, 
CodeMsg, 
DeliveryMsg, 
FactureMsg)


logging.config.fileConfig(fname='log/handler.toml', disable_existing_loggers=False)
logger=logging.getLogger("log/authLogger")
date = datetime.now()



os.system("cls" if os.name == 'nt' else "clear")
while True:
    registration_mode: str =input('have you registered in our site?:[YES/NO] ').upper()
    match registration_mode:
        case "YES":
            # we ask for username
            # we check if username is available in our database by user pass check method
            # if user name is available the method checks the password
            # if both are right then it makes log in user true
            username: str =input(InfoMsg.enter_username)
            password: str =input(InfoMsg.enter_password)
            # as long as check user pass returns bool we put it in a var
            # if the var is true it means user log in was successful
            # so the logger logs user log in
            logged_in: bool =User.check_user_password("user_info.json", username, password)
            if logged_in is True:
                print(f'{username} you are logged in your account')
                logger.info(f'{username} have been logged in')
                break
            else:
                continue
        case "NO":
            # our user class need username full name address password phone number
            # we get all these info as input
            # we define instance of class with all these input
            print('please fill in your information to create an account')
            username: str =input(InfoMsg.enter_username)
            full_name: str =input(InfoMsg.enter_full_name)
            address: str =input(InfoMsg.enter_address)
            while True:
                password: str =input(InfoMsg.enter_password)
                password_confirm: str =input(InfoMsg.enter_pass_confirm)
                if password==password_confirm:
                    break
                else:
                    print(InfoMsg.confirm_failed)
                    continue
            phone_number: str =input(InfoMsg.enter_phone)
            user_info: object =User(username, full_name, address, phone_number, password)
            # we use write user info method and write info of instance we made in file
            user_info.write_users_info('user_info.json')
            logger.info(f'{username} registered')
            break
        case _:
            print(CommandsMsg.invalid_command)


os.system("cls" if os.name == 'nt' else "clear")
while True:
    # when user log in we give user option to win discount code
    # user can see their info and then can change info or keep with prev info
    # user can get out of user bar
    # user can quit the app
    helper.msg.user_bar_help()
    user_command: str =input(CommandsMsg.chose_command)
    match user_command:
        case '1':
            password, full_name, address, phone_number=User.get_users_info('user_info.json', username)
            logged_in_user : object =User(username, full_name,address,phone_number,password)
            logged_in_user.read_users_info('user_info.json')
            # user see their info
            # user have option to change info or not
            while True:
                to_edit_info: str =input(InfoMsg.edit_info)
                match to_edit_info:
                    case "1":
                        password, full_name, address, phone_number=User.get_users_info('user_info.json', username)
                        print(helper.msg.edit_info_help())
                        info_edit_type : str =input(CommandsMsg.chose_command).upper()
                        # we get new info and make instance 
                        # we put new info inside dict and
                        # delete prev info and overwrite new info by edit info method
                        match info_edit_type:
                            case 'USERNAME':
                                new_username : str =input(InfoMsg.enter_n_username)
                                username=new_username
                                continue
                            case 'NAME':
                                new_full_name : str =input(InfoMsg.enter_n_full_name)
                                full_name=new_full_name
                                continue
                            case 'PHONE':
                                new_phone: str =input(InfoMsg.enter_n_phone)
                                phone_number=new_phone
                                continue
                            case 'ADDRESS':
                                new_address : str =input(InfoMsg.enter_n_address)
                                address=new_address
                                continue
                            case 'PASSWORD':
                                while True:
                                    # we ask for new pass and its confirmation 
                                    # if those two match then we can continue
                                    new_password : str =input(InfoMsg.enter_n_password)
                                    new_password_confirm : str =input(InfoMsg.enter_n_pass_confirm)
                                    if new_password == new_password_confirm:
                                        password=new_password
                                        break
                                    else:
                                        print(InfoMsg.confirm_failed)
                                        continue
                            case 'CONTINUE':
                                break
                            case _:
                                print(CommandsMsg.invalid_command)
                        # we make new instance by new infos 
                        new_user_info: object =User(username, full_name, address, phone_number, password)
                        new_user_info.edit_user_info('user_info.json')
                    case "2":
                        break
                    case _:
                        print(CommandsMsg.invalid_command)
                        continue
        case '2':
            code : List= random.choices(DISCOUNT_CODES, weights=[1, 2, 3, 4])
            if code[0] == 'CHRISTMAS':
                print(CodeMsg.christmas_code)
            elif code[0] == 'MYBIRTHDAY':
                print(CodeMsg.birthday_code)
            elif code[0] == 'GOLDMEMBER':
                print(CodeMsg.gold_member_code)
            else:
                print(CodeMsg.no_discount)
        case '3':
            break
        case '4':
            exit()
        case _:
            print(CommandsMsg.invalid_command)


os.system("cls" if os.name == 'nt' else "clear")
shop: object = ShoppingList()
while True:
    new_item: str =input(ListMsg.add_item).upper().strip()
    os.system("cls" if os.name == 'nt' else "clear")
    if new_item not in shop.items:
        match new_item:
            case "SEARCH":
                to_search_item: str=input(ListMsg.item_search).upper()
                shop.search_item(to_search_item)
            case "DELETE":
                to_delete_item: str=input(ListMsg.item_delete).upper()
                shop.delete_item(to_delete_item)
            case "SHOW":
                shop.show()
            case "DONE":
                break
            case "PRODUCTS":
                category: str=input(ProductMsg.product_category).upper()
                Product.get_categories('shopping_list_data.json', category)
            case _:
                available_products=Product.check_available_products('shopping_list_data.json')
                if new_item in available_products:
                    shop.add_item(new_item)
                else:
                    print(helper.msg.not_exist_message())
    else:
        print(helper.msg.exist_message())

shopping_list: List=shop.items
costs: List = list()
for i in range(len(shopping_list)):
    quantity = int(input(f'how many boxes of {shopping_list[i]} you want?: '))
    os.system("cls" if os.name == 'nt' else "clear")
    available_products_dict=Product.get_products_dict('shopping_list_data.json')
    value_of_item = int(available_products_dict[shopping_list[i]])
    item_cost = (quantity)*(value_of_item)
    costs.append(item_cost)

# calculating total cost
for item_cost in costs:
    total: int = sum(costs)

discount_code:str = input(CodeMsg.get_code).upper() # noqa E501
os.system("cls" if os.name == 'nt' else "clear")
# use these discount code for different percentage of discount
# christmas: 50% off
# mybirthday 30% off
# goldmember 10% off
if discount_code in DISCOUNT_CODES:
    match discount_code:
        case "CHRISTMAS":
            discounted_total_price = (total*50)/100
        case "MYBIRTHDAY":
            discounted_total_price = (total*70)/100
        case "GOLDMEMBER":
            discounted_total_price = (total*90)/100
else:
    discounted_total_price = CodeMsg.no_discount_shop



while True:
    delivery: str = input(DeliveryMsg.chose_delivery)
    delivery_codes: list = ['1', '2']
    if delivery not in delivery_codes:
        print(CommandsMsg.invalid_command)
        continue
    else:
        break

print(FactureMsg.finish_msg)
print(FactureMsg.lines)
print(FactureMsg.header)

for k in range(len(shopping_list)):
    item_name = shopping_list[k]
    item_price = available_products_dict.get(shopping_list[k])
    print('\t{}\t\t${}'.format(item_name.title(), item_price))

print(FactureMsg.lines)
print('\t\t\tTotal')
print('\t\t\t${}'.format(total))
print(FactureMsg.lines)
print('\t\t\ttotal cost after discount')
print('\t\t\t${}'.format(discounted_total_price))

print(FactureMsg.lines)
print(FactureMsg.finish_time.format(date))
if delivery == '1':
    print(DeliveryMsg.pick_up)
if delivery == '2':
    print(DeliveryMsg.delivery)
    password, full_name, address, phone_number=User.get_users_info('user_info.json', username)
    customer=User(username, full_name,address,phone_number,password)
    customer.read_users_info('user_info.json')