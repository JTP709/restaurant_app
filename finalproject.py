from flask import Flask
app = Flask(__name__)

@app.route('/restaurants/')
def showRestaurants():
	return "This page will show all of my restaurants."

@app.route('/restaurants/new/')
def newRestaurants():
	return "This page will be for making a new restaurant."

@app.route('/restaurants/restaurant_id/edit')
def editRestaurants():
	return "This page will be for editing restaurants."

@app.route('/restaurants/restaurant_id/delete')
def deleteRestaurants():
	return "This page will be for deleting restaurants."

@app.route('/restaurants/restaurant_id/menu')
@app.route('/restaurants/restaurant_id/')
def showMenu():
	return "This page is the menu for the restaurant's id."

@app.route('/restaurants/restaurant_id/new/')
def newMenuItem():
	return "This page will be for making a new menu item."

@app.route('/restaurants/restaurant_id/menu_id/edit')
def editMenuItem():
	return "This page will be for editing menu items."

@app.route('/restaurants/restaurant_id/menu_id/delete')
def deleteMenuItem():
	return "This page will be for deleting menu items."

if __name__=='__main__':
	app.debug = True
	app.run(host = '0.0.0.0',port = 5000)