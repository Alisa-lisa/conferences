FROM python:3.8

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py /app
COPY blueprints/ /app/blueprints/
COPY storage/ /app/storage/
COPY run.sh /app
RUN chmod +x run.sh
RUN export EXPLAIN_TEMPLATE_LOADING=true

EXPOSE 5000

CMD ["./run.sh"]
