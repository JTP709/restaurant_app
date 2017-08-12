from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

# Import CRUD operations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Restaurant,MenuItem

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

#API Endpoint (JSON Request) for restaruants
@app.route('/restaurants/<int:restaurant_id>/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return jsonify(MenuItems = [i.serialize for i in items])

#API Endpoint (JSON Request) for menus
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/JSON')
def restaurantMenuItemJSON(restaurant_id,menu_id):
	menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
	return jsonify(MenuItems = menuItem.serialize)

#Page that lists out all restaruants
@app.route('/')
@app.route('/restaurant/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)

#Page for a restaraunt's menu
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	return render_template('menu.html',restaurant=restaurant, items=items)

#Page for making a new restaurant
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'],restaurant_id = restaurant_id)
		session.add(newItem)
		session.commit()
		flash("New menu item created!")
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
		return render_template('newMenuItem.html', restaurant_id=restaurant_id)

#Page for editing a menu item
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/',methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
	editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		session.add(editedItem)
		session.commit()
		flash("Menu item edited!")
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
		return render_template('editMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)

#Page for deleting a menu item
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/',methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
	deletedItem = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			deletedItem.name = request.form['name']
		session.delete(deletedItem)
		session.commit()
		flash("Menu item deleted!")
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
		return render_template('deleteMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=deletedItem)
	

if __name__=='__main__': #only activates if executed using the Python interpetor (i.e. host machine), not if it's called from another computer.
	app.secret_key = 'super_secret_key'
	app.debug = True # reloads itself when it detects a code change.
	app.run(host = '0.0.0.0', port = 5000) # tells vagrant VM to scan on all public IP addresses