from restAPI import api, Order, app

api.add_resource(Order,'/place-order')

if __name__=="__main__":
    app.run(debug=True)