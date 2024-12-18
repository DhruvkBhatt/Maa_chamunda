from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from email_service import send_admin_email, send_client_acknowledgment
from config import Config
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate=Migrate(app,db)

mail = Mail(app)
# Enable CORS for all routes
CORS(app)


# Database Model for Tour Packages
class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    images = db.Column(db.Text, nullable=False)  # Comma-separated image URLs
    highlights = db.Column(db.Text, nullable=True)
    inclusions = db.Column(db.Text, nullable=True)
    exclusions = db.Column(db.Text, nullable=True)
    specialty_tour = db.Column(db.String(50), nullable=True)  # New field
    tour_type = db.Column(db.String(50), nullable=True)       # New field
    city = db.Column(db.String(50), nullable=True)            # New field
    # category = db.Column(db.String(50), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_popular = db.Column(db.Boolean, default=False)
    show_on_homepage = db.Column(db.Boolean, default=False)

    # Add the to_dict method
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "duration": self.duration,
            "images": self.images.split(","),  # Convert image string to a list
            "highlights": self.highlights,
            "inclusions": self.inclusions,
            "exclusions": self.exclusions,
            "specialty_tour": self.specialty_tour,
            "tour_type": self.tour_type,
            "city": self.city,
            # "category": self.category,
            "is_active": self.is_active,
            "is_popular": self.is_popular,
            "show_on_homepage": self.show_on_homepage,
        }

# Itinerary Model
class Itinerary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day_description = db.Column(db.Text, nullable=False)  # Description of the day's activities
    day_number = db.Column(db.Integer, nullable=False)     # Day number (e.g., Day 1, Day 2)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False)  # Foreign key reference to Package
    
    # Relationship to Package
    package = db.relationship('Package', backref=db.backref('itinerary', lazy=True))

    def __repr__(self):
        return f"<Itinerary Day {self.day_number} for Package {self.package_id}>"

# Initialize Database
with app.app_context():
    db.create_all()



@app.route("/")
def index():
    # Fetch featured packages
    featured_packages = Package.query.filter_by(show_on_homepage=True).all()

    # Fetch popular destinations
    popular_destinations = Package.query.filter_by(is_popular=True).all()

    return render_template(
        "index.html",
        featured_packages=featured_packages,
        popular_destinations=popular_destinations,
    )


@app.route("/about-us")
def about():
    return render_template("about-us.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/home")
def home():
    return render_template("home.html")

# @app.route("/packages")
# def packages():
#     return render_template("packages.html")

@app.route("/enquiry")
def enquiry():
    return render_template("enquiry.html")


@app.route('/submit-enquiry', methods=['POST'])
def submit_enquiry():
    try:
        # Handle form data
        if request.form:
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            message = request.form.get('message')
        elif request.is_json:
            data = request.get_json()
            name = data.get('name')
            email = data.get('email')
            phone = data.get('phone')
            message = data.get('message')
        else:
            return jsonify({"status": "error", "message": "Unsupported data format"})

        # Send emails
        send_admin_email(mail, name, email, phone, message)
        send_client_acknowledgment(mail, email, name, email, phone, message)

        # Flash success message
        flash("Thank you for your enquiry! A confirmation email has been sent to you.", "success")
        return redirect(url_for('home'))

    except Exception as e:
        print(f"Error: {e}")
        flash("There was an issue processing your request. Please try again later.", "danger")
        return redirect(url_for('index'))


@app.route('/submit-hotel-booking', methods=['POST'])
def submit_hotel_booking():
    try:
        # Handle form data
        if request.form:
            name = request.form.get('name')
            email = request.form.get('email')
            contact = request.form.get('contact')
            location = request.form.get('Location')  # Added location field
            checkin = request.form.get('checkin')
            checkout = request.form.get('checkout')
            rooms = request.form.get('rooms')
            adults = request.form.get('adults')
            children = request.form.get('children')
            message = request.form.get('message')
        elif request.is_json:
            data = request.get_json()
            name = data.get('name')
            email = data.get('email')
            contact = data.get('contact')
            location = data.get('Location')  # Added location field
            checkin = data.get('checkin')
            checkout = data.get('checkout')
            rooms = data.get('rooms')
            adults = data.get('adults')
            children = data.get('children')
            message = data.get('message')
        else:
            return jsonify({"status": "error", "message": "Unsupported data format"})

        # Send admin email
        send_admin_email(
            mail, "hotel booking",
            name=name, email=email, contact=contact, location=location, checkin=checkin, 
            checkout=checkout, rooms=rooms, adults=adults, 
            children=children, message=message
        )

        # Send client acknowledgment
        send_client_acknowledgment(mail, email, name, "hotel booking")

        flash("Your hotel booking request has been submitted successfully.", "success")
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error: {e}")
        flash("An error occurred while processing your request.", "danger")
        return redirect(url_for('index'))


@app.route('/submit-train-booking', methods=['POST'])
def submit_train_booking():
    try:
        # Handle form data
        if request.form:
            name = request.form.get('name')
            email = request.form.get('email')
            contact = request.form.get('contact')
            From = request.form.get('from')
            To = request.form.get('to')
            departure = request.form.get('departure')
        elif request.is_json:
            data = request.get_json()
            name = data.get('name')
            email = data.get('email')
            contact = data.get('contact')
            From = data.get('from') # Updated field
            To = data.get('to') # Updated field
            departure = data.get('departure')
        else:
            return jsonify({"status": "error", "message": "Unsupported data format"})

        # Send admin email
        send_admin_email(
            mail, "train booking",
            name=name, email=email, contact=contact, From=From, To=To, departure_date=departure
        )

        # Send client acknowledgment
        send_client_acknowledgment(mail, email, name, "train booking")

        flash("Your train booking request has been submitted successfully.", "success")
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error: {e}")
        flash("An error occurred while processing your request.", "danger")
        return redirect(url_for('index'))


@app.route('/submit-bus-booking', methods=['POST'])
def submit_bus_booking():
    try:
        # Handle form data
        if request.form:
            name = request.form.get('name')
            email = request.form.get('email')
            contact = request.form.get('Contact')
            From = request.form.get('From')  # Updated field
            To = request.form.get('To')  # Updated field
            departure_date = request.form.get('departure')
        elif request.is_json:
            data = request.get_json()
            name = data.get('name')
            email = data.get('email')
            contact = data.get('contact')
            From = data.get('from')  # Updated field
            To = data.get('to')  # Updated field
            departure_date = data.get('departure')
        else:
            return jsonify({"status": "error", "message": "Unsupported data format"})

        # Send admin email
        send_admin_email(
            mail, "bus booking",
            name=name, email=email, contact=contact,From=From,
            To=To, departure_date=departure_date
        )

        # Send client acknowledgment
        send_client_acknowledgment(mail, email, name, "bus booking")

        flash("Your bus booking request has been submitted successfully.", "success")
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error: {e}")
        flash("An error occurred while processing your request.", "danger")
        return redirect(url_for('index'))

@app.route("/nav")
def nav():
    return render_template("nav.html")

@app.route('/bus-booking')
def bus_booking():
    return render_template('bus_booking.html')


@app.route('/hotel-booking')
def hotel_booking():
    return render_template('hotel_booking.html')


@app.route('/train-booking')
def train_booking():
    return render_template('train_booking.html')

# @app.route('/packages', methods=['GET'])
# def get_packages():
#     # Retrieve all packages from the database
#     packages = Package.query.all()
#     print("packages")
#     print(packages)
#     return jsonify([pkg.to_dict() for pkg in packages])

# @app.route('/packages', methods=['GET'])
# def get_packages():
#     # Check if the request is from a browser or an API client
#     if request.headers.get('Accept') == 'application/json':
#         # JSON response for API clients
#         category = request.args.get('category')
#         tour_type = request.args.get('tour_type')
#         specialty = request.args.get('specialty')
#         city = request.args.get('city')
#         min_duration = request.args.get('min_duration', type=int)
#         max_duration = request.args.get('max_duration', type=int)
#         is_active = request.args.get('is_active', type=lambda v: v.lower() == 'true')

#         query = Package.query

#         if category:
#             query = query.filter_by(category=category)
#         if tour_type:
#             query = query.filter_by(tour_type=tour_type)
#         if specialty:
#             query = query.filter_by(specialty_tour=specialty)
#         if city:
#             query = query.filter_by(city=city)
#         if min_duration:
#             query = query.filter(Package.duration >= min_duration)
#         if max_duration:
#             query = query.filter(Package.duration <= max_duration)
#         if is_active is not None:
#             query = query.filter_by(is_active=is_active)

#         packages = query.all()

#         return jsonify({
#             "data": [pkg.to_dict() for pkg in packages],
#             "status": "success"
#         })
#     else:
#         # Render the packages.html template for browser clients
#         return render_template('packages.html')

@app.route('/packages', methods=['GET'])
def get_packages():
    # Get filter parameters with default values
    specialties = request.args.getlist('specialties')  # Multiple specialties
    tour_types = request.args.getlist('tour_types')    # Multiple tour types
    # categories = request.args.getlist('categories')    # Multiple categories
    min_duration = request.args.get('min_duration', type=int, default=0)
    max_duration = request.args.get('max_duration', type=int, default=30)
    city = request.args.get('city', '').strip().lower()  # Case-insensitive partial match
    duration_range = request.args.get('duration_range')

    # Adjust min/max duration based on the selected range
    if duration_range == "1-3":
        min_duration, max_duration = 1, 3
    elif duration_range == "4-10":
        min_duration, max_duration = 4, 10
    elif duration_range == "10+":
        min_duration, max_duration = 10, 30

    print(f"Filters - specialties: {specialties}, tour_types: {tour_types}, min_duration: {min_duration}, max_duration: {max_duration}, city: {city}")

    # Initialize query object
    query = Package.query
    packages = query.all()
    print("packages")
    print(packages)
    for package in packages:
        print(package.duration)
    # Apply filters
    if specialties:
        query = query.filter(db.func.lower(Package.specialty_tour).in_([s.lower() for s in specialties]))
    if tour_types:
        query = query.filter(db.func.lower(Package.tour_type).in_([t.lower() for t in tour_types]))
    # if categories:
    #     query = query.filter(db.func.lower(Package.category).in_([c.lower() for c in categories]))
    if city:
        query = query.filter(db.func.lower(Package.city).ilike(f"%{city}%"))  # Case-insensitive partial match
    # if min_duration and max_duration:
    #     query = query.filter(Package.duration.between(min_duration, max_duration))

    # Execute the query
    packages = query.all()

    # Process duration dynamically
    def extract_days(duration_str):
        """Extract numerical day values from the duration string."""
        try:
            return int(duration_str.split(' ')[0])  # Extract the first number
        except (ValueError, IndexError):
            return None  # Handle invalid or missing data
    
    if min_duration and max_duration:
        packages = [
            package for package in packages
            if extract_days(package.duration) is not None and
            min_duration <= extract_days(package.duration) <= max_duration
        ]
    print("packages")
    print(packages)


    # Fetch distinct filter options from the database
    specialties_options = sorted(set(p.specialty_tour for p in Package.query.all() if p.specialty_tour))
    tour_types_options = sorted(set(p.tour_type for p in Package.query.all() if p.tour_type))
    # categories_options = sorted(set(p.category for p in Package.query.all() if p.category))

    print(f"Available filters - specialties_options: {specialties_options}, tour_types_options: {tour_types_options}")

    # Render the template and pass the data
    return render_template(
        'packages.html',
        packages=packages,
        specialties_options=specialties_options,
        tour_types_options=tour_types_options,
        # categories_options=categories_options,
        selected_specialties=specialties,
        selected_tour_types=tour_types,
        # selected_categories=categories,
        selected_min_duration=min_duration,
        selected_max_duration=max_duration,
        selected_city=city
    )




@app.route('/packages/<int:id>', methods=['GET'])
def view_package(id):
    # Get details for a single package
    package = Package.query.get_or_404(id)
    print("package")
    print(package)
    return render_template('package_details.html', package=package)

@app.route('/package-details/<int:package_id>', methods=['GET'])
def package_details(package_id):
    package = Package.query.get_or_404(package_id)
    print("package")
    print(package)
    return render_template('package_details.html', package=package)

@app.route('/add-package-12359876', methods=['GET', 'POST'])
def add_package():
    if request.method == 'GET':
        # Render the Add Package form
        return render_template('add_package.html')
    elif request.method == 'POST':
        data = request.form
        
        # Check if "Other" is selected for category, tour_type, and specialty_tour
        specialty_tour = data['specialty_tour']
        if specialty_tour == "Other":
            specialty_tour = data.get('other_specialty_tour', '').strip()

        tour_type = data['tour_type']
        if tour_type == "Other":
            tour_type = data.get('other_tour_type', '').strip()

        # category = data['category']
        # if category == "Other":
        #     category = data.get('other_category', '').strip()

        new_package = Package(
            name=data['name'],
            description=data['description'],
            duration=data['duration'],
            images=data['images'],
            highlights=data['highlights'],
            inclusions=data['inclusions'],
            exclusions=data['exclusions'],
            specialty_tour=specialty_tour,
            tour_type=tour_type,
            city=data['city'],
            # category=category,
            is_active=data.get('isActive', 'true') == 'true',
            is_popular=data.get('is_popular', 'true') == 'true',
            show_on_homepage=data.get('show_on_homepage', 'true') == 'true',
        )
        
        db.session.add(new_package)
        print("new_package")        
        print(new_package)
        db.session.flush()  # Get the package ID before committing

        # Process itinerary details
        itinerary_days = [
            key for key in data.keys() if key.startswith("itinerary_day_")
        ]
        print("itinerary_item")
        for day_key in itinerary_days:
            day_number = int(day_key.split("_")[-1])  # Extract day number
            day_description = data[day_key]
            itinerary_item = Itinerary(
                day_description=day_description,
                day_number=day_number,
                package_id=new_package.id
            )
            print(itinerary_item)
            db.session.add(itinerary_item)
        
        db.session.commit()
        return redirect(url_for('get_packages'))

@app.route('/edit-package/<int:id>', methods=['GET', 'POST'])
def edit_package(id):
    package = Package.query.get_or_404(id)
    
    if request.method == 'POST':
        # Update the package details from the form data
        data = request.form
        print("data")
        print(data)
        package.name = data['name']
        package.description = data['description']
        package.duration = data['duration']
        package.images = data['images']
        package.highlights = data['highlights']
        package.inclusions = data['inclusions']
        package.exclusions = data['exclusions']
        package.specialty_tour =  data.get('specialty_tour', '').strip()
        package.tour_type =  data.get('tour_type', '').strip()
        package.city = data['city']
        # package.category = data['category']
        package.is_active = data.get('is_active', 'true') == 'true'
        package.is_popular = data.get('is_popular', 'true') == 'true'
        package.show_on_homepage = data.get('show_on_homepage', 'true') == 'true'
        db.session.commit()
        return redirect(url_for('package_details', package_id=id))
    
    return render_template('edit_package.html', package=package)


@app.route('/delete-package/<int:id>', methods=['POST'])
def delete_package(id):
    # Delete a package
    package = Package.query.get_or_404(id)
    db.session.delete(package)
    db.session.commit()
    # add a flash message
    flash("The package has been deleted successfully.", "success")
    return redirect(url_for('get_packages'))


# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(debug=True)
