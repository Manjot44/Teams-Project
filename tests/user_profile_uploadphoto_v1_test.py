import requests
import src.config
import os.path

def test_correct_output():
    requests.delete(f"{src.config.url}/clear/v1")

    response = requests.post(f"{src.config.url}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    assert response.status_code == 200 
    user1 = response.json()

    response2 = requests.post(f"{src.config.url}/user/profile/uploadphoto/v1", json = {"token": user1["token"], "img_url": "http://cdn.mos.cms.futurecdn.net/iC7HBvohbJqExqvbKcV3pP.jpg", "x_start": 100, "y_start": 100, "x_end": 200, "y_end": 200})
    # assert response2.status_code == 200
    # assert user1['profile_img_url'] == f'src/static/profile_pic_0.jpg'
    assert os.path.isfile("src/static/profile_pic_0.jpg") is True

def test_invalid_token():
    requests.delete(f"{src.config.url}/clear/v1")

    response = requests.post(f"{src.config.url}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    assert response.status_code == 200 

    response2 = requests.post(f"{src.config.url}/user/profile/uploadphoto/v1", json = {"token": "invalid token", "img_url": "http://cdn.mos.cms.futurecdn.net/iC7HBvohbJqExqvbKcV3pP.jpg", "x_start": 100, "y_start": 100, "x_end": 200, "y_end": 200})
    assert response2.status_code == 403   
 

def test_invalid_url():
    requests.delete(f"{src.config.url}/clear/v1")   

    response = requests.post(f"{src.config.url}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    assert response.status_code == 200 
    user1 = response.json()

    response2 = requests.post(f"{src.config.url}/user/profile/uploadphoto/v1", json = {"token": user1["token"], "img_url": 'http://www.sredtrfjgkyjhkgkyftjdrsher.jpg/', "x_start": 100, "y_start": 100, "x_end": 200, "y_end": 200})
    assert response2.status_code == 400


def test_invalid_dimensions_negative():
    requests.delete(f"{src.config.url}/clear/v1")

    response = requests.post(f"{src.config.url}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    assert response.status_code == 200 
    user1 = response.json()

    response2 = requests.post(f"{src.config.url}/user/profile/uploadphoto/v1", json = {"token": user1["token"], "img_url": "http://cdn.mos.cms.futurecdn.net/iC7HBvohbJqExqvbKcV3pP.jpg", "x_start": -10, "y_start": -10, "x_end": -20, "y_end": -20})
    assert response2.status_code == 400 


def test_invalid_dimensions_start_greaterthan_end():
    requests.delete(f"{src.config.url}/clear/v1")

    response = requests.post(f"{src.config.url}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    assert response.status_code == 200 
    user1 = response.json()

    response2 = requests.post(f"{src.config.url}/user/profile/uploadphoto/v1", json = {"token": user1["token"], "img_url": "http://cdn.mos.cms.futurecdn.net/iC7HBvohbJqExqvbKcV3pP.jpg", "x_start": 500, "y_start": 500, "x_end": 300, "y_end": 300})
    assert response2.status_code == 400 


def test_invalid_dimensions_outofbounds():
    requests.delete(f"{src.config.url}/clear/v1")

    response = requests.post(f"{src.config.url}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    assert response.status_code == 200 
    user1 = response.json()

    response2 = requests.post(f"{src.config.url}/user/profile/uploadphoto/v1", json = {"token": user1["token"], "img_url": "http://cdn.mos.cms.futurecdn.net/iC7HBvohbJqExqvbKcV3pP.jpg", "x_start": 5000, "y_start": 5000, "x_end": 6000, "y_end": 6000})
    assert response2.status_code == 400 
    

def test_not_jpg():
    requests.delete(f"{src.config.url}/clear/v1")

    response = requests.post(f"{src.config.url}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    assert response.status_code == 200 
    user1 = response.json()

    response2 = requests.post(f"{src.config.url}/user/profile/uploadphoto/v1", json = {"token": user1["token"], "img_url": "http://www.cse.unsw.edu.au/~richardb/index_files/RichardBuckland-200.png", "x_start": 50, "y_start": 50, "x_end": 100, "y_end": 100})
    assert response2.status_code == 400 
