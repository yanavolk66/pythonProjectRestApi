from api import PetFriends
from settings import valid_email, valid_password


pf = PetFriends()

def test_get_api_key_for_valid_users (email=valid_email, password=valid_password):
   status, result = pf.get_api_key(email, password)
   assert status == 200
   assert 'key' in result

def test_get_all_pets_with_valid_key (filter=''):
   _, auth_key = pf.get_api_key(valid_email, valid_password)
   status, result = pf.get_list_of_pets(auth_key, filter)
   assert status == 200
   assert len(result['pets']) > 0


def test_09_add_new_pet_without_text_field(name='', animal_type='', age='', pet_photo='images/Relax.jpg'):
   '''Тест-09 Добавление нового питомца с фотографией без заполнения текстовых полей'''

   # Получаем полный путь к файлу с изображением и сохраняем в переменную pet_photo
   pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

   # Запрашиваем ключ API и сохраняем в переменную auth_key
   _, auth_key = pf.get_api_key(valid_email, valid_password)

   # Добавляем питомца
   status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

   # Сверяем ожидаемый и фактический результат
   assert status == 200
   assert result['name'] == name
   assert result['pet_photo'] is not ''