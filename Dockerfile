FROM python:3.13.2-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get upgrade \
    && apt-get install gcc python3-dev musl-dev 

RUN python -m pip install -r requirements.txt --no-cache-dir && \
    python manage.py migrate 


EXPOSE 8000

CMD [ "python", "manage.py", "runserver" ]

# docker ps
# docker build -t clgc_backend .
# docker run --name clgc_backend_container -d -p 8000:8000 clgc_backend
# docker logs -f clgc_backend_container