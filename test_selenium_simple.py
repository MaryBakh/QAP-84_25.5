#!/usr/bin/python3
# -*- encoding=utf8 -*-

# You can find very simple example of the usage Selenium with PyTest in this file.
#
# More info about pytest-selenium:
#    https://pytest-selenium.readthedocs.io/en/latest/user_guide.html
#
# How to run:
#  1) Download geko driver for Chrome here:
#     https://chromedriver.storage.googleapis.com/index.html?path=2.43/
#  2) Install all requirements:
#     pip install -r requirements.txt
#  3) Run tests:
#     python3 -m pytest -v --driver Chrome --driver-path /tests/chrome test_selenium_simple.py
#

import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('D:\chromedriver_win32\chromedriver.exe')

   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends.skillfactory.ru/login')

   yield

   pytest.driver.quit()



def test_show_my_pets():
   pytest.driver.implicitly_wait(10)
   # Вводим email
   # Дополнительная проверка наличия элемента
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'email')))
   pytest.driver.find_element('id', 'email').send_keys('imy1540@ya.ru')

   # Вводим пароль
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'pass')))
   pytest.driver.find_element('id', 'pass').send_keys('shichihenge7')

   # Нажимаем на кнопку входа в аккаунт
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()


   # # Проверяем, что мы оказались на главной странице пользователя
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
   assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

   # Переход на личную страницу
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[@href="/my_pets"]')))
   pytest.driver.find_element(By.XPATH, '//a[@href="/my_pets"]').click()

   # Получение количества питомцев из статистики
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='.col-sm-4 left']")))
   stat_div = pytest.driver.find_element(By.XPATH, "//div[@class='.col-sm-4 left']")
   stat_list = stat_div.text.split("\n")
   stat_pets_list = stat_list[1].split(" ")
   amount_pets = int(stat_pets_list[1])

   # Получение количества питомцев на странице
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'tr')))
   pets_cards = pytest.driver.find_elements(By.TAG_NAME, 'tr')
   # Проверка присутствия всех питомцев
   assert len(pets_cards)-1 == amount_pets

   # Проверка наличия фото
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'img')))
   images = pytest.driver.find_elements(By.TAG_NAME, 'img')

   # Находим питомцев с непустым фото
   pets_with_img = 0
   for item in images:
      if (item.get_attribute('src') != '' and item.get_attribute('id') != 'pet_photo'):
         pets_with_img += 1

   # Проверяем - хотя бы у половины питомцев есть фото
   assert pets_with_img >= (len(pets_cards)-1)/2

   desc_list = []
   for i in range(1, len(pets_cards)):
      tmp_list = []
      for j in range(0, 4):
         if j == 0:
            # В самый первый проход находим сурс картинки
            str = "//*[@id='all_my_pets']/table[1]/tbody[1]/tr[{0}]/th[1]/img[1]".format(i)
            WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, str)))
            find = pytest.driver.find_element(By.XPATH, str)
            tmp_list.append(find.get_attribute('src'))
         else:
            # А в остальных случаях просто находим атрибуты
            str = "//*[@id='all_my_pets']/table[1]/tbody[1]/tr[{0}]/td[{1}]".format(i, j)
            WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, str)))
            find = pytest.driver.find_element(By.XPATH, str)
            tmp_list.append(find.text)
      desc_list.append(tmp_list)

   # Проверяем непустые имена
   for item in desc_list:
      name = item[1]
      assert name != ''

   # Проверяем непустой пол
   for item in desc_list:
      type = item[2]
      assert type != ''

   # Проверяем непустой возраст
   for item in desc_list:
      age = item[3]
      assert age != ''

   # Проверка, что у всех разные имена
   unique_name_list = []
   for item in desc_list:
      name = item[1]
      if name not in unique_name_list:
         unique_name_list.append(name)
   assert len(unique_name_list) == len(desc_list)

   # Проверка, что все разные
   unique_list = []
   for item in desc_list:
      # elem = item[0] + item[1] + item[2] + item[3]
      elem = item[1] + item[2] + item[3]
      if elem not in unique_list:
         unique_list.append(elem)
   assert len(unique_list) == len(desc_list)

   # # Проверка неявного ожидания
   # unknown_tag = pytest.driver.find_element(By.TAG_NAME, 'dfbdfbdbfdhdtggfj')
   # # Этого элемента не должно найтись
   # assert unknown_tag.text == 'dgfdfgdfg'


