# Repository Name
Project for HashMicro

## Prerequisites

Before you begin, make sure you have the following prerequisites installed:

- UBUNTU 22.04.5
- Python 3.x
- Git (to clone repositories or install dependencies from GitHub)

## Installation

Follow the steps below to install and run this project:

**1. Install Database postgresql-10**

First, we will install the postgresql-10 database.

```bash
sudo wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -sc)-pgdg main" > /etc/apt/sources.list.d/PostgreSQL.list'

sudo apt update
sudo apt-get install postgresql-10
```

Database setup

```bash
sudo -u postgres psql -c "CREATE USER uprohashmicro WITH ENCRYPTED PASSWORD 'PwDprohashmicroSatu1Dua3';"
sudo -u postgres psql -c "CREATE DATABASE db_prohashmicro;"

sudo -u postgres psql db_prohashmicro -c "GRANT ALL ON ALL TABLES IN SCHEMA public to uprohashmicro;"
sudo -u postgres psql db_prohashmicro -c "GRANT ALL ON ALL SEQUENCES IN SCHEMA public to uprohashmicro;"
sudo -u postgres psql db_prohashmicro -c "GRANT ALL ON ALL FUNCTIONS IN SCHEMA public to uprohashmicro;"
```


**2. Install Environment**

Second, we will create an environment for the HashMicro project.

```bash
sudo apt install language-pack-id
sudo dpkg-reconfigure locales

sudo apt install -y python3 python3-pip python3-venv
python3 -m pip install --user pipenv
sudo -H pip3 install virtualenv

python3.10 -m venv envprohashmicro
```

**3. Clone Repository**

Third, clone this repository to your local machine using the following command:

```bash
git clone https://github.com/herbew/prohashmicro.git
```

**4. Install Service**

To install the service, the first thing to do is to ensure that all the required libraries are properly installed according to the Ubuntu 22.04.5 OS.

```bash
sudo apt install dos2unix -y 
dos2unix prohashmicro/utilities/install_os_dependencies.sh 
dos2unix prohashmicro/utilities/install_python_dependencies.sh

sudo chmod a+x prohashmicro/utilities/install_os_dependencies.sh
sudo chmod a+x prohashmicro/utilities/install_python_dependencies.sh

sudo ./prohashmicro/utilities/install_os_dependencies.sh install
```
Then, install the application libraries.

```bash
source envprohashmicro/bin/activate
cd prohashmicro
./utilities/install_python_dependencies.sh
```

**5. Setup Service**

Running the setup, according to django framework rules

```bash
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser

python3 manage.py loaddata modules/fixtures/0001_module.json
python3 manage.py loaddata users/fixtures/0002_users.json
```

**6. Test Service**

To ensure everything is running well, testing must be carried out.

```bash
python manage.py test  --verbosity=2

```

**7. Running Service**

The last step for local service is to run the service.

```bash
python manage.py runserver 0.0.0.0:8000
```







