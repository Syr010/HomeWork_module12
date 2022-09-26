from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()

def test_get_api_key_for_invalid_user(email=invalid_email, password=valid_password):
    """Тест с невалидным email, проверяем что запрос апи ключа возвращает статус 403"""
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_get_api_key_for_invalid_user(email=valid_email, password=invalid_password):
    """Тест с невалидным паролем, проверяем что запрос апи ключа возвращает статус 403"""
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_get_all_pets_with_valid_filter(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
       Для этого сначала получаем апи ключ и сохраняем в переменную auth_key. Далее используя этот ключ
       запрашиваем список всех питомцев с параметром фильтра my_pets"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets_with_valid_filter(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_get_all_pets_with_invalid_filter(filter=''):
    """ Проверяем что запрос не проходит с неверным параметром фильтра и возвращает статус код 500"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets_with_invalid_filter(auth_key, filter)
    assert status == 500


def test_add_new_pet_with_invalid_name(name="машамашамашамашмашамашамашамашамашмаша"
                                            "машамашамашамашмашамашамашамашамашмаша"
                                            "машамашамашамашмашамашамашамашамашмаша"
                                            "машамашамашамашмашамашамашамашамашмаша"
                                            "машамашамашамашмашамашамашамашамашмаша"
                                            "машамашамашамашмашамашамашамашамашмаша"
                                            "машамашамашамашмашамашамашамашамашмаша"
                                            "машамашамашамашмашамашамашамашамашмаша"
                                            "машамашамашамашмашамашамашамашамашмаша"
                                            "машамашамашамашмашамашамашамашамашмаша"
                                            "машамашамашамашмашамашамашамашамашмаша"
                                            "машамашамашамашмашамашамашамашамашмаша"
                                            "машамашамашамашмашамашамашамашамашмаша"
                                            "машамашамашамашмашамашамашамашамашмаша"
                                            "машамашамашамашмашамашамашамашамашмаша", animal_type='кошка',
                                     age='5', pet_photo='image/1.jpg'):
    """Проверяем возможность добавления питомца с некорректным именем"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_invalid_photo(name="LOL", animal_type='кошка',
                                     age='5', pet_photo='image/video.mp4'):
    """Проверяем возможность добавления питомца с невалидным форматом фото питомца"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_delete_not_my_pet():
    """Проверяем возможность удаления несуществующего питомца, тест проходит..
    видимо я делаю что-то неправильно, буду признательна за все Ваши замечания"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Батон", "котлета", "5", "image/2.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        pet_id = my_pets['Хлеб']['5346940359034']
        status, _ = pf.delete_pet(auth_key, pet_id)

        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        assert status == 200
        assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info_with_incorrect_age(name='Гусь', animal_type='птица', age='22 годов'):
    """Проверяем возможность обновления информации о питомце c невалидным значением
    параметра age"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_successful_update_self_pet_info_with_incorrect_animal_type(name="Вася", animal_type=78, age=22):
    """Проверяем возможность обновления информации о питомце c невалидным значением
    параметра animal_type"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

def test_successful_update_self_pet_info_with_incorrect_name(name=77, animal_type='журавль', age=22):
    """Проверяем возможность обновления информации о питомце c невалидным значением
    параметра name"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
    else:
        raise Exception("There is no my pets")