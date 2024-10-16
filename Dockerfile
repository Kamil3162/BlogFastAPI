# Dockerfile

# pull the official docker image
FROM python:3.9

# set work directory
WORKDIR /BlogFastAPI

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

ENV PYTHONPATH=/BlogFastAPI

# copy project
CMD ["uvicorn", "BlogFastAPI.app.main", "--host", "0.0.0.0", "--port", "8000"]
