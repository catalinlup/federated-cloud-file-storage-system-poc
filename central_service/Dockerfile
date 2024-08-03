FROM python:3.10

ARG env_file

COPY requirements.txt ./
RUN pip install python-dotenv
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ADD envs/$env_file src/.env

ADD keys/central_service_key.json src/keys/key.json

EXPOSE 8080

WORKDIR src

CMD ["sh", "-c", "flask run --host 0.0.0.0 --port 8080"]
