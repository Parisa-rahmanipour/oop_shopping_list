import logging
import logging.config
import json


logging.config.fileConfig(fname='log/handler.toml', disable_existing_loggers=False)
logger=logging.getLogger("log/authLogger")

class User:                                           
    """
    this class is about user which make instance of user and 
    each instance of this user have username, password, name,
    phone number and address
    """
    def __init__(self, username, fullname, address, phone, password) :
        self.username=username
        self.fullname=fullname
        self.address=address
        self.phone=phone
        self.password=password

    @property
    def username(self):
        return self.__username

    @property
    def fullname(self):
        return self.__fullname

    @property
    def address(self):
        return self.__address

    @property
    def phone(self):
        return self.__phone

    @property
    def password(self):
        return self.__password

    @username.setter
    def username(self , value):
        try:
            assert value.isalnum() is True
        except AssertionError:
            print('***your username must contain alphabet and number, spaces are not acceptable***')
            logger.error('user tried entering invalid info for username')
        self.__username =value

    @fullname.setter
    def fullname(self, value):
        try:
            assert all(x.isalpha() or x.isspace() for x in value) is True
        except AssertionError:
            print('***please use alphabet for your name***')
            logger.error('user tried entering invalid info for name')
        self.__fullname=value

    @address.setter
    def address(self, value):
        self.__address=value

    @phone.setter
    def phone(self, value):
        try:
            assert value.isdigit() is True
        except AssertionError:
            print('***please use numbers for phone number***')
            logger.error('user tried entering invalid info for phone number')
        self.__phone=value

    @password.setter
    def password(self, value):
        try:
            assert value.isalnum() is True
        except AssertionError:
            print('your password must contain alphabet and numbers')
            logger.error('user tried entering invalid info for password')
        self.__password=value

    def write_users_info(self, info_file):
        """
        this method writes user's info into a json file
        as a nested dict
        """
        with open(info_file, 'r') as users_info:
            data=json.load(users_info)
            info_dict={'username':f'{self.username}',
            'full_name':f'{self.fullname}',
            'password':f'{self.password}',
            'address':f'{self.address}',
            'phone_number':f'{self.phone}'}
            data[f'{self.username}']=info_dict
            info=json.dumps(data,  indent=4)
            with open(info_file, 'w') as new_user_info:
                new_user_info.write(info)
    
    def read_users_info(self, info_file):
        """
        this method read users info by their user name from
        json file which contains user's info and show their info
        """
        with open(info_file, 'r+') as file:
            info_dict=json.load(file)
            if self.username in info_dict.keys():
                print(f'username: {info_dict[self.username]["username"]}')
                print(f'full name: {info_dict[self.username]["full_name"]}')
                print(f'address: {info_dict[self.username]["address"]}')
                print(f'phone number: {info_dict[self.username]["phone_number"]}')

    def edit_user_info(self, info_file):
        """
        this method edit users info, by finding the related dict
        delete it and writing new dict in file by new info from user
        """
        with open(info_file, 'r+') as users_info:
            data = json.load(users_info)
            del data[self.username]
            info_dict = {'username':f'{self.username}',
            'full_name':f'{self.fullname}',
            'password':f'{self.password}',
            'address':f'{self.address}',
            'phone_number':f'{self.phone}'}
            data[f'{self.username}']=info_dict
            info = json.dumps(data,  indent=4)
            with open(info_file, 'w') as new_user_info:
                new_user_info.write(info)

    def get_users_info(info_file, username) :
        """
        this method read users info from file and return their info
        """
        with open(info_file, 'r+') as file:
            info_dict = json.load(file)
            if username in info_dict.keys():
                full_name = info_dict[username]["full_name"]
                address = info_dict[username]["address"]
                phone_number = info_dict[username]["phone_number"]
                password = info_dict[username]["password"]
        return password, full_name, address, phone_number

    @staticmethod
    def check_user_password(info_file, username, password):
        """
        this method checks if username that user is trying to enter
        is available in our info file or not and if it was available 
        it checks if password match with our password written in file
        then user can login 
        """
        logged_in=False
        with open(info_file, 'r+') as file:
            info_dict=json.load(file)
            try:
                assert username in info_dict.keys()
            except AssertionError:
                print('this username does not exist')
                logger.error('user tried entering invalid username')
            else:
                if password != info_dict[username]["password"]:
                    print('wrong password!')
                    logger.error(f'{username} entered wrong password')
                else:
                    logged_in=True
        return logged_in

    def __str__(self) -> str:
        return self.username

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}:{self.username}'
