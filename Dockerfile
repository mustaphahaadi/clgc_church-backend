FROM python:3.13.2-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get upgrade -y && apt-get install -y gcc python3-dev musl-dev && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt 
RUN python manage.py test && python manage.py migrate &&  python manage.py create_user_details


# EXPOSE 8000

CMD [ "python", "manage.py", "runserver" ,"0.0.0.0:8000"]

# docker ps
# docker build -t clgc_backend .
# docker run --name clgc_backend_container -d -p 8000:8000 clgc_backend
# docker logs -f clgc_backend_container
