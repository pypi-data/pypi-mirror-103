import os
def create_app_ini():
    with open("app.ini","w") as f:
        f.write(f"""\
[uwsgi]
wsgi-file = app.py
callable = app
socket = :8080
processes = 4
threads = 2
master = true
chmod-socket = 660
vacuum = true
die-on-term = true\
""")

def create_flask_dockerfile():
    with open("Dockerfile","w") as f:
        f.write(f"""\
FROM python:3.7.2-stretch
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
CMD ["uwsgi", "app.ini"]\
""")

def create_docker_compose_yml(project_name):
    def wrapper():
        with open("docker-compose.yml","w") as f:
            f.write(f"""\
version: "3.7"

services:

  flask:
    build: ./
    container_name: flask
    restart: always
    environment:
      - APP_NAME={project_name}
    expose:
      - 8080

  nginx:
    build: ./nginx
    container_name: nginx
    restart: always
    ports:
      - "80:80"
""")
    return wrapper

def create_nginx_conf():
  os.mkdir('nginx')
  with open(os.path.join('nginx', 'nginx.conf'), 'w') as f:
    f.write("""\
server {

    listen 80;

    location / {
        include uwsgi_params;
        uwsgi_pass flask:8080;
    }

}   
""")

def create_nginx_dockerfile():
    with open(os.path.join("nginx","Dockerfile"),"w") as f:
        f.write(f"""\
FROM nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/\
""")