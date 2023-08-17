# AmazonBOT: A Python app for placing an Order on Amazon with 1 Click

## Description

AmazonBOT is a user-friendly Python application designed to simplify the process of placing orders on Amazon. With just
one click,
users can effortlessly initiate an order for a desired product. This streamlined and efficient solution aims to enhance
the convenience and
speed of online shopping, making it easier than ever to make purchases on Amazon's platform.

## Prerequisites

Before using this application, ensure you have the following prerequisites:

1. Python Programming Language
2. MySQL
3. Flask
4. Flask-RESTful
5. beautifulsoup4(bs4)
6. Selenium

## Installation

To install the required packages and libraries, run the following command in your terminal:

```
pip install -r requirements.txt
```

This command will install all the necessary dependencies listed in the requirements.txt file, allowing you to run the
project without any issues.

### Usage:

1. Start the application by running the following command in the project directory:

```
python main.py
```

This will start the application, and you should be able to use it. (or) Directly run the main.py file by defalt the url
of application would be : http://127.0.0.1:5000

This will start the Redis server and the Celery worker to enable asynchronous task processing.

#### Endpoint Working:

1. **Login**:

    - Endpoint: /order
    - Description: Used to login the user.
    - Method: POST
    - Example Request:```POST http://127.0.0.1:5000/order```
    - Example Input:
    - ```{"username":"hello@hello.com","password":"123"}```
    - Example Response:
    - ```{"Message": "Data Received, Proceed with Order in GET REQUEST"}```


2. **Palace Order**:

    - Endpoint: /order
    - Description: Retrieve a generated store report.
    - Method: GET
    - Example Request: ```GET http://127.0.0.1:5000/order```
    - Example Input:
    - ```{"start_price":10000.0, "end_price": 20000.0, "product_name" :"smartphone", "product_company":"Samsung"}```
    - Example Response (Report Generation Completed):
    - ```{"Order Placed": "<OrderID>"}```

### Contact:

**Name** : Ujit Kumar

**Email** : ujitkumar1@gmail.com
