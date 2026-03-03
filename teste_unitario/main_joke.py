import requests


def len_joke():
    joke = get_joke()
    return len(joke)

def get_joke():
    url = 'https://api.chucknorris.io/jokes/random'

    response = requests.get(url)

    if response.status_code == 200:
        joke = response.json()['value']
    else:
        joke = 'No jokes'
    
    return joke


if __name__ == '__main__':
    print(len_joke())
