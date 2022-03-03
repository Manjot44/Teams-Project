import src.auth
import pytest 
from src.other import clear_v1
from src.error import InputError

@pytest.fixture
def test_authreg_valid():
    clear_v1()
    new_id = []
    
    returned = src.auth.auth_register_v1("aBc123._%+-@aBc123.-.Co", "123456", "A", "A")
    assert isinstance(returned, int) and returned not in new_id
    new_id.append(returned)

    returned = src.auth.auth_register_v1(".@..Ml", "a>?:1#", 
    "1234567890!@#$%^&*()<>?:|_+PqwertyuiPMhsDFtaVclikg", "1234567890!@#$%^&*()<>?:|_+PqwertyuiPMhsDFtaVclikg")
    assert isinstance(returned, int) and returned not in new_id
    new_id.append(returned)

    returned = src.auth.auth_register_v1("abc@gmail.com", "thisIsPass13./", "Jerry", "Lin")
    assert isinstance(returned, int) and returned not in new_id

    return new_id

def test_authreg_email():
    clear_v1()
    with pytest.raises(InputError):
        assert src.auth.auth_register_v1("abcgmail.com", "thisIsPass13./", "Jerry", "Lin")      # missing the @
        assert src.auth.auth_register_v1("abc@gmailcom", "thisIsPass13./", "Jerry", "Lin")      # missing the .

        assert src.auth.auth_register_v1("abc@gmail.M", "thisIsPass13./", "Jerry", "Lin")       # not >one characters to end
        
        assert src.auth.auth_register_v1("abc@gmail.com", "thisIsPass13./", "Jerry", "Lin")     #
        assert src.auth.auth_register_v1("abc@gmail.com", "thisIsPass13./", "Jerry", "Lin")     # repeated email

        assert src.auth.auth_register_v1("abc%^@gmail.com", "thisIsPass13./", "Jerry", "Lin")   # invalid character in first section
        assert src.auth.auth_register_v1("abc@gmail.+.com", "thisIsPass13./", "Jerry", "Lin")   # invalid character in second section
        assert src.auth.auth_register_v1("abc@gmail.co2", "thisIsPass13./", "Jerry", "Lin")     # invalid character in third section
        assert src.auth.auth_register_v1("abc@gmail.co.*", "thisIsPass13./", "Jerry", "Lin")    # invalid character in third section

        assert src.auth.auth_register_v1("@gmail.com", "thisIsPass13./", "Jerry", "Lin")        # empty first section
        assert src.auth.auth_register_v1("abc@.com", "thisIsPass13./", "Jerry", "Lin")          # empty second section
        assert src.auth.auth_register_v1("abc@gmail.", "thisIsPass13./", "Jerry", "Lin")        # empty third section
        assert src.auth.auth_register_v1("", "thisIsPass13./", "Jerry", "Lin")                  # empty email

def test_authreg_password():
    clear_v1()
    with pytest.raises(InputError):
        assert src.auth.auth_register_v1("abc@gmail.com", "1>;[g", "Jerry", "Lin")              # 5 letter password
        assert src.auth.auth_register_v1("abc@gmail.com", "", "Jerry", "Lin")                   # empty password

def test_authreg_names():
    clear_v1()
    with pytest.raises(InputError):
        assert src.auth.auth_register_v1("abc@gmail.com", "thisIsPass13./", "Jerry", "")        # 
        assert src.auth.auth_register_v1("abc@gmail.com", "thisIsPass13./", "", "Lin")          # empty names
        
        assert src.auth.auth_register_v1("abc@gmail.com", "thisIsPass13./",                     #
        "1234567890!@#$%^&*()<>?:|_+PqwertyuiPMhsDFtaVclikg8", "Lin")                           #
        assert src.auth.auth_register_v1("abc@gmail.com", "thisIsPass13./",                     #
        "Jerry", "1234567890!@#$%^&*()<>?:|_+PqwertyuiPMhsDFtaVclikg8")                         # long names



def test_authlog_valid(test_authreg_valid):
    assert src.auth.auth_login_v1("aBc123._%+-@aBc123.-.Co", "123456") == test_authreg_valid[0]
    assert src.auth.auth_login_v1(".@..Ml", "a>?:1#") == test_authreg_valid[1]

def test_authlog_missing(test_authreg_valid):
    with pytest.raises(InputError):
        assert src.auth.auth_login_v1("aBc12._%+-@aBc123.-.Co", "123456")                       # missing email
        assert src.auth.auth_login_v1("aBc123._%+-@aBc123.-.Co", "1234576")                     # missing password

def test_authlog_mixed(test_authreg_valid):
    with pytest.raises(InputError):
        assert src.auth.auth_login_v1("aBc123._%+-@aBc123.-.Co", "a>?:1#")                      # 
        assert src.auth.auth_login_v1(".@..Ml", "123456")                                       # different accounts password

def test_authlog_none():
    with pytest.raises(InputError):
        assert src.auth.auth_login_v1("anything@gmail.com", "password1$^")                      # no accounts stored