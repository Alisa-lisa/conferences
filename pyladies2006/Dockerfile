FROM python:3.8

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY self_quantify_app/ /app/self_quantify_app/
COPY app.py /app
COPY run.sh /app
RUN chmod +x run.sh


EXPOSE 5000

CMD ["./run.sh"]
