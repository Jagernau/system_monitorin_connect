FROM python:3.10
COPY . /system_monitorin_connect
WORKDIR /system_monitorin_connect

ENV GLONASS_LOGIN=${GLONASS_LOGIN}
ENV GLONASS_PASSWORD=${GLONASS_PASSWORD}
ENV GLONASS_BASED_ADRESS=${GLONASS_BASED_ADRESS}
ENV SCOUT_TREEHUNDRED_LOGIN=${SCOUT_TREEHUNDRED_LOGIN}
ENV SCOUT_TREEHUNDRED_PASSWORD=${SCOUT_TREEHUNDRED_PASSWORD}
ENV SCOUT_TREEHUNDRED_BASED_ADRESS=${SCOUT_TREEHUNDRED_BASED_ADRESS}
ENV SCOUT_TREEHUNDRED_BASE_TOKEN=${SCOUT_TREEHUNDRED_BASE_TOKEN}
ENV GELIOS_BASED_ADRES=${GELIOS_BASED_ADRESS}
ENV GELIOS_LOGIN=${GELIOS_LOGIN}
ENV GELIOS_PASSWORD=${GELIOS_PASSWORD}
ENV FORT_LOGIN=${FORT_LOGIN}
ENV FORT_PASSWORD=${FORT_PASSWORD}
ENV FORT_BASED_ADRESS=${FORT_BASED_ADRESS}
ENV ERA_LOGIN=${ERA_LOGIN}
ENV ERA_PASSWORD=${ERA_PASSWORD}
ENV ERA_BASED_ADRESS=${ERA_BASED_ADRESS}
ENV ERA_PORT=${ERA_PORT}
ENV SCOUT_LOCAL_LOGIN=${SCOUT_LOCAL_LOGIN}
ENV SCOUT_LOCAL_PASSWORD=${SCOUT_LOCAL_PASSWORD}
ENV SCOUT_LOCAL_BASED_ADRESS=${SCOUT_LOCAL_BASED_ADRESS}
ENV SCOUT_LOCAL_PORT=${SCOUT_LOCAL_PORT}
ENV WIALON_LOCAL_TOKEN=${WIALON_LOCAL_TOKEN}
ENV WIALON_LOCAL_BASED_ADRESS=${WIALON_LOCAL_BASED_ADRESS}
ENV WIALON_LOCAL_PORT=0
ENV WIALON_HOSTING_TOKEN=${WIALON_HOSTING_TOKEN}
ENV WIALON_HOSTING_BASED_ADRESS=${WIALON_HOSTING_BASED_ADRESS}
ENV WIALON_HOSTING_PORT=0
ENV MTS_API_SMS_LOGIN=${MTS_API_SMS_LOGIN}
ENV MTS_API_SMS_PASSWORD=${MTS_API_SMS_PASSWORD}
ENV MTS_API_SMS_NAMING=${MTS_API_SMS_NAMING}
ENV MTS_API_SMS_TEST_TEL=${MTS_API_SMS_TEST_TEL}

ENV DB_HOST=${DB_HOST}
ENV MYSQL_USER=${MYSQL_USER}
ENV MYSQL_DB_NAME=${MYSQL_DB_NAME}
ENV MYSQL_PASSWORD=${MYSQL_PASSWORD}
ENV MYSQL_PORT=${MYSQL_PORT}
ENV API_TOKEN=${API_TOKEN}

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
