from flask import Blueprint, render_template, flash, redirect, request

from marvel_shop.models import Comic, db, Customer, Order
from marvel_shop.forms import ComicForm

site = Blueprint('site', __name__, template_folder = 'site_templates')


@site.route('/')
def shop():
    allcomics = Comic.query.all()
    allcustomers = Customer.query.all()
    allorders = Order.query.all()

    shop_stats = {
        'customers': len(allcomics),
        'sales': sum([order.order_total for order in allorders]),
        'customers' : len(allcustomers)
    }

    our_class = "Rangers are the best"

    return render_template('shop.html', shop = allcomics, stats = shop_stats)

@site.route('/shop/create', methods = ['GET', 'POST'])
def create():
    createform = ComicForm()

    if request.method == 'POST' and createform.validate_on_submit():
        name = createform.name.data
        image = createform.image.data
        description = createform.description.data
        price = createform.price.data
        quantity = createform.quantity.data 

        comic = Comic(name, price, quantity, image, description)

        db.session.add(comic)
        db.session.commit()

        flash(f"You have successfully created comic {name}", category = 'success')
        return redirect('/')

    elif request.method == 'POST':
        flash("We were unable to process your request", category = 'warning')
        return redirect('/shop/create')
    
    return render_template('create.html', form = createform)

@site.route('/shop/delete/<id>')
def delete(id):

    comic = Comic.query.get(id)

    db.session.delete(comic)
    db.session.commit()

    return redirect('/')






