from src import api, app
from src.restAPI import Order

api.add_resource(Order, '/order')

if __name__ == "__main__":
    app.run(debug=True)
