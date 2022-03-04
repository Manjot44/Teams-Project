import pytest
import src.auth
from src.other import clear_v1
from src.error import InputError

@pytest.fixture
def register_three_users():
    clear_v1()
    new_id = []
    
    returned = src.auth.auth_register_v1("aBc123._%+-@aBc123.-.Co", "123456", "A", "A")
    new_id.append(returned)

    returned = src.auth.auth_register_v1(".@..Ml", "a>?:1#", 
    "1234567890!@#$%^&*()<>?:|_+PqwertyuiPMhsDFtaVclikg", "1234567890!@#$%^&*()<>?:|_+PqwertyuiPMhsDFtaVclikg")
    new_id.append(returned)

    returned = src.auth.auth_register_v1("abc@gmail.com", "thisIsPass13./", "Jerry", "Lin")
    new_id.append(returned)

    return new_id