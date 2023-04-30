def create_url(resource, id=None) -> str:
    url = "http://127.0.0.1:8000/api/"
    if resource == "user":
        url += f"user/{id}"
    elif resource == "users":
        url += "user/all"
    elif resource == "user_telegram":
        url += f"user/telegram/{id}"
    elif resource == "tasks":
        url += f"task/all"
    elif resource == "task":
        url += f"task/{id}"
    elif resource == "tasks_user":
        url += f"task/user/{id}"
    return url


def checking_for_success(good_answer: str, response) -> str:
    bad_answer = 'Упс что-то пошло не так. Попробуйте снова'
    if response["success"] == "OK":
        return good_answer
    return bad_answer


def get_id_from_string(string):
    i = 0
    el = string[i]
    id = ''
    while el != ':':
        id += el
        i += 1
        el = string[i]
    return int(id)
