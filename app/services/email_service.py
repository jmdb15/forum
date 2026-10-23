from fastapi_mail import FastMail, MessageSchema, MessageType

from app.core.settings import settings


async def send_welcome_email(
        email: str,
        name: str,
) -> None:
    print(f"Sending Email to {name}({email})")
    message = MessageSchema(
        subject=f"Welcome {name}",
        recipients=[email],
        body=f"""
            <h1>Hello {name},</h1>

            <h3>Welcome sa'yo <span style="color: red;">kaibigan</span>. Enjoy!</h3>
        """,
        subtype=MessageType.html
    )

    mailer = FastMail(settings.mail_config)
    await mailer.send_message(message)
