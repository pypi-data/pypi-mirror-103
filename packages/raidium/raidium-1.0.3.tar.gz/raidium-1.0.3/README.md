<h1 align="center">Raidium</h1>

<h3>Модуль для Накрутки Прослушиваний в Вашем Альбоме в Социальной Сети ВКонтакте<h3>

<h4>1. Установите <a href="https://chromedriver.chromium.org/downloads">chromedriver.exe</a> Вашей версии Google Chrome<h3>
<h4>2. Перетащите <a href="https://chromedriver.chromium.org/downloads">chromedriver.exe</a> в C:\Users\User\AppData\Local\Google\Chrome<h4>
<h4>3. Если нет папки, то создай её<h4>

<h3>Простой пример кода с использованием библиотеки "Raidium"<h3>

```python
import vk-listener

listener.init('hide')

listener.authorization('Логин', 'Пароль')

if(listener.check()):
	print('Авторизация прошла успешно!')
else:
	print('Ошибка авторизации!')

listener.loop('Ссылка на Ваш альбом', 15)
```
