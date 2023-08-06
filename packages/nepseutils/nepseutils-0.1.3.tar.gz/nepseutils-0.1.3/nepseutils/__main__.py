import sys
import json
from meroshare import MeroShare
import pickle


def modify_config():
    pass

def add_new_account():
    dpid = input("DPID: ")
    username = input("Username: ")
    password = input("Password: ")
    pin = input("PIN: ")

    try:
        with open("data.json", "r") as config_file:
            configs = json.load(config_file)
    except FileNotFoundError:
        configs = None
    except json.JSONDecodeError:
        raise Exception("Invalid config file!")

    if not configs:
        configs = {"accounts": []}

    account = {
        "dpid": dpid,
        "username": username,
        "password": password,
        "pin": pin,
    }

    configs["accounts"].append(account)

    with open("data.json", "w") as config_file:
        json.dump(configs, config_file, indent=4)


if __name__ == "__main__":
    if sys.argv[1] == "add":
        add_new_account()
    else if sys.argv[1] == "config":
        modify_config()
