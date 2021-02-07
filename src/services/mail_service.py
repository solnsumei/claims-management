from typing import List
from pydantic import EmailStr
from fastapi_mail import FastMail, MessageSchema
from src.config.mail_config import MAIL_CONFIG


mail_service = FastMail(MAIL_CONFIG)


def create_welcome_message(name: str, email: List[EmailStr], password: str) -> MessageSchema:
    """

    :rtype: object
    """
    html = f"""
        <h3>Hello {name}</h3>
        <p>
            Your email {email[0]} have been registered on our platform by the admin. <br /> <br />
            Your default password is {password}, you will have to change it on first login.
            <br /> </br /> Thanks for using our platform. <br /><br /> Cheers
        </p>
    """

    return MessageSchema(
        subject="Welcome to Our Platform",
        recipients=email,
        body=html,
        subtype="html"
    )