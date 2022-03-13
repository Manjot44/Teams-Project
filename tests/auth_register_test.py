import src.auth
import src.channels
import src.channel
import pytest 
from src.other import clear_v1
from src.error import InputError

def test_authreg_valid(register_three_users):
    for id in register_three_users:
        assert isinstance(id, int)
    
    assert register_three_users[0] != register_three_users[1]
    assert register_three_users[0] != register_three_users[2] 
    assert register_three_users[1] != register_three_users[2]

def test_email_missing_element():
    clear_v1()
    with pytest.raises(InputError):
        src.auth.auth_register_v1("abcgmail.com", "thisIsPass13./", "Jerry", "Lin")    
    with pytest.raises(InputError):
        src.auth.auth_register_v1("abc@gmailcom", "thisIsPass13./", "Jerry", "Lin")      
    with pytest.raises(InputError):
        src.auth.auth_register_v1("abc@gmail.M", "thisIsPass13./", "Jerry", "Lin")       

def test_email_repeat():
    clear_v1()
    src.auth.auth_register_v1("abc@gmail.com", "thisIsPass13./", "Jerry", "Lin")   
    src.auth.auth_register_v1("aBc123._%+-@aBc123.-.Co", "123456", "A", "A")
    with pytest.raises(InputError):  
        src.auth.auth_register_v1("abc@gmail.com", "thisIsPass13./", "Jerry", "Lin")    

def test_email_invalid_char():
    clear_v1()
    with pytest.raises(InputError):
        src.auth.auth_register_v1("abc%^@gmail.com", "thisIsPass13./", "Jerry", "Lin")   
    with pytest.raises(InputError):
        src.auth.auth_register_v1("abc@gmail.+.com", "thisIsPass13./", "Jerry", "Lin")   
    with pytest.raises(InputError):
        src.auth.auth_register_v1("abc@gmail.co2", "thisIsPass13./", "Jerry", "Lin")     
    with pytest.raises(InputError):
        src.auth.auth_register_v1("abc@gmail.co.*", "thisIsPass13./", "Jerry", "Lin")    

def test_email_empty_section():
    clear_v1()
    with pytest.raises(InputError):
        src.auth.auth_register_v1("@gmail.com", "thisIsPass13./", "Jerry", "Lin")        
    with pytest.raises(InputError):
        src.auth.auth_register_v1("abc@.com", "thisIsPass13./", "Jerry", "Lin")          
    with pytest.raises(InputError):
        src.auth.auth_register_v1("abc@gmail.", "thisIsPass13./", "Jerry", "Lin")        
    with pytest.raises(InputError):
        src.auth.auth_register_v1("", "thisIsPass13./", "Jerry", "Lin")                 

def test_password_invalid():
    clear_v1()
    with pytest.raises(InputError):
        src.auth.auth_register_v1("abc@gmail.com", "1>;[g", "Jerry", "Lin")             
    with pytest.raises(InputError):
        src.auth.auth_register_v1("abc@gmail.com", "", "Jerry", "Lin")       
            
def test_names_empty():
    clear_v1()
    with pytest.raises(InputError):
        src.auth.auth_register_v1("abc@gmail.com", "thisIsPass13./", "Jerry", "")        
    with pytest.raises(InputError):
        src.auth.auth_register_v1("abc@gmail.com", "thisIsPass13./", "", "Lin")          

def test_names_long():
    clear_v1()
    with pytest.raises(InputError):
        src.auth.auth_register_v1("abc@gmail.com", "thisIsPass13./",                     
        "1234567890!@#$%^&*()<>?:|_+PqwertyuiPMhsDFtaVclikg8", "Lin")                    
    with pytest.raises(InputError):
        src.auth.auth_register_v1("abc@gmail.com", "thisIsPass13./",                     
        "Jerry", "1234567890!@#$%^&*()<>?:|_+PqwertyuiPMhsDFtaVclikg8")                  




def test_handle_normal():
    clear_v1()
    user_id = src.auth.auth_register_v1("jerrylin@gmail.com", "123456", "Jerry", "Lin")["auth_user_id"]
    channel_id = src.channels.channels_create_v1(user_id, "new channel", True)["channel_id"]
    generated_handle = src.channel.channel_details_v1(user_id, channel_id)["all_members"][0]["handle_str"]

    expected_handle = "jerrylin"
    assert generated_handle == expected_handle

def test_border_handle_long():
    clear_v1()
    user_id = src.auth.auth_register_v1("jerrylin@gmail.com", "123456", "Iamthegreatest", "JerryL")["auth_user_id"]
    channel_id = src.channels.channels_create_v1(user_id, "new channel", True)["channel_id"]
    generated_handle = src.channel.channel_details_v1(user_id, channel_id)["all_members"][0]["handle_str"]

    expected_handle = "iamthegreatestjerryl"
    assert generated_handle == expected_handle

    clear_v1()
    user_id = src.auth.auth_register_v1("jerrylin@gmail.com", "123456", "Iamthegreatest", "JerryLi")["auth_user_id"]
    channel_id = src.channels.channels_create_v1(user_id, "new channel", True)["channel_id"]
    generated_handle = src.channel.channel_details_v1(user_id, channel_id)["all_members"][0]["handle_str"]

    assert generated_handle == expected_handle

def test_handle_repeat():
    clear_v1()
    src.auth.auth_register_v1("jerrylin@gmail.com", "123456", "Jerry", "Lin")
    user_id = src.auth.auth_register_v1("jerry@gmail.com", "123456", "Jerry", "Lin")["auth_user_id"]
    channel_id = src.channels.channels_create_v1(user_id, "new channel", True)["channel_id"]
    generated_handle = src.channel.channel_details_v1(user_id, channel_id)["all_members"][0]["handle_str"]

    expected_handle = "jerrylin0"
    assert generated_handle == expected_handle

def test_long_handle_repeat():
    clear_v1()
    src.auth.auth_register_v1("jerrylin@gmail.com", "123456", "Iamthegreatest", "JerryLi")
    user_id = src.auth.auth_register_v1("jerry@gmail.com", "123456", "Iamthegreatest", "JerryLi")["auth_user_id"]
    channel_id = src.channels.channels_create_v1(user_id, "new channel", True)["channel_id"]
    generated_handle = src.channel.channel_details_v1(user_id, channel_id)["all_members"][0]["handle_str"]

    expected_handle = "iamthegreatestjerryl0"
    assert generated_handle == expected_handle
