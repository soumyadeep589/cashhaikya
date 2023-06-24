from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice


def notify(title, body):

    message = Message(
        notification=Notification(title=title, body=body),
    )
    device = FCMDevice.objects.all()
    # send_message parameters include: message, dry_run, app
    device.send_message(message)
