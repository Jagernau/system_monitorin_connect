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

    FORT_LOGIN=логин пользователя Форт локал
    FORT_PASSWORD=пароль пользователя Форт локал
    FORT_BASED_ADRESS=адрес сайта Форт локал

    ERA_LOGIN=логин пользователя ЭРА
    ERA_PASSWORD=пароль пользователя ЭРА
    ERA_BASED_ADRESS=адрес сайта ЭРА
    ERA_PORT=порт для подключения к ЭРА

    SCOUT_LOCAL_LOGIN=логин пользователя СКАУТ локал
    SCOUT_LOCAL_PASSWORD=пароль пользователя СКАУТ локал
    SCOUT_LOCAL_BASED_ADRESS=адрес сайта СКАУТ локал
    SCOUT_LOCAL_PORT=порт для подключения СКАУТ локал

    WIALON_LOCAL_TOKEN=токен получен от wialon https://<адрес локала>/login.html?client_id=wialon&access_type=-1&activation_time=0&duration=0
    WIALON_LOCAL_BASED_ADRESS=адрес Wialon local
    WIALON_LOCAL_PORT=порт Wialon local


    WIALON_HOSTING_TOKEN=токен получен от wialon https://<адрес hoting>/login.html?client_id=wialon&access_type=-1&activation_time=0&duration=0
    WIALON_HOSTING_BASED_ADRESS=адрес Wialon hosting
    WIALON_HOSTING_PORT=порт Wialon hosting


    # Для перепрограммирования терминалов
    MTS_API_SMS_LOGIN=рассыльщик СМС Логин
    MTS_API_SMS_PASSWORD=рассыльщик СМС Пароль
    MTS_API_SMS_NAMING=рассыльщик СМС От имени СМС
    MTS_API_SMS_TEST_TEL=рассыльщик СМС тестовая СМС

    # Для получения номеров телефонов терминалов из БД_2
    DB_HOST= адрес БД
    MYSQL_DB_NAME= Название БД
    MYSQL_PORT= Порт БД
    MYSQL_USER= Учётка БД
    MYSQL_PASSWORD= Пароль учётки.
    ```

# Доп. функции
* Простейшая миграция объектов из wialon в глонасс, перенос произвольных полей.
* При необходимости, если не работает Wialon, можно выполнять запросы через Tor:
    1. Установить Tor на компьютер: `sudo apt install tor`
    2. Установить obfs4proxy для мостов на компьютер: `sudo apt install obfs4proxy`
    3. Получить мосты.
    4. Внести в Torrc `/etc/tor` необходимые данные:
        ```
        UseBridges 1

        ClientTransportPlugin obfs4 exec /usr/bin/obfs4proxy

        Bridge <Мосты>
        ```
    5. Внести изменения проксирования в стандартную библиотеку Wialon для Python:
        ```
        import socks
        import socket

        socks.set_default_proxy(socks.SOCKS5, "localhost", 9050)
        socket.socket = socks.socksocket


        proxies = {
            'http': 'socks5://localhost:9050',
            'https': 'socks5://localhost:9050'
        }

        ...

        request = requests.post(url=self.base_url, params=parameters, proxies=proxies)
        ...

        ```
## Ввёл в код Мигратор.
Требуется рефакторинг.


