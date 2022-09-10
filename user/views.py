import random
import requests
import structlog
from rest_framework.views import APIView

# from .validators import validate_duplicate_user, validate_password
from .models import CustomUser
from .utils import json_error, json_success
from cashhaikya.settings import FAST_2_SMS_API_KEY
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


structlog.dev.ConsoleRenderer(
    pad_event=30,
    colors=True,
    force_colors=True,
    repr_native_str=False,
    level_styles=None,
)
logger = structlog.get_logger(__name__)


class GenerateOTP(APIView):
    """
    for creating customer
    """

    def post(self, request):
        data = request.data

        if not data.get("phone"):
            return json_error("phone is mandatory")

        try:
            phone = data["phone"]
            otp = random.randrange(100000, 999999)
            user, _ = CustomUser.objects.get_or_create(
                phone=data["phone"],
            )
            user.otp = str(otp)
            user.save()
            logger.info("otp saved to customer successfully")
            url = (
                f"https://www.fast2sms.com/dev/bulkV2?authorization="
                f"{FAST_2_SMS_API_KEY}&variables_values=for cashaikya is {str(otp)}&route=otp"
                f"&numbers={phone}"
            )
            response = requests.get(url)
            logger.info("otp sent successfully")
        except Exception as e:
            logger.error("something went wrong: " + str(e))
            return json_error("something went wrong" + str(e), status=500)

        return json_success(response.json()["message"])


class VerifyOTP(APIView):
    def post(self, request):
        data = request.data

        if not data.get("phone"):
            return json_error("phone is mandatory")
        if not data.get("otp"):
            return json_error("otp is mandatory")

        try:
            user = CustomUser.objects.get(phone=data["phone"], otp=data["otp"])
        except CustomUser.DoesNotExist:
            logger.error("Invalid OTP")
            return json_error("Invalid OTP")
        except Exception as e:
            logger.error("something went wrong" + str(e))
            return json_error("something went wrong" + str(e), 500)

        token = Token.objects.create(user=user)
        return json_success({"token": token.key})


class Test(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        return json_success("authenticated")
