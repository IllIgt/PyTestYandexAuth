import pytest
import requests as rq

url_auth = 'https://passport.yandex.ru/passport?mode=auth'
url_main = 'https://yandex.ru'
url_unauth ='https://passport.yandex.ru/passport?mode=logout&uid=539596544'
auth_data = 'login=test.testovishev&passwd=123459876'


@pytest.fixture(scope = 'module')
#Setup создание сессии
def setup_module(request):
    print("Отличный фикстурный setup")
    session = rq.Session()
    #Teardown разлогинвается в конце тест-кейса, сессия сбрасывается сама
    def teardown_module():
        print("Отличный фикстурный teardown")
        cookie = session.cookies.get_dict()
        s_resp = session.get(url_unauth + '&yu=' + cookie['yandexuid'])
    request.addfinalizer(teardown_module)
    return session

#Превращаем запрос в строку
def resp_to_string(session):
    s_resp = session.get(url_main)
    rts = str(s_resp.text)
    return rts

#Проверка на вхождение
def test_yandex_page(setup_module):
    print ('тест соответствия на своем месте')
    rts = resp_to_string(setup_module)
    assert "<title>Яндекс — поиск №1 в России</title>" in rts

#авторизуемся, проверяем изменилась ли форма логин/пароль
def test_yandex_auth(setup_module):
    print('тест авторизации на своем месте')
    setup_module.post(url_auth,data=auth_data)
    rts = resp_to_string(setup_module)
    assert'test.testovishev' in rts and 'Выйти' in rts




