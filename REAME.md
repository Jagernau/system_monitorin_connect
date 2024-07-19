# Программа для сбора данных с систем мониторинга

## Установка
1. Скопировать этот репозиторий в любой место: `git clone https://github.com/Jagernau/system_monitorin_connect`
2. Перейти в директорию `system_monitorin_connect`
3. Создать виртуальное окружение: `python3.10 -m virtualenv env`
4. Активировать виртуальное окружение: `source venv/bin/activate`
5. Установить зависимости: `pip install -r requirements.txt`
6. Создать файл .env: `touch .env` с конфигурацией:
    * Записать в фай .env следующие переменные
    * На данный момент реализованны:
    ```
    GLONASS_LOGIN=логин пользователя глонасс
    GLONASS_PASSWORD=пароль пользователя глонасс
    GLONASS_BASED_ADRESS=адрес сайта глонасс

    SCOUT_TREEHUNDRED_LOGIN=логин пользователя scout_365
    SCOUT_TREEHUNDRED_PASSWORD=пароль пользователя scout_365
    SCOUT_TREEHUNDRED_BASED_ADRESS=адрес сайта scout_365
    SCOUT_TREEHUNDRED_BASE_TOKEN=токен пользователя scout_365


    GELIOS_BASED_ADRESS=адрес сайта гелиос
    GELIOS_LOGIN=логин пользователя гелиос
    GELIOS_PASSWORD=пароль пользователя гелиос
    ```
