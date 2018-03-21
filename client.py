import requests

#print(requests.get("http://127.0.0.1:5000/").content)
def login():
    id = 'walter2'
    password ='123456'

    setup = "[[0, 0, 'k', 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 'k', 0, 0, 0, 0, 0, 0, 0], ['c', 'c', 's', 's', 0, 0, 0, 's', 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 's', 0, 0, 's', 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]"

    # id = ''
    # password =''

    login_request = requests.post('http://127.0.0.1:5000/login', data = {'username':id, 'password':password})

    r = requests.get('http://127.0.0.1:5000/get_setup', cookies=login_request.cookies)

    r = requests.post('http://127.0.0.1:5000/update_setup', data = {'setup':setup}, cookies=login_request.cookies)
    r = requests.get('http://127.0.0.1:5000/find_game', cookies=login_request.cookies)
    #
    #
    r = requests.get('http://127.0.0.1:5000/check_game_ready', cookies=login_request.cookies)

    print(r.content)


if __name__ == '__main__':

    login()
