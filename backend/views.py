from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth import get_user_model
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from . import verify
from django.db.models.query_utils import Q
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from .forms import(NewUserForm, LoginForm,UpdateForm, 
                   CheckEmailForm,ConfirmPasswordForm, UploadForm,AudioForm,SkillForm)
from .serializers import(ProfileSerializer,AudioSerializer,SkillSerializer)
from .import models
import requests
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
UserModel = get_user_model()
# Create your views here.


class RegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        zip_code = data['zip_code']
        phone = data['phone']
        state = data['state']
        city = data['city']
        password1 = data['password1']
        password2 = data['password2']
        associated_users = models.User.objects.filter(Q(email=email))
        if associated_users:
            return Response("User with the email already exit",status=status.HTTP_400_BAD_REQUEST)
        else:
            if password1 == password2:
                user = models.User.objects.create(first_name=first_name, last_name=last_name, email=email,
                                                 zip_code=zip_code,phone=phone,city=city,state=state,
                                                 password=password1)
                user.set_password(password1)
                user.save()
                return Response("Registration Successfull", status=status.HTTP_201_CREATED)
            else:
                return Response("Password didn't match", status=status.HTTP_400_BAD_REQUEST)

class SigninView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        email = data['email']
        password = data['password']
        if email is None:
            return Response("Please enter email", status=status.HTTP_400_BAD_REQUEST)
        elif password is None:
            return Response("Please enter password", status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            login(request, user)
            content ={
                'token':f"{refresh.access_token}"
            }
            return Response(content,  status=status.HTTP_200_OK)
        return Response("Invalid username or password", status=status.HTTP_400_BAD_REQUEST)
    
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        profile = models.User.objects.get(pk=request.user.id)
        serializer = ProfileSerializer(profile, many=False)
        content = {
            'data':serializer.data
        }
        return Response(content,  status=status.HTTP_200_OK)
    def post(self, request):
        data = request.data
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        zip_code = data['zip_code']
        phone = data['phone']
        city = data['city']
        state = data['state']
        try:
            user = models.User.objects.filter(pk=request.user.id).update(first_name=first_name, last_name=last_name, email=email,
                                                 zip_code=zip_code,phone=phone,city=city,
                                                 state=state)
            return Response("Profile successfully Updated",  status=status.HTTP_200_OK)
        except:
            return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)
    
class CheckEmailView(APIView):
    def post(self, request):
        data = request.data
        email = data['email']
        try:
            userEmail = models.User.objects.get(email = email)
            if userEmail is not None:
                Email = userEmail.email
                request.session['mail']=Email
                name = userEmail.username
                subject = "Password Reset Form"
                email_template_name = "backend/password_reset_email.txt"
                c = {
                "email":Email,
                'domain':'127.0.0.1:8000',
                'site_name': 'IELTS',
                'protocol': 'http',
                "uid": urlsafe_base64_encode(force_bytes(userEmail.pk)),
                "name":name,
                "user": userEmail,
                'token': default_token_generator.make_token(userEmail),

                }
                email = render_to_string(email_template_name, c)
                try:
                    send_mail(subject, email, 'balosod37@gmail.com' , [Email], fail_silently=False)
                except BadHeaderError:
                    return Response("Invalid header found", status=status.HTTP_400_BAD_REQUEST)
                return Response("Password Reset Form Sent to Your Email", status=status.HTTP_200_OK)
        except:
            return Response("Wrong Email Address", status=status.HTTP_400_BAD_REQUEST)
        
class PasswordResetView(APIView):
    def get(self,request,uidb64,token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError):
            user = None
        if user is not None and default_token_generator.check_token(user,token):
            return Response("User confirm redirect him to password reset form", status=status.HTTP_200_OK)
            #return redirect('/password_confirm/')
        return HttpResponse("Token Expired", status=400)
    
class PasswordConfirmView(APIView):
    def post(self, request):
        data = request.data
        password = data['password']
        confirm_password = data['confirm_password']
        if password == confirm_password:
            Email = request.session['mail']
            user = UserModel._default_manager.get(email=Email)
            user.set_password(password)
            user.save()
            return Response("password reset successfully", status=status.HTTP_200_OK)
        else:
            return Response("Password does not match", status=status.HTTP_400_BAD_REQUEST)
class UploadView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        data = request.data
        essay = data['essay']
        try:
            userEmail = models.User.objects.get(email = request.user.email)
            if userEmail is not None:
                Email = userEmail.email
                first_name = userEmail.first_name
                last_name = userEmail.last_name
                subject = "Submitted Easay"
                email_template_name = "backend/essay.txt"
                c = {
                "essay":essay,
                "email":Email,
                "first_name":first_name,
                "last_name":last_name
                }
                email = render_to_string(email_template_name, c)
                try:
                    send_mail(subject, email, 'sodiqb86@gmail.com' , ['sodiqb86@gmail.com'], fail_silently=False)
                except BadHeaderError:
                    return Response("Invalid header found", status=status.HTTP_400_BAD_REQUEST)
                return Response("Essay sent", status=status.HTTP_200_OK)
        except:
            return HttpResponse("Something went wrong", status=400)
        
class AudioView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        record = data['record']
        owner = models.User.objects.get(email =request.user.email)
        serializer = AudioSerializer(data = request.data)
        if serializer.is_valid():
            models.Audio_store.objects.create(record=record, owner=owner)
            AudioUrl = f"media/audios/{record}"
            try:
                userEmail = models.User.objects.get(email = request.user.email)
                if userEmail is not None:
                    Email = userEmail.email
                    first_name = userEmail.first_name
                    last_name = userEmail.last_name
                    subject = "Submitted Audio"
                    email_template_name = "backend/audio.txt"
                    c = {
                    'domain':'127.0.0.1:8000/',
                    "email":Email,
                    "first_name":first_name,
                    "last_name":last_name,
                    'protocol': 'http',
                    "url": AudioUrl,
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'sodiqb86@gmail.com' , ['sodiqb86@gmail.com'], fail_silently=False)
                    except BadHeaderError:
                        return Response("Invalid header found.", status=status.HTTP_400_BAD_REQUEST)
                    return Response("Audio Uploaded", status=status.HTTP_200_OK)
            except:
                return Response("Wrong Email Address", status=status.HTTP_400_BAD_REQUEST)
        return Response('error',status=status.HTTP_400_BAD_REQUEST)

class SkillView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        price = data['amount']
        package = data['package']
        email = request.user.email
        owner = models.User.objects.get(email =email)
        new_price = int(price)
        url = "https://api.paystack.co/transaction/initialize"
        payload = {"email": email, "amount" : new_price * 100, "first_name" : email}
        headers = {"Authorization":os.environ['PAYSTACK_AUTHORIZATION_KEY']}
        try:
            skill_exist = models.Skill.objects.filter(user_skill=owner.id).get(package=package)
            return Response("You have Already buy this package", status=status.HTTP_200_OK)
        except:
            request.session['price'] = price
            response =  requests.post(url, headers = headers,data = payload)
            Json_Response = response.json()
            payment_url = Json_Response["data"]["authorization_url"]
            reference = Json_Response['data']['reference']
            request.session['ref'] = reference
            request.session['package'] = package
            content ={
                'authorization url':f"{payment_url}"
            }
            return Response(content, status=status.HTTP_200_OK)

class SkillVerifyView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        email = request.user.email
        reference = request.session['ref']
        user_id = models.User.objects.get(email=email)
        if reference == '':
            skill = models.Skill.objects.filter(user_skill=user_id)
            serializer = SkillSerializer(skill, many=True)
            content = {
                'data':serializer.data
            }
            return Response(content,  status=status.HTTP_200_OK) 
        if reference:
            if verify.payment(reference) ==  'success':
                request.session['ref'] = ''
                price = request.session['price']
                package = request.session['package']
                user = models.User.objects.get(email=request.user.email)
                bought_package = models.Skill.objects.create(package=package,amount=price,user_skill=user)
                bought_package.save()
                skill = models.Skill.objects.filter(user_skill=user_id)
                serializer = SkillSerializer(skill, many=True)
                content = {
                'data':serializer.data
                }
                return Response(content,  status=status.HTTP_200_OK)
            else:
                skill = models.Skill.objects.filter(user_skill=user_id)
                serializer = SkillSerializer(skill, many=True)
                content = {'data':serializer.data}
                return Response(content,  status=status.HTTP_200_OK)  
                