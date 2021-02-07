from typing import List
from pydantic import EmailStr, BaseModel
from fastapi_mail import FastMail, MessageSchema
from src.config.mail_config import MAIL_CONFIG


mail_service = FastMail(MAIL_CONFIG)


class WelcomeMessageSchema(BaseModel):
    name: str
    email: List[EmailStr]
    password: str


def create_welcome_message(welcome_schema: WelcomeMessageSchema) -> MessageSchema:
    html = f"""
        <h3>Hello {welcome_schema.name}</h3>
        <p>
            Your {welcome_schema.email} have been registered on our platform by the admin. <br />
            Your default password is {welcome_schema.password}, you will have to change it on first login.
            <br /> Thanks for using our platform. <br /> Cheers
        </p>
    """

    return MessageSchema(
        subject="Welcome to Our Platform",
        recipients=welcome_schema.email,
        body=html,
        subtype="html"
    )