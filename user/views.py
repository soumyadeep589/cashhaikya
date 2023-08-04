import random
import requests
import structlog
from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta

# from .validators import validate_duplicate_user, validate_password
from .models import CustomUser
from .utils import json_error, json_success
from .serializer import UserSerializer
from cashhaikya.settings import FAST_2_SMS_API_KEY
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict


structlog.dev.ConsoleRenderer(
    pad_event=30,
    colors=True,
    force_colors=True,
    repr_native_str=False,
    level_styles=None,
)
logger = structlog.get_logger(__name__)


class Register(APIView):
    """
    for registering customer
    """

    def post(self, request):
        data = request.data

        if not data.get("phone"):
            return json_error("phone is mandatory")
        if not data.get("name"):
            return json_error("name is mandatory")

        try:
            phone = data["phone"]
            name = data["name"]
            otp = random.randrange(100000, 999999)
            otp_expiration_date = timezone.now() + timedelta(minutes=1)
            if CustomUser.objects.filter(phone=phone, is_active=True).exists():
                return json_error("User already present with this phone, try login")
            user = CustomUser.objects.create(phone=phone, name=name)
            user.otp = str(otp)
            user.otp_expiration_date = otp_expiration_date
            user.save()
            logger.info("otp saved to customer successfully")
            url = (
                f"https://www.fast2sms.com/dev/bulkV2?authorization="
                f"{FAST_2_SMS_API_KEY}&variables_values={otp}&route=otp"
                f"&numbers={phone}&flash=0"
            )
            response = requests.get(url)
            logger.info("otp sent successfully")
        except Exception as e:
            logger.error("something went wrong: " + str(e))
            return json_error("something went wrong" + str(e), status=500)

        return json_success(response.json()["message"])


class Login(APIView):
    """
    for login customer
    """

    def post(self, request):
        data = request.data

        if not data.get("phone"):
            return json_error("phone is mandatory")

        try:
            phone = data["phone"]
            otp = random.randrange(100000, 999999)
            otp_expiration_date = timezone.now() + timedelta(minutes=1)
            if not CustomUser.objects.filter(phone=phone).exists():
                return json_error("User not present with this phone, try register")
            user = CustomUser.objects.get(
                phone=phone,
            )
            user.otp = str(otp)
            user.otp_expiration_date = otp_expiration_date
            user.save()
            logger.info("otp saved to customer successfully")
            url = (
                f"https://www.fast2sms.com/dev/bulkV2?authorization="
                f"{FAST_2_SMS_API_KEY}&variables_values={otp}&route=otp"
                f"&numbers={phone}&flash=0"
            )
            response = requests.get(url)
            logger.info("otp sent successfully")
        except Exception as e:
            logger.error("something went wrong: " + str(e))
            return json_error("something went wrong" + str(e), status=500)

        return json_success(response.json()["message"])


# class GenerateOTP(APIView):
#     """
#     for creating customer
#     """
#
#     def post(self, request):
#         data = request.data
#
#         if not data.get("phone"):
#             return json_error("phone is mandatory")
#
#         try:
#             phone = data["phone"]
#             otp = random.randrange(100000, 999999)
#             user, _ = CustomUser.objects.get_or_create(
#                 phone=data["phone"],
#             )
#             user.otp = str(otp)
#             user.save()
#             logger.info("otp saved to customer successfully")
#             url = (
#                 f"https://www.fast2sms.com/dev/bulkV2?authorization="
#                 f"{FAST_2_SMS_API_KEY}&variables_values=for cashaikya is {str(otp)}&route=otp"
#                 f"&numbers={phone}"
#             )
#             response = requests.get(url)
#             logger.info("otp sent successfully")
#         except Exception as e:
#             logger.error("something went wrong: " + str(e))
#             return json_error("something went wrong" + str(e), status=500)
#
#         return json_success(response.json()["message"])


class VerifyOTP(APIView):
    def post(self, request):
        data = request.data

        if not data.get("phone"):
            return json_error("phone is mandatory")
        if not data.get("otp"):
            return json_error("otp is mandatory")

        try:
            user = CustomUser.objects.get(phone=data["phone"], otp=data["otp"])
            if user.is_otp_expired():
                return json_error("OTP expired, please retry")
        except CustomUser.DoesNotExist:
            logger.error("Invalid OTP")
            return json_error("Invalid OTP")
        except Exception as e:
            logger.error("something went wrong" + str(e))
            return json_error("something went wrong" + str(e), 500)

        token, _ = Token.objects.get_or_create(user=user)
        return json_success({"token": token.key})


class UserInfo(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return json_success(serializer.data)


class Logout(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = request.auth
        if token:
            token.delete()

        return json_success("Logout successful")

