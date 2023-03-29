import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


from api import PetFriends
import os
from settings import valid_email, valid_password
from settings import notvalid_email, notvalid_password

pf = PetFriends()

def test_get_api_key_for_novalid_email(email=notvalid_email, password=valid_password):
    status, result = pf.get_api_key(email,password)
    assert status == 200
    assert 'key' in result

def test_get_api_key_for_novalid_password(email=valid_email, password=notvalid_password):
    status, result = pf.get_api_key(email,password)
    assert status == 200
    assert 'key' in result

def test_post_add_new_pet_without_name(animal_type='dog', age='3', pet_photo='images/Rex.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet(auth_key, os.name, animal_type, age, pet_photo)
    assert status == 200
    assert result['animal_type'] == animal_type


def test_post_add_new_pet_big_age(name='Bella', animal_type='bird', age='54544897984561211516584845', pet_photo='images/Bella.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_delete_pet_with_wrong_id():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][5]['id']
    status, _ = pf.delete_pet(auth_key,pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    assert status == 200
    assert pet_id not in my_pets.values()

def test_delete_pet_with_last_id():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][-1]['id']
    status, _ = pf.delete_pet(auth_key,pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    assert status == 200
    assert pet_id not in my_pets.values()

def test_put_update_pet_without_age(name='Banty', animal_type='dog'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) > 0:
        status, result = pf.put_update_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age=None)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception('There is no my pets')

def test_put_update_pet_wrong_auth_key(name='Banty', animal_type='dog', age=6):
    _, auth_key = pf.get_api_key(valid_email, notvalid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) > 0:
        status, result = pf.put_update_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception('There is no my pets')


def test_add_new_pet_without_text_field(name='', animal_type='', age='', pet_photo='images/Vasya.jpg'):

    #Получаем полный путь к файлу с изображением и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    #Запрашиваем ключ API и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    #Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    #Сверяем ожидаемый и фактический результат
    assert status == 200
    assert result['name'] == name
    assert result['pet_photo'] is not ''

def test_add_new_empty_pet(name='', animal_type='', age=''):

    #Запрашиваем ключ API и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    #Добавляем питомца
    status, result = pf.add_new_pet_wo_photo(auth_key, name, animal_type, age)

    #Сверяем ожидаемый и фактический результат
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age
