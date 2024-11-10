FROM python

RUN mkdir /app

COPY . /app/

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["/bin/bash", "-c", "python3 main.py"]