FROM python:3.9
USER root
RUN mkdir /app
COPY . /app/
WORKDIR /app/
RUN pip3 install -r requirements.txt
ENV AIRFLOW_HOME="/app/airflow"
ENV AIRFLOW__CORE__DAGBAG_IMPORT_TIMEOUT=1000
ENV ARIFLOW__CORE__ENABLE_XCOM_PICKLING=True
RUN airflow db init
RUN airflow users create -e shaktijain9@gmail.com -f Shakti -l Jain -p admin -r Admin -u admin
RUN chmod 777 start.sh
RUN apt update -y && apt install awscli -y
ENTRYPOINT ["/bin/sh"]
CMD ["start.sh"]