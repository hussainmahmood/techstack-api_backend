# techstack-api_backend

## Clone this repo

Type following command in you terminal:

```bash
# clone this repo in your machine
git clone https://github.com/hussainmahmood/techstack-api_backend.git

# move to project folder
cd techstack-api_backend
```

## Setup project

Once you've cloned this project, create a virtual environment and install dependencies:

```bash
# create a virtual environment
virtualenv .venv

# source your virtual environment
# Linux
source .venv/bin/activate

# Windows Powershell
.venv/Scripts/activate.ps1

# Command prompt
call .venv/Scripts/activate

# install dependencies
pip install -r requirements.txt
```

Once you've installed dependencies, make migrations and start server:

```bash
# make migrations
python manage.py makemigrations

# migrate
python manage.py migrate

# start server
python manage.py runserver {hostname}:{port}
```

## Database population

Run following commands to populate product table with dummy data:

```bash
# Windows Powershell
$Parameters = @{
    Method = "POST"
    Uri =  "http://{hostname}:{port}/api/product/generate_data/"
    ContentType = "application/json"
}
Invoke-RestMethod @Parameters

# Linux
curl -X POST http://{hostname}:{port}/api/product/generate_data/
   -H 'Content-Type: application/json'
```

