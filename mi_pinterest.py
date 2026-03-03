# pip3 install py3-pinterest
from py3pin.Pinterest import Pinterest

#Create new instance of the API
pinterest = Pinterest(email='your-email', 
                      password='your-password', 
                      username='your-username',
                      cred_root='cache')


def get_user_profile():
    # retorna um dicionário com os dados:
    profile = pinterest.get_user_overview()
    # pega dados específicos desse dicionário:
    boards = profile['board_count']
    pins = profile['pin_count']
    followers = profile['follower_count']
    following = profile['following_count']
    data_pin = profile['last_pin_save_time']
    return [ boards, pins, followers, following, data_pin ]

def get_boards():
    # pega dados de todos os boards
    boards = pinterest.boards_all()
    # pega nome e seguidores de cada board
    for i in range(len(boards)):
        print( boards[i]['name'], boards[i]['follower_count'] )

def get_website_pinnable_images():
    # endpoint que pega todas as imagens de um site
    return pinterest.get_pinnable_images(url='some-url')

def get_pin_comments(pin_id=''):
    return pinterest.get_comments(pin_id=pin_id)


if __name__ == "__main__":
    print(get_boards())
