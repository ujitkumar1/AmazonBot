from flask import request
from flask_restful import Resource

from src.amazon import AmazonPhoneSearch
from src.log import log


class Order(Resource):
    """
    Represents an API resource for placing orders using AmazonPhoneSearch.
    Supports both GET and POST methods for placing orders and user login.

    Attributes:
        username (str): User's username for authentication.
        password (str): User's password for authentication.
        driver_path (str): Path to the ChromeDriver executable.

    Methods:
        get(): Handles the GET request to place an order based on provided JSON data.
        post(): Handles the POST request for user login and data processing.
    """

    def get(self):
        """
        Handles the GET request for placing an order based on JSON data.

        Returns:
            dict: Response indicating whether the order was successfully placed.
        """
        log.info("Order-GET METHOD Called")

        log.info("Fetching the Json Data")
        start_price = request.json.get('start_price')
        end_price = request.json.get('end_price')
        product_name = request.json.get('product_name')
        product_company = request.json.get('product_company')
        log.info("Fetching Json Completed")

        if not all([start_price, end_price, product_company, product_name]):
            log.error("Missing Data in Json Request")
            return {'Error': "Data missing"}, 500

        if not (type(start_price) == float and type(end_price) == float and type(product_name) == str and type(
                product_company) == str):
            log.error("Data Not in correct format")
            return {'Error': "Data not correct"}, 500

        # Path to the ChromeDriver executable
        self.driver_path = "C:\Program Files (x86)\chromedriver.exe"
        try:
            log.info("Starting the Order Process")
            order = AmazonPhoneSearch(self.username, self.password, self.driver_path, start_price, end_price,
                                      product_name, product_company)
            order.run()

            log.info("Order Placed - OrderID")
            return {"Order Placed": "OrderID"}, 200
        except Exception as e:
            log.error("Exception ", e)
            return {
                "Error": "Some error occ."
            }, 500

    def post(self):
        """
        Handles the POST request for user login and data processing.

        Returns:
            dict: Response indicating that the data has been received and processed.
        """
        log.info("Order - POST METHOD - User Login")
        Order.username = request.json.get('username')
        Order.password = request.json.get('password')
        log.info("Data Received")

        return {"Message": "Data Received, Proceed with Order in GET REQUEST"}
