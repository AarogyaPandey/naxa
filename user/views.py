from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from django.contrib.auth.models import User


class SignUp(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.create_user(username= username, password=password)
        
        if user is not None:
            return Response("User created successfully!")
        return Response("Incorrect email or password")

@api_view(["POST"])
def postapi(request):
    user = authenticate(username =request.data["username"], password = request.data["password"] )
    print(user)
    if user:
        token = Token.objects.get_or_create(user=user)
        return Response({"token": token.key,
                         "user_id":user.id,})
    else:
        return Response({"error": "Invalid credentials"}, status=401)



