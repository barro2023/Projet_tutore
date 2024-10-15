from flask_mail import Mail, Message
from app import create_app

app = create_app()
mail = Mail(app)

def send_notification(to, ad):
    msg = Message("Nouvelle annonce correspondante à vos préférences",
                  sender="tiomokobaarro@gmail.com",
                  recipients=[to])
    msg.body = f"Il y a une nouvelle annonce correspondant à vos critères :\n\n{ad.type}\n{ad.price}\n{ad.location}\n{ad.url}"
    mail.send(msg)
