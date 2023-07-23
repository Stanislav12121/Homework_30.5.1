from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('c:\1\chromedriver.exe')
   # Переходим на страницу авторизации
   pytest.driver.set_window_size(1400, 1000)
   pytest.driver.get('http://petfriends.skillfactory.ru/login')

   yield

   pytest.driver.quit()

# Задание 30.3.1
def test_my_pets():
   # Вводим email
   pytest.driver.find_element(By.ID, 'email').send_keys('qqq@qqq.qqq')
   # Вводим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys('12345')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Нажимаем на ссылку "Мои питомцы"
   pytest.driver.find_element(By.XPATH, '//a[contains(text(), "Мои пит")]').click()
   # Проверяем, что мы оказались на странице пользователя
   assert pytest.driver.find_element(By.TAG_NAME, 'h2').text == "werty1234"

   # 1. Проверяем, что присутствуют все питомцы
   table = pytest.driver.find_element(By.XPATH, '//tbody')
   qty_t = 0
   for i in table.text:
      #В каждой строке таблицы есть символ '×', поэтому если посчитать сколько таких символов в таблице - мы узнаем количество питомцев
      if i == '×':
         qty_t += 1
   # В блоке с информацией о пользователе указано количество питомцев, нужно переменной присвоить эту цифру для последюущего сравнения
   user_stat = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='.col-sm-4 left']")))
   parts = user_stat.text.split(": ")
   qty = int(parts[1][0])
   #Проверяем, что кол-во питомцев, указанное в блоке пользователя и количество питомцев в таблице совпадает
   assert qty_t == qty

   # 2. Проверяем, что хотя бы у половины питомцев есть фото
   qty_jpg = 0
   for i in pytest.driver.find_elements(By.XPATH, '//tr/th[@scope="row"]'):
      if "jpeg" in i.get_attribute('innerHTML'):
         qty_jpg += 1
   assert qty_jpg >= qty // 2

   # 3. Проверяем что у всех питомцев есть имя, возраст и порода
   # Создаем список из значений в таблице
   list_table = table.text.split()
   #Создаем пустые списки имен, пород и возраста для дальнейшего заполнения
   names = []
   kind_anim = []
   age = []
   #Добавляем имена в соответствующий список
   for i in range(0, len(list_table), 4):
      names.append(list_table[i])
   # Добавляем породы в соответствующий список
   for i in range(1, len(list_table), 4):
      kind_anim.append(list_table[i])
   # Добавляем возраст в соответствующий список
   for i in range(2, len(list_table), 4):
      age.append(list_table[i])
   #Проверяем, что у всех питомцев есть имена, породы, возраст (qty_t - переменная, которой присвоено кол-во питомцев из таблицы)
   assert qty_t == len(names) and qty_t == len(kind_anim) and qty_t == len(age)

   #4. Проверяем, что у всех питомцев разные имена
   # Создаем пустой список, в который будут добавляться дубликаты имен
   duplicates = []
   for i in names:
      if names.count(i) > 1 and i not in duplicates:
         duplicates.append(i)
   # Поставить != если нужно проверить что есть дубликаты или ==, что дубликатов нет
   assert duplicates != ''

   #5. Проверяем, что нет повторяющихся питомцев
   uniq = 0
   dubl = 0
   while uniq < qty_t:
      for i in range(uniq + 1, qty_t):
         if names[uniq] == names[i] and kind_anim[uniq] == kind_anim[i] and age[uniq] == age[i]:
            dubl += 1
      uniq += 1
   #Поставить !=, если нужно проверить, что повторяющиеся питомцы есть или ==, что повторяющихся нет
   assert uniq != 0

#Задание 30.5.1
def test_my_pets_2():
   # Вводим email
   pytest.driver.find_element(By.ID, 'email').send_keys('qqq@qqq.qqq')
   # Вводим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys('12345')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   #Нажимаем на ссылку "Мои питомцы"
   pytest.driver.find_element(By.XPATH, '//a[contains(text(), "Мои пит")]').click()
   # Проверяем, что мы оказались на странице пользователя
   assert pytest.driver.find_element(By.TAG_NAME, 'h2').text == "werty1234"

   #Ожидаем, что на странице "Мои питомцы" страница называется "PetFriends: My Pets"
   title = WebDriverWait(pytest.driver, 10).until(EC.title_is("PetFriends: My Pets"))
   assert title == True

   #Ожидаем, что на странице "Мои питомцы" есть ссылка "Мои питомцы"
   my_pets = WebDriverWait(pytest.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Мои питомцы")))
   assert my_pets.text == "Мои питомцы"

   #Ожидаем, что на странице "Мои питомцы" имеется блок статистики пользователя
   user_stat = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='.col-sm-4 left']")))
   assert "Питомцев" and "Друзей" and "Сообщений" in user_stat.text

   # Ожидаем, что на странице "Мои питомцы" есть элемент "Все питомцы"
   pets = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Все питомцы")))
   assert pets.text == "Все питомцы"

   # Ожидаем, что на странице "Мои питомцы" есть таблица с питомцами
   table = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//table[@class='table table-hover']")))
   assert "Фото" and "Имя" and "Порода" and "Возраст" in table.text
   

def test_all_pets():
   # Вводим email
   pytest.driver.find_element(By.ID, 'email').send_keys('qqq@qqq.qqq')
   # Вводим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys('12345')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице
   assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
   pytest.driver.implicitly_wait(10)

   #Ожидаем что на странице "Все питомцы" есть заголовок PetFriends
   name = pytest.driver.find_element(By.XPATH, '//h1[@class="text-center"]')
   assert name.text == "PetFriends"

   # Ожидаем что на странице "Все питомцы" есть блок с карточками питомцев
   table = pytest.driver.find_element(By.XPATH, '//div[@class="card-deck"]')
   assert table.text != ''

   # Ожидаем что на странице "Все питомцы" у первого питомца есть фото (или указать номер другого питомца)
   pet_photo = pytest.driver.find_element(By.XPATH, '(//img[@class="card-img-top"])[1]')
   assert "jpeg" in pet_photo.get_attribute('src')

   # Ожидаем что на странице "Все питомцы" есть питомец по имени VbzVbz (или указать имя другого питомца)
   pet_VbzVbz = pytest.driver.find_element(By.XPATH, '//h5[@class="card-title" and contains(text(), "VbzVbz")]')
   assert pet_VbzVbz.text == 'VbzVbz'

   # Ожидаем что на странице "Все питомцы" у питомцев указан возраст
   pet_age = pytest.driver.find_element(By.XPATH, '//p[@class="card-text" and contains(text(), "лет") or contains(text(), "года")]')
   assert "лет" or "года" in pet_age.text

def test_my_pets_3():
   # Вводим email
   pytest.driver.find_element(By.ID, 'email').send_keys('qqq@qqq.qqq')

   # Вводим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys('12345')

   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

   # Нажимаем на ссылку перехода в раздел "Мои питомцы"
   pytest.driver.find_element(By.XPATH, '//a[@href="/my_pets"]').click()

   # Проверяем, что мы оказались на странице пользователя
   assert pytest.driver.find_element(By.TAG_NAME, 'h2').text == "werty1234"


   pytest.driver.implicitly_wait(10)
   # Ожидаем что на странице "Мои питомцы" у питомцев есть ячейка для фото
   for i in pytest.driver.find_elements(By.XPATH, '//tr/th[@scope="row"]'):
      assert i.get_attribute('src') != ''
   # Ожидаем что на странице "Мои питомцы" у питомцев есть имена
   for i in pytest.driver.find_elements(By.XPATH, '//tr/td[1]'):
      assert i.text != ''
   # Ожидаем что на странице "Мои питомцы" у питомцев указан возраст
   for i in pytest.driver.find_elements(By.XPATH, '//tr/td[3]'):
      assert i.text != ''

   #Эксперименты
   # Ожидаем что на странице "Мои питомцы" у питомцев имеются ячейки для фото
   for i in pytest.driver.find_elements(By.XPATH, '//img[@style="max-width: 100px; max-height: 100px;"]'):
      assert i.get_attribute('style') != ''

   # Ожидаем что на странице "Мои питомцы" есть питомец по имени Tuzik
   for i in pytest.driver.find_elements(By.XPATH, '//td[contains(text(), "Tuzik")]'):
      assert "Tuzik" in i.text

   # Ожидаем что на странице "Мои питомцы" у первого питомца есть элемент возраст
   for i in pytest.driver.find_elements(By.XPATH, '(//tr/td[3])[1]'):
      assert i.text != ''


   # Код из лекции юнита 30.3
   # images = pytest.driver.find_elements(By.XPATH, '//p[@class="card-text"]')
   # names = pytest.driver.find_elements(By.XPATH, '//h5[@class="card-title"]')
   # descriptions = pytest.driver.find_elements(By.XPATH, '//img[@class="card-img-top"]')
   #
   # for i in range(len(names)):
   #    assert images[i].get_attribute('src') != ''
   #    assert names[i].text != ''
   #    assert descriptions[i].text != ''
   #    assert ', ' in descriptions[i]
   #    parts = descriptions[i].text.split(", ")
   #    assert len(parts[0]) > 0
   #    assert len(parts[1]) > 0
