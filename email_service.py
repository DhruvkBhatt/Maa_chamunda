from flask_mail import Mail, Message

from flask_mail import Message

admin_email = None
def create_admin_email_body(booking_type, **kwargs):
    """
    Generates the email body for admin based on the booking type.
    """
    try:
        if booking_type == "hotel booking":
            body = f"""
            New {booking_type} request received:

            Name: {kwargs.get('name')}
            Email: {kwargs.get('email')}
            Contact No: {kwargs.get('contact')}
            Location: {kwargs.get('location')}
            Check-in Date: {kwargs.get('checkin')}
            Check-out Date: {kwargs.get('checkout')}
            Number of Rooms: {kwargs.get('rooms')}
            Adults: {kwargs.get('adults')}
            Children: {kwargs.get('children')}
            Special Requests: {kwargs.get('message')}
            """
        elif booking_type.lower() in ["train booking", "bus booking"]:
            body = f"""
            New {booking_type} request received:

            Name: {kwargs.get('name')}
            Email: {kwargs.get('email')}
            Contact No: {kwargs.get('contact')}
            From: {kwargs.get('From')}
            To: {kwargs.get('To')}
            Departure Date: {kwargs.get('departure_date')}
            """
        else:
            body = "Booking details not available."
        return body
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while processing the booking details."


def create_client_ack_body(name, booking_type="Enquiry"):
    """
    Generates the acknowledgment email body for the client.
    """
    return f"""
    Dear {name},

    Thank you for choosing Maa Chamunda Tours & Travels. Your {booking_type} request has been received. 
    Our team will contact you shortly to finalize the details.

    Best regards,  
    Maa Chamunda Tours & Travels Team
    """


def send_admin_email(mail, booking_type="Enquiry", **kwargs):
    """
    Sends an email to the admin with booking details.
    """
    admin_email = mail.app.config['MAIL_USERNAME']
    subject = f"New {booking_type.capitalize()} Request"
    body = create_admin_email_body(booking_type, **kwargs)
    admin_msg = Message(subject, sender=mail.app.config['MAIL_USERNAME'], recipients=[admin_email])
    admin_msg.body = body
    mail.send(admin_msg)


def send_client_acknowledgment(mail, client_email, name, booking_type="Enquiry"):
    """
    Sends an acknowledgment email to the client confirming their booking request.
    """
    subject = f"Thank You for Your {booking_type.capitalize()} Request"
    body = create_client_ack_body(name, booking_type)
    client_msg = Message(subject, sender=mail.app.config['MAIL_USERNAME'], recipients=[client_email])
    client_msg.body = body
    mail.send(client_msg)
