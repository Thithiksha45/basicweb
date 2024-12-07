from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

# Home route
@app.route("/")
def home():
    return render_template("home.html")

# About route
@app.route("/about")
def about():
    return render_template("about.html")

# Contact route
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        
        if name and email and message:
            new_contact = Contact(name=name, email=email, message=message)
            db.session.add(new_contact)
            db.session.commit()
            flash("Your message has been sent successfully!", "success")
            return redirect(url_for("contact"))
        else:
            flash("All fields are required!", "danger")
    
    return render_template("contact.html")

if __name__ == "__main__":
    # Fix: Wrap `db.create_all()` in an application context
    with app.app_context():
        db.create_all()  # Create database tables if not already present
    app.run(debug=True)
