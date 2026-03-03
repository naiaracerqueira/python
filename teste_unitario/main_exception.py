import requests


def len_joke():
    joke = get_joke()
    return len(joke)

def get_joke():
    url = 'https://api.chucknorris.io/jokes/random'

    try:
        response = requests.get(url, timeout=30)
    except requests.exceptions.Timeout:
        return 'No jokes'
    except requests.exceptions.ConnectionError:
        pass
    else:
        if response.status_code == 200:
            joke = response.json()['value']
        else:
            joke = 'No jokes'
    
    return joke


if __name__ == '__main__':
    print(len_joke())