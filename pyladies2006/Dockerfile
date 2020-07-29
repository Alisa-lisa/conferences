FROM python:3.8

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY self_quintify_app/ /app/self_quintify_app
COPY run.sh /app
RUn chmod +x run.sh


EXPOSE 5000

CMD ["/.run.sh"]
