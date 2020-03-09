from django.shortcuts import render,HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.models import User,auth
from userForms.models import Notes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.core.mail import EmailMessage
from django_short_url.views import get_surl
from django_short_url.models import ShortURL as short
from userForms.serializer import UserSerializer,RegisterationFormSerializer,LoginFormFormSerializer,ForgotPasswordFormSerializer
from userForms.serializer import DisplayNoteSerializer,ResetPasswordFormSerializer,CreateNoteSerializer
from userForms.tokens import token_activation
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import mixins
from validate_email import validate_email
from fundooNotes.settings import SECRET_KEY

import jwt

class registerForm(GenericAPIView):
    serializer_class = RegisterationFormSerializer

    def post(self, request):
        try:
            userName = request.data['username']
            email = request.data['email']
            password = request.data['password']
            confirm_password = request.data['confirm_password']

            if userName == "" or email == "" or password == "":
                return Response("You can not put empty fields")
            if password == confirm_password:
                try:
                    validate_email(email)
                    user = User.objects.create_user(
                        username=userName, email=email, password=password)
                    user.save()

                    current_site = get_current_site(request)
                    print("current_sit : ",current_site)
                    domain_name = current_site.domain
                    print("domain_name : ",domain_name)

                    token = token_activation(username=userName,password=password)

                    url = str(token)
                    print("url : ",url)
                    surl = get_surl(url)
                    print("surl : ",surl)

                    z = surl.split('/')
                    print("z : ",z)
                    print("z[2] : ",z[2])

                    mail_subject = "Click link for activating "
                    msg = render_to_string('email_validation.html', {
                        'user': userName,
                        'domain': domain_name,
                        'surl': z[2]
                    })
                    recipients = email
                    print(msg)
                    email = EmailMessage(mail_subject, msg, to=[recipients])
                    email.send()
                    print('confirmation mail sent')
                    return Response('Please confirm your email address to complete the registration')

                except ValidationError:
                    return Response("Email not found")

            else:
                return Response("Password Missmatch")
        
        except IntegrityError:
            return Response("User Already exist")

class loginForm(GenericAPIView):
    serializer_class = LoginFormFormSerializer

    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return Response("Login successfully")

        else:
            return Response("Log in failed")

class forgotPasswordForm(GenericAPIView):
    serializer_class = ForgotPasswordFormSerializer

    def post(self, request):
        email = request.data['email']

        try:
            user = User.objects.filter(email=email)
            if user.count() == 0:
                return Response("Not Found mail in database")
            
            else:
                username = user.values()[0]["username"]
                current_site = get_current_site(request)
                print("current_sit : ",current_site)
                domain_name = current_site.domain
                print("domain_name : ",domain_name)

                token = token_activation(username=username)

                url = str(token)
                print("url : ",url)
                surl = get_surl(url)
                print("surl : ",surl)

                z = surl.split('/')
                print("z : ",z)
                print("z[2] : ",z[2])

                mail_subject = "Click link for activating "
                msg = render_to_string('reset_password.html', {
                    'user': username,
                    'domain': domain_name,
                    'surl': z[2]
                })
                recipients = email
                print(msg)
                email = EmailMessage(mail_subject, msg, to=[recipients])
                email.send()
                print('confirmation mail sent')
                return Response('Please confirm your email address to reset password')

        except KeyError:
            return Response("Key error")

class resetPasswordForm(GenericAPIView):
    serializer_class = ResetPasswordFormSerializer

    def post(self, request):
        username = self.request.user.username
        if username != "":
            password = request.data['password']
            confirm_password = request.data['confirm_password']

            if password == "" or confirm_password == "":
                return Response("you can not put empty field")

            if password == confirm_password:
                user = User.objects.get(username=username)
                user.set_password(password)
                user.save()

                return Response("successfull reset password")

            else:
                return Response("password missmatch")
        
        else:
            return Response("First you have to login")

class createNoteList(GenericAPIView):
    serializer_class = CreateNoteSerializer    
    
    def get(self,request):
        queryset = Notes.objects.filter(user=self.request.user.id)
        seri = DisplayNoteSerializer(queryset,many=True)
        return Response(seri.data)

    def post(self,request):
        title = request.data['title']
        takeNote = request.data['takeNote']
        user_id = User.objects.get(id=self.request.user.id)
        note = Notes.objects.create(user=user_id,title=title,takeNote=takeNote)
        note.save()
        return Response("Note Created")

class UpdateNoteList(GenericAPIView):

    serializer_class = CreateNoteSerializer
    queryset = Notes.objects.all()

    def put(self,request,pk):
        title = request.data['title']
        takeNote = request.data['takeNote']
        print(title)
        print(takeNote)
        user_id = User.objects.get(id=self.request.user.id)
        print(user_id)
        Notes.objects.filter(id=pk).update(title=title)

        return Response('Note updated')

    def delete(self,request, pk):
        try:
            note = Notes.objects.get(id=pk)
            print(note)
            note.delete()

            return Response("Note deleted")

        except Notes.DoesNotExist:
            return Response("Not found")

def activate(request,surl):
    try:
        token_object = short.objects.get(surl=surl)
        token = token_object.lurl
        decode = jwt.decode(token,SECRET_KEY)
        user_name = str(decode['username'])
        
        user = User.objects.get(username=user_name)

        if user is not None:
            # user.is_active = True
            user.save()
            return HttpResponse("successfully activate your account......")

        else:
            return Response("Something went wrong")

    except KeyError:
        return Response("Key Error")

def logout(request):
    print(auth.logout(request))
    return HttpResponse("Logout")