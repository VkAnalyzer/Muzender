import pickle
import sys

tg_token_path = 'data/token.pkl'
vk_secret_path = 'data/secret.pkl'

greetings = 'Welcome to Muzender music recommender bot setup!'
old_python_warning = 'It seems you are a bit old-fashioned and still use Python 2, ' \
                     'make sure you use quotes around your inputs.'
vk_intro = '\nFirst let`s setup vk.com accont for parser.'
tg_intro = '\nNow enter Telegram bot credentials. Talk to @BotFather.'
success = '\nGreat, now download model.pkl manually and place it in ./data/ folder:'
model_link = 'https://drive.google.com/open?id=1Jkvhuo5ULFl8L4jkwc_1XjtFkEaosyHm'


if __name__ == '__main__':
    print(greetings)

    if sys.version_info[0] < 3:
        print(old_python_warning)

    print(vk_intro)
    vk_login = input('Login: ')
    vk_password = input('Password: ')

    with open(vk_secret_path, 'wb') as f:
        pickle.dump({'login': vk_login, 'password': vk_password}, f)

    print(tg_intro)
    tg_token = input('Token: ')

    with open(tg_token_path, 'wb') as f:
        pickle.dump(tg_token, f)

    print(success)
    print(model_link)
