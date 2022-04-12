import requests
import src.config

def test_correct_output():
    requests.delete(f"{src.config.url}/clear/v1")