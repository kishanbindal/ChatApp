import logging
from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .models import Account
from .serializers import UserRegistrationSerializer
from Services.account_services import UserFunctions
from Services.token_services import Generatetoken
from Services.mail_services import MailServices

logging.basicConfig(level=logging.DEBUG)


class UserRegistrationView(GenericAPIView):

    serializer_class = UserRegistrationSerializer
    queryset = Account.objects.all()

    def post(self, request, *args, **kwargs):

        serializer = UserRegistrationSerializer(data=request.data)
        smd = {
            'success': 'fail',
            'message': 'Failed To Register User',
            'data': []
        }
        try:
            import pdb
            pdb.set_trace()

            if serializer.is_valid():

                user_info = UserFunctions(request)
                username, email, password = user_info.get_reg_data()
                if self.queryset.filter(email=email).exists() or self.queryset.filter(username=username):
                    smd['message'] = 'Email already exists, Please Login'
                    return Response(data=smd, status=status.HTTP_208_ALREADY_REPORTED)
                user = Account.objects.create_user(username, email, password)
                user.is_active = False
                token = Generatetoken().registration_token(username, email)
                MailServices().send_registration_email(request, user, 'kishan.bindal@gmail.com', token)
                smd['success'], smd['message'] = 'success', 'Successfully registered User. Active link sent to email'
                return Response(data=smd, status=status.HTTP_201_CREATED)

            else:
                logging.debug('Serializer is Invalid')
                logging.debug(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ValueError:
            return Response(data=smd, status=status.HTTP_406_NOT_ACCEPTABLE)
        except TypeError:
            return Response(data=smd, status=status.HTTP_406_NOT_ACCEPTABLE)

        except Exception:
            logging.debug(Exception)
            return Response(data=smd, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
