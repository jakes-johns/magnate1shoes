from flask import Flask, render_template, redirect, url_for, session, request, flash
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')  # Ensure SECRET_KEY is set in .env

# Configure Flask-Mail
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

# Dummy data for shoes
shoes = [
    {'id': 1, 'name': 'Running Shoes', 'price': 649, 'description': 'Perfect for running', 'image': 'images/running_shoes.jpg'},
    {'id': 2, 'name': 'Casual Sneakers', 'price': 1190, 'description': 'Great for everyday wear', 'image': 'images/casual_sneakers.jpg'},
    {'id': 3, 'name': 'Formal Shoes', 'price': 1399, 'description': 'Sleek and stylish for formal events', 'image': 'images/formal_shoes.jpg'},
    {'id': 4, 'name': 'Basketball Shoes', 'price': 799, 'description': 'Ideal for the court', 'image': 'images/basketball_shoes.jpg'},
    {'id': 5, 'name': 'Sandals', 'price': 850, 'description': 'Comfortable for summer', 'image': 'images/sandals.jpg'}
]

# Home route displaying all shoes
@app.route('/')
def index():
    return render_template('index.html', shoes=shoes)

# Route for shoe details
@app.route('/shoe/<int:shoe_id>')
def shoe_detail(shoe_id):
    shoe = next((s for s in shoes if s['id'] == shoe_id), None)
    if shoe:
        return render_template('shoe_detail.html', shoe=shoe)
    else:
        return "Shoe not found", 404

@app.route('/purchase/<int:shoe_id>', methods=['GET', 'POST'])
def purchase(shoe_id):
    shoe = next((s for s in shoes if s['id'] == shoe_id), None)
    if not shoe:
        return "Shoe not found", 404
    
    if request.method == 'POST':
        client_name = request.form['client_name']
        client_email = request.form['client_email']
        
        # Debug: Check form data
        print(f"Client Name: {client_name}, Client Email: {client_email}")
        
        try:
            msg = Message(f"New Purchase: {shoe['name']}", recipients=['magnatefxke@gmail.com'])
            msg.body = f"""
            A new purchase has been made!

            Client Name: {client_name}
            Client Email: {client_email}
            Item Purchased: {shoe['name']}
            Price: Ksh{shoe['price']}
            """
            mail.send(msg)
            flash("Purchase successful! We will get back to you soon.")
            print("Email sent successfully.")  # For debugging
        except Exception as e:
            flash("Purchase successful! However, notification could not be sent.")
            print(f"Error sending email: {e}")
            
            # Optionally, send an email to yourself for debugging if needed
            msg = Message("Error sending purchase notification", recipients=["youremail@example.com"])
            msg.body = f"Error: {str(e)}"
            mail.send(msg)

        
        return redirect(url_for('index'))
    
    return render_template('purchase.html', shoe=shoe)

# Route to add a shoe to the cart
@app.route('/add_to_cart/<int:shoe_id>')
def add_to_cart(shoe_id):
    shoe = next((s for s in shoes if s['id'] == shoe_id), None)
    if shoe:
        cart = session.get('cart', [])
        cart.append(shoe)
        session['cart'] = cart
        flash(f"{shoe['name']} has been added to your cart!")
    else:
        flash("Shoe not found.")
    return redirect(url_for('index'))

# Cart page to show added items
@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    total_price = sum(item['price'] for item in cart)
    return render_template('cart.html', cart=cart, total_price=total_price)

if __name__ == '__main__':
    app.run(debug=True)
