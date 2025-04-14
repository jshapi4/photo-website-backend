import os
import requests

def test_mailgun_send():
    domain = os.environ.get("MAILGUN_DOMAIN")
    api_key = os.environ.get("MAILGUN_API_KEY")

    if not domain or not api_key:
        return "Missing MAILGUN_DOMAIN or MAILGUN_API_KEY"

    try:
        response = requests.post(
            f"https://api.mailgun.net/v3/{domain}/messages",
            auth=("api", api_key),
            data={
                "from": f"Mailgun Test <postmaster@{domain}>",
                "to": ["joeladamshapiro@gmail.com"],
                "subject": "Mailgun Test Email",
                "text": "This is a test email sent from the Mailgun API via Django!",
            },
        )
        response.raise_for_status()
        return f"✅ Test email sent successfully! Status: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"❌ Failed to send test email: {e}"
