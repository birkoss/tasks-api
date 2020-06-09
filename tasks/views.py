from django.http import HttpResponse
from django.shortcuts import render

from exponent_server_sdk import DeviceNotRegisteredError
from requests.exceptions import HTTPError
from requests.exceptions import ConnectionError
from exponent_server_sdk import PushServerError
from exponent_server_sdk import PushResponseError
from exponent_server_sdk import PushMessage
from exponent_server_sdk import PushClient

from users.models import User


def test(request):

    user = User.objects.filter(pk=request.user.pk).first()

    print(user.expo_token)
    send_push_message(
        user.expo_token, "You have new tasks waiting to be selected")

    return HttpResponse("ok")

# Basic arguments. You should extend this function with the push features you
# want to use, or simply pass in a `PushMessage` object.


def send_push_message(token, message, extra=None):
    try:
        response = PushClient().publish(
            PushMessage(to=token,
                        body=message,
                        data=extra))
    except PushServerError as exc:
        print("ERROR")
        # Encountered some likely formatting/validation error.
        rollbar.report_exc_info(
            extra_data={
                'token': token,
                'message': message,
                'extra': extra,
                'errors': exc.errors,
                'response_data': exc.response_data,
            })
        raise
    except (ConnectionError, HTTPError) as exc:
        print("ERROR")
        # Encountered some Connection or HTTP error - retry a few times in
        # case it is transient.
        rollbar.report_exc_info(
            extra_data={'token': token, 'message': message, 'extra': extra})
        raise self.retry(exc=exc)

    try:
        # We got a response back, but we don't know whether it's an error yet.
        # This call raises errors so we can handle them with normal exception
        # flows.
        response.validate_response()
    except DeviceNotRegisteredError:
        print("ERROR")
        # Mark the push token as inactive
        from notifications.models import PushToken
        PushToken.objects.filter(token=token).update(active=False)
    except PushResponseError as exc:
        print("ERROR")
        # Encountered some other per-notification error.
        rollbar.report_exc_info(
            extra_data={
                'token': token,
                'message': message,
                'extra': extra,
                'push_response': exc.push_response._asdict(),
            })
        raise self.retry(exc=exc)
