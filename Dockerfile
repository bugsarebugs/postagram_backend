FROM python:3.12-alpine
# pull official base image 

WORKDIR /app 

# Install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev

# Install python dependencies 
COPY requirements.txt /app/requirements.txt 
RUN pip install --upgrade pip 
RUN pip install --no-cache-dir -r requirements.txt 

# Add app 
COPY . .
