# Welcome to OLX scraping application

## installation

1. Go to main folder and create python virtual env

> python -m venv venv

   - Activate virualenv for windows
   > venv\Scripts\activate

2. Using venv terminal use requirement.txt to install required libraries used in this project

> pip install -r requirements.txt

3. while in venv run the flask application

> flask run

4. using localhost and using any api tool like postman to run the endpoint

> Please note that before running this tool you should adjust the DB connection 
> the DB connection line will be available at /Server/__init__.py at line 6 adjust the DB colleciton name and url and port

> http://127.0.0.1:5000/scrape_olx

> this method is post with payload that contains all 3 fields

```
eg:
{
    "key_word": "mobile",
    "email": "oatef98@gmail.com",
    "items_in_mail": 20
}
```

## process explaination

this tool will start by going to olx and login using a default account after logging in the application will use the key_word to search for it and get all the listings associated

after getting the ads it will get each ad detail and store it in DB

after storing in DB come the part which formats the data stored in DB and send email to targeted email 
