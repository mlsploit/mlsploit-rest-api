# MLsploit REST API

## ENVIRONMENT VARIABLES

The primary configuration settings of the API are stored
inside the `.env` file.

The first thing you should update before running anything
is the `MLSPLOIT_API_SECRET_KEY`,
which is necessary for the security of the API.
It should ideally be a string with at least 50 characters, and should
contain lowercase, uppercase, numeric as well as special characters.
You can use [this tool](https://pinetools.com/random-string-generator)
to quickly generate a secret key.

## DOCKER SETUP

We use `docker-compose` to setup and run the API service.
You will need to setup [docker](https://www.docker.com/get-started) on your system,
and then run the following commands.

### Build the Docker images

```bash
$ bash docker-setup-api.sh
```

### Create a super user (administrator)

```bash
$ bash docker-manage-api.sh createsuperuser --username admin
```

#### Create an admin token

```bash
$ bash docker-manage-api.sh drf_create_token admin
```

### Create modules

```bash
$ bash docker-manage-api.sh createmodule helloworld https://github.com/mlsploit/module-helloworld.git
```

### Start the API server

```bash
$ bash docker-start-api.sh
```

## MANUAL SETUP

### Install the dependencies

```bash
$ pip install -r requirements.txt
```

### Provision the database

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

### Create a super user (administrator)

```bash
$ python manage.py createsuperuser --username admin
```

#### Create an admin token

```bash
$ python manage.py drf_create_token admin
```

### Create modules

```bash
$ python manage.py createmodule helloworld https://github.com/mlsploit/module-helloworld.git
```

### Start the API server

```bash
$ python manage.py runserver
```

This will start the server on port 8000.

## Model Architecture

![architecture](architecture.png)
