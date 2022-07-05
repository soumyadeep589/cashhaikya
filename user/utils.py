from django.http import JsonResponse
import uuid


def json_success(data):
    return JsonResponse({"error": None, "data": data, "success": True})


def json_error(error, status=400):
    return JsonResponse({"error": error, "data": None, "success": False}, status=status)


def generate_uniq_id():
    return uuid.uuid4().hex[:6].upper()
