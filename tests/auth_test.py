import src.auth
import pytest 
from src.other import clear_v1
from src.error import InputError

def test_authreg_valid():
    clear_v1()
    new_id = []
    
    returned = src.auth.auth_register_v1("aBc123._%+-@aBc123.-.Co", "123456", "A", "A")
    assert isinstance(returned['auth_user_id'], int) and returned['auth_user_id'] not in new_id
    new_id.append(returned['auth_user_id'] )

    returned = src.auth.auth_register_v1(".@..Ml", "a>?:1#", 
    "1234567890!@#$%^&*()<>?:|_+PqwertyuiPMhsDFtaVclikg", "1234567890!@#$%^&*()<>?:|_+PqwertyuiPMhsDFtaVclikg")
    assert isinstance(returned['auth_user_id'] , int) and returned['auth_user_id']  not in new_id
    new_id.append(returned['auth_user_id'])

    returned = src.auth.auth_register_v1("abc@gmail.com", "thisIsPass13./", "Jerry", "Lin")
    assert isinstance(returned['auth_user_id'] , int) and returned['auth_user_id']  not in new_id

def test_authreg_email_miss1():
    clear_v1()
    with pytest.raises(InputError):
        src.auth.auth_register_v1("abcgmail.com", "thisIsPass13./", "Jerry", "Lin")      # missing the @

def test_authreg_email_miss2():
    clear_v1()
    with pytest.raises(InputError):
        src.auth.auth_register_v1("abc@gmailcom", "thisIsPass13./", "Jerry", "Lin")      # missing the .

def test_authreg_email_end():
    clear_v1()
    with pytest.raises(InputError):
        src.auth.auth_register_v1("abc@gmail.M", "thisIsPass13./", "Jerry", "Lin")       # not >1 characters to end

def test_authreg_email_repeat():
    clear_v1()
    with pytest.raises(InputError):  
        src.auth.auth_register_v1("abc@gmail.com", "thisIsPass13./", "Jerry", "Lin")     #
        src.auth.auth_register_v1("aBc123._%+-@aBc123.-.Co", "123456", "A", "A")
        src.auth.auth_register_v1("abc@gmail.com", "thisIsPass13./", "Jerry", "Lin")     # repeated email

def test_authreg_email_inv1():
    clear_v1()
    with pytest.raises(InputError):
        src.auth.auth_register_v1("abc%^@gmail.com", "thisIsPass13./", "Jerry", "Lin")   # invalid character in first section

def test_authreg_email_inv2():
    clear_v1()
    with pytest.raises(InputError):
        src.auth.auth_register_v1("abc@gmail.+.com", "thisIsPass13./", "Jerry", "Lin")   # invalid character in second section

def test_authreg_email_inv3():
    clear_v1()
    with pytest.raises(InputError):
        src.auth.auth_register_v1("abc@gmail.co2", "thisIsPass13./", "Jerry", "Lin")     # invalid character in third section

def test_authreg_email_inv4():
    clear_v1()
    with pytest.raises(InputError):
        src.auth.auth_register_v1("abc@gmail.co.*", "thisIsPass13./", "Jerry", "Lin")    # invalid character in third section

def test_authreg_email_empty1():
    clear_v1()
    with pytest.raises(InputError):
        src.auth.auth_register_v1("@gmail.com", "thisIsPass13./", "Jerry", "Lin")        # empty first section

def test_authreg_email_empty2():
    clear_v1()
    with pytest.raises(InputError):
        src.auth.auth_register_v1("abc@.com", "thisIsPass13./", "Jerry", "Lin")          # empty second section

def test_authreg_email_empty3():
    clear_v1()
    with pytest.raises(InputError):
        src.auth.auth_register_v1("abc@gmail.", "thisIsPass13./", "Jerry", "Lin")        # empty third section

def test_authreg_email_empty4():
    clear_v1()
    with pytest.raises(InputError):
        src.auth.auth_register_v1("", "thisIsPass13./", "Jerry", "Lin")                  # empty email

def test_authreg_password_less():
    clear_v1()
    with pytest.raises(InputError):
        src.auth.auth_register_v1("abc@gmail.com", "1>;[g", "Jerry", "Lin")              # 5 letter password

def test_authreg_password_empty():
    clear_v1()
    with pytest.raises(InputError):
        src.auth.auth_register_v1("abc@gmail.com", "", "Jerry", "Lin")                   # empty password

def test_authreg_names_empty1():
    clear_v1()
    with pytest.raises(InputError):
        src.auth.auth_register_v1("abc@gmail.com", "thisIsPass13./", "Jerry", "")        # empty first name

def test_authreg_names_empty2():
    clear_v1()
    with pytest.raises(InputError):
        src.auth.auth_register_v1("abc@gmail.com", "thisIsPass13./", "", "Lin")          # empty last name

def test_authreg_names_long1():
    clear_v1()
    with pytest.raises(InputError):
        src.auth.auth_register_v1("abc@gmail.com", "thisIsPass13./",                     #
        "1234567890!@#$%^&*()<>?:|_+PqwertyuiPMhsDFtaVclikg8", "Lin")                    # long first name
        
def test_authreg_names_long2():
    clear_v1()
    with pytest.raises(InputError):
        src.auth.auth_register_v1("abc@gmail.com", "thisIsPass13./",                     #
        "Jerry", "1234567890!@#$%^&*()<>?:|_+PqwertyuiPMhsDFtaVclikg8")                  # long last name



def test_authlog_valid(register_three_users):
    assert src.auth.auth_login_v1("aBc123._%+-@aBc123.-.Co", "123456")['auth_user_id'] == register_three_users[0]
    assert src.auth.auth_login_v1(".@..Ml", "a>?:1#")['auth_user_id'] == register_three_users[1]

def test_authlog_missing1(register_three_users):
    with pytest.raises(InputError):
        src.auth.auth_login_v1("aBc12._%+-@aBc123.-.Co", "123456")                       # missing email

def test_authlog_missing2(register_three_users):
    with pytest.raises(InputError):
        src.auth.auth_login_v1("aBc123._%+-@aBc123.-.Co", "1234576")                     # missing password

def test_authlog_empty1(register_three_users):
    with pytest.raises(InputError):
        src.auth.auth_login_v1("", "123456")                                             # empty email
        
def test_authlog_empty2(register_three_users):
    with pytest.raises(InputError):
        src.auth.auth_login_v1("aBc123._%+-@aBc123.-.Co", "")                            # empty password

def test_authlog_mixed1(register_three_users):
    with pytest.raises(InputError):
        src.auth.auth_login_v1("aBc123._%+-@aBc123.-.Co", "a>?:1#")                      # different accounts password

def test_authlog_mixed2(register_three_users):
    with pytest.raises(InputError):
        src.auth.auth_login_v1(".@..Ml", "123456")                                       # different accounts password

def test_authlog_none():
    clear_v1()
    with pytest.raises(InputError):
        src.auth.auth_login_v1("anything@gmail.com", "password1$^")                      # no accounts stored