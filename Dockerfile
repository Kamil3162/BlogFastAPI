#Dockerfile

# pull the official docker image
FROM python:3.9

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

ENV PYTHONPATH=/BlogFastAPI

# Make the entrypoint script executable
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Run migrations and start app
ENTRYPOINT ["./entrypoint.sh"]

# copy project
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
