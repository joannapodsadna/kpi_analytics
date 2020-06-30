FROM python:2.7-stretch

RUN apt-get update
RUN apt-get install -y \
    g++ \
    unixodbc-dev \
    libsasl2-modules-gssapi-mit

RUN wget https://public-repo-1.hortonworks.com/HDP/hive-odbc/2.1.16.1023/Debian/hive-odbc-native_2.1.16.1023-2_amd64.deb
RUN dpkg -i hive-odbc-native_2.1.16.1023-2_amd64.deb

COPY ./ /opt/kpi

RUN cd /opt/kpi; pip install --trusted-host pypi.python.org -r requirements.txt

CMD ["python", "/opt/kpi/src/kpi_generator.py"]