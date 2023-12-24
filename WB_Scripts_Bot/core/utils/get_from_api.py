import requests as requests

API_URL = "https://127.0.0.1/api-bot/"


def get_categories(parent=0):
    response = requests.get(API_URL + f"get-category/?parent={parent}", verify=False)
    return response.json()


def get_posts(category):
    response = requests.get(API_URL + f"get-category-posts/?category_posts={category}", verify=False)
    return response.json()


def get_scripts(post):
    response = requests.get(API_URL + f"get-post-scripts/?post_id={post}", verify=False)
    return response.json()


def get_script(script):
    response = requests.get(API_URL + f"get-script/?script_id={script}", verify=False)
    return response.json()


def check_user(telegram_id):
    response = requests.get(API_URL + f"register-user/?telegram_id={telegram_id}", verify=False)
    if response.status_code == 200:
        return True
    else:
        return False


def register_user(username, telegram_id):
    response = requests.post(API_URL + f"register-user/",
                             data={"username": username,
                                   "telegram_id": telegram_id}, verify=False)
    return response.json()


def reset_password(telegram_id):
    response = requests.get(API_URL + f"reset-password/?telegram_id={telegram_id}", verify=False)
    return response.json()
