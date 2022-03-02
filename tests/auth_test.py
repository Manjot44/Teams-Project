import src.auth
import pytest 
from src.other import clear_v1
from src.error import InputError

def test_authreg_valid():
    clear_v1()
    new_id = []
    
    returned = src.auth.auth_register_v1("aBc123._%+-@aBc123.-.Co", "123456", "A", "A")
    assert returned is int not in new_id
    new_id.append(returned)

    returned = src.auth.auth_register_v1(".@..Ml", "a>?:1#", 
    "1234567890!@#$%^&*()<>?:|_+PqwertyuiPMhsDFtaVclikg", "1234567890!@#$%^&*()<>?:|_+PqwertyuiPMhsDFtaVclikg")
    assert returned is int not in new_id
    new_id.append(returned)

    returned = src.auth.auth_register_v1("abc@gmail.com", "thisIsPass13./", "Jerry", "Lin")
    assert returned is int not in new_id

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
    clearv1()
    with pytest.raises(InputError):
        assert src.auth.auth_register_v1("abc@gmail.com", "1>;[g", "Jerry", "Lin")              # 5 letter password
        assert src.auth.auth_register_v1("abc@gmail.com", "", "Jerry", "Lin")                   # empty password

def test_authreg_names():
    clearv1()
    with pytest.raises(ImportError):
        assert src.auth.auth_register_v1("abc@gmail.com", "thisIsPass13./", "Jerry", "")        # 
        assert src.auth.auth_register_v1("abc@gmail.com", "thisIsPass13./", "", "Lin")          # empty names
        
        assert src.auth.auth_register_v1("abc@gmail.com", "thisIsPass13./",                     #
        "1234567890!@#$%^&*()<>?:|_+PqwertyuiPMhsDFtaVclikg8", "Lin")                           #
        assert src.auth.auth_register_v1("abc@gmail.com", "thisIsPass13./",                     #
        "Jerry", "1234567890!@#$%^&*()<>?:|_+PqwertyuiPMhsDFtaVclikg8")                         # long names
