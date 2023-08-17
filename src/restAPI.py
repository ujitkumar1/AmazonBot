from flask import request
from flask_restful import Resource

from src.amazon import AmazonPhoneSearch


class Order(Resource):
    def get(self):
        start_price = request.json.get('start_price')
        end_price = request.json.get('end_price')
        product_name = request.json.get('product_name')
        product_company = request.json.get('product_company')

        if not all([start_price, end_price, product_company, product_name]):
            return {'Error': "Data missing"}, 500

        if not (type(start_price) == float and type(end_price) == float and type(product_name) == str and type(
                product_company) == str):
            return {'Error': "Data not correct"}, 500

        self.driver_path = "C:\Program Files (x86)\chromedriver.exe"
        print(self.username, self.password, self.driver_path, start_price, end_price, product_name, product_company)
        try:
            print(self.username, self.password, self.driver_path, start_price, end_price, product_name, product_company)
            order = AmazonPhoneSearch(self.username, self.password, self.driver_path, start_price, end_price,
                                      product_name, product_company)
            order.run()
            return {"Order Placed": "OrderID"}, 200
        except:
            return {
                "Error": "Some error occ."
            }, 500

    def post(self):
        Order.username = request.json.get('username')
        Order.password = request.json.get('password')
        return ("Done...!")
