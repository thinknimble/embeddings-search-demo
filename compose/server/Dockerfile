FROM python:3.7-slim-buster

# These environment values help with watching for file changes
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install system-level dependencies.
RUN apt-get update \
    # dependencies for building Python packages
    && apt-get install -y build-essential \
    && apt-get install -y gcc \
    # psycopg2 dependencies
    && apt-get install -y libpq-dev \
    # Pillow dependencies
    && apt-get install -y libjpeg-dev zlib1g-dev \
    && apt-get install -y python3-pip

# Set the name of the working directory inside the docker container
WORKDIR /app

# Install pipenv and create a virtual environment with it.
COPY ./Pipfile /app/Pipfile
COPY ./Pipfile.lock /app/Pipfile.lock

# Install Python packages from the Pipfile at the system level,
# since virtual environments are not needed in containers.
RUN pip3 install pipenv \
    && pipenv install --system --deploy --ignore-pipfile

# Move the 'start' shell script to the root
# and alter line endings for compatibility.
COPY ./compose/server/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
