from django.middleware import csrf
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Product
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import  api_view, action
from rest_framework.response import Response
from .serializers import (
    UserSerializer,
    LoginSerializer,
    RegisterSerializer,
    ProductSerializer
)
from .data_generator import generate_random_products

# Create your views here.

@api_view(['GET'])
def generate_csrf_token(request):
    csrftoken = csrf.get_token(request)
    return Response({"csrftoken": csrftoken})

def set_session(request, user, remember_user=False):
    session_id = request.session._get_or_create_session_key()
    session_store = SessionStore(session_key=session_id)
    session_store["user"] = user.user_id
    session_store["email"] = user.email
    session_store["marked_products"] = []
    session_store.save()

    if remember_user:
        expiry = 2592000
    else:
        expiry = 0

    return session_store.session_key,
        


class AuthViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    @action(detail=False, methods=["post"])
    def register(self, request):
        register_serializer = RegisterSerializer()
        user = register_serializer.validate(data=request.data)
        session_id = set_session(request, user)
        return Response({'sessionid': session_id})
    
    @action(detail=False, methods=["post"])
    def login(self, request):
        remember_user = request.data.get("remember_user", False)
        login_serializer = LoginSerializer()
        user = login_serializer.validate(data=request.data)
        session_id = set_session(request, user, remember_user)
        return Response({'sessionid': session_id})

    @action(detail=False, methods=["post"])
    def logout(self, request):
        request.session.flush()
        return Response({"message": "logged out successfully"})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=["get"])
    def currently_logged_in(self, request):
        if request.session.get('user'):
            return Response({"user": request.session.get('user'), "email": request.session.get('email')})
        
        return Response({"message": "session not found"}, status=status.HTTP_400_BAD_REQUEST)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=["get"])
    def search(self, request):
        marked_products = request.session.get('marked_products', [])
        search_string = request.query_params.get('search', '')
        products = list(self.get_queryset().filter(Q(product_id__icontains=search_string) | Q(name__contains=search_string)).values())
        products = [dict(product, **{'is_marked': True}) if product['product_id'] in marked_products else dict(product, **{'is_marked': False}) for product in products]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["get"])
    def marked_products(self, request):
        marked_products = request.session.get('marked_products', [])
        products = self.get_queryset().filter(product_id__in=marked_products)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["post"])
    def mark_product(self, request):
        marked_products = request.session.get('marked_products', [])
        marker = request.data.get('marker', 'off')
        product = request.data.get('product', None)
        print(marker, product)
        if product is not None:
            if product in marked_products and marker == 'off':
                marked_products.remove(product)
            elif marker == 'on':
                marked_products.append(product)
        
        request.session['marked_products'] = marked_products
        request.session.save()
        return Response({"message": "marked products updated"})
    
    @action(detail=False, methods=["post"])
    def generate_data(self, request):
        products = generate_random_products()
        products_created = Product.objects.bulk_create(
		    [Product(**product) for product in products], batch_size=100
	    )
        return Response({"message": "data successfully genrated"})


# router = Router()


# def ensure_logged_in(func):
#     @wraps(func)
#     def wrapper(request, *args, **kwargs):
#         if request.session.get("user") is not None:
#             return func(request, *args, **kwargs)

#         raise SessionUnavailableError()

#     return wrapper


# def ensure_not_logged_in(func):
#     @wraps(func)
#     def wrapper(request, *args, **kwargs):
#         if request.session.get("user") is None:
#             return func(request, *args, **kwargs)

#         raise SessionAvailableError()

#     return wrapper



# class UserIn(ModelSchema):
#     class Config:
#         model = User
#         model_exclude = [
#             "user_id",
#             "username",
#             "is_active",
#             "is_verified",
#             "created_at",
#             "updated_at",
#         ]
#         model_fields_optional = ["phone"]


# class UserOut(Schema):
#     id: int
#     username: str


# class Error(Schema):
#     field: str
#     message: str


# @router.post("/register", response={201: UserOut, 400: Error})
# @ensure_not_logged_in
# def register(request, response: HttpResponse, data: UserIn):
#     encrypted_password = make_password(data.dict().pop("password"))
#     data.dict()["password"] = encrypted_password
#     user = User.objects.filter(email=data.dict().pop("email"))
#     if user.exists():
#         return 400, {
#             "field": "email",
#             "message": "User with this email address already exists",
#         }
#     data.dict()["username"] = ""
#     user = User.objects.create(**data.dict())
#     set_session(request, response, user)
#     return 201, {"id": user.user_id, "username": user.username}


# @router.post("/login")
# def login(request):
#     print(request.COOKIES)
#     print(request.session.get("user"))
#     # Retrieve the session ID from somewhere (e.g., request parameters, database, etc.)
#     session_id = request.session._get_or_create_session_key()
#     print(session_id)

#     # Create a new session store
#     session_store = SessionStore(session_key=session_id)

#     session_store["user"] = 2
#     session_store.set_expiry(2592000)
#     session_store.save()

#     sessionid = session_store.session_key

#     # Set the session ID on the response object
#     response = JsonResponse({"message": "session id set"})

#     response.set_cookie(
#         "sessionid",
#         sessionid,
#         httponly=True,
#         samesite="None",
#         secure=True,
#         max_age=2592000,
#     )
#     return response


# @router.post("/get-session-id")
# def get_session_id(request):
#     print(request.COOKIES)
#     print(request.session.get("user"))
#     # Retrieve the session ID from somewhere (e.g., request parameters, database, etc.)
#     session_id = request.session._get_or_create_session_key()
#     print(session_id)

#     # Create a new session store
#     session_store = SessionStore(session_key=session_id)

#     # Set the session ID on the response object
#     response = JsonResponse({"message": session_store.session_key})

#     return response
