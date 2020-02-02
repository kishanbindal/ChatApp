import json
import logging
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Account
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserForgotPassordSerializer
from Services.account_services import UserFunctions
from Services.cache_services import Redis
from Services.token_services import Generatetoken
from Services.mail_services import MailServices

logging.basicConfig(level=logging.DEBUG)

rdb = Redis()


class UserRegistrationView(GenericAPIView):

    serializer_class = UserRegistrationSerializer

    def post(self, request):

        serializer = UserRegistrationSerializer(data=request.data)
        smd = {
            'success': 'fail',
            'message': 'Failed To Register User',
            'data': []
        }

        try:

            if serializer.is_valid():

                user_info = UserFunctions(request)
                username, email, password = user_info.get_reg_data()
                if Account.objects.filer(email=email).exists() or Account.objects.filter(username=username):
                    smd['message'] = 'Email already exists, Please Login'
                    return Response(data=smd, status=status.HTTP_208_ALREADY_REPORTED)
                user = Account.objects.create_user(username, email, password)
                user.is_active = False
                token = Generatetoken().registration_token(username, email)
                logging.info('---- token--->', token)
                # token = "".join(chr(x) for x in bytearray(token))
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
            return Response(data=smd, status=status.HTTP_404_NOT_FOUND)

def activate(self, token):

    try:

        payload = Generatetoken().decode_token(token)
        username = payload.get('username')
        user = Account.objects.get(username=username)
        smd = {'success': 'fail', 'message': 'Unable to Activate Account', 'data': []}

        if user:
            user.is_active = True
            smd['success'], smd['message'], smd['data'] = 'Success', 'Account Successfully activated', [user.username]
            return JsonResponse(data=smd, status=status.HTTP_200_OK)
        return Response(data=smd, status=status.HTTP_400_BAD_REQUEST)

    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response(e, status=status.HTTP_404_NOT_FOUND)


class UserLoginView(GenericAPIView):

    serializer_class = UserLoginSerializer

    def post(self, request):

        serializer = UserLoginSerializer(data=request.data)
        smd = {
            'success': 'Fail',
            'message': 'Unable to Login',
            'data': []
        }

        try:
            if serializer.is_valid():

                email, password = UserFunctions(request).get_login_data()
                user = Account.objects.get(email=email)
                if user is not None and user.is_active:
                    logging.info('Successfully logged in')
                    token = Generatetoken().login_token(user.pk)
                    # token = "".join(chr(x) for x in bytearray(token))
                    smd['success'], smd['message'], smd['data'] = 'Success', f'Successfully logged in as {user.username}', \
                                                                  [token]
                    rdb.set(user.pk, token)
                    return Response(data=smd, status=status.HTTP_200_OK)
                else:
                    logging.info('User Does Not Exist or is not active')
                    return Response(data=smd, status=status.HTTP_400_BAD_REQUEST)
            else:
                logging.info('Ivalid Serializer')
                smd['data'] = ["Invalid Serializer"]
                return Response(data=smd, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.info(Exception)
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserLogOutView(APIView):

    def post(self, request):

        token = request.headers.get('token')
        payload = Generatetoken().decode_token(token)
        user_id = payload.get('id')
        logging.info(f'USER ID FROM TOKEN : {token}')
        rdb.delete(user_id)
        smd = {'success': 'Success', 'message': 'User Logged Out', 'data': []}
        return Response(data=smd, status=status.HTTP_200_OK)


class UserForgotPasswordView(GenericAPIView):

    serializer_class = UserForgotPassordSerializer

    def post(self, request):

        serializer = UserForgotPassordSerializer(data=request.data)

        smd = {'success': 'fail', 'message': 'User Not Found', 'data': []}

        try:
            import pdb
            pdb.set_trace()

            if serializer.is_valid():
                email = UserFunctions(request).get_forgot_password_data()
                user = Account.objects.get(email=email)
                if user is not None:
                    token = Generatetoken().login_token(user.pk)
                    logging.info(f'Forgot Password Token ---> {token}')
                    MailServices().send_forgot_password_email(request, email, token)
                    logging.info(f'Mail sent Successfully to {email}')
                    smd = {'success': 'Success', 'message': f'Reset mail sent successfully to {email}', 'data': []}
                    return JsonResponse(data=smd, status=status.HTTP_200_OK)
                else:
                    logging.info('User not found')
                    return Response(data=smd, status=status.HTTP_404_NOT_FOUND)
            logging.info(f'Invalid Serializer')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND)


def reset(request, token):

    try:

        import pdb
        pdb.set_trace()
        payload = Generatetoken().decode_token(token)
        user_id = payload.get('id')
        user = Account.objects.get(pk=user_id)
        smd = {'success': 'fail', 'message': 'Unable to Reset Password', 'data': []}

        if user:
            request_data = json.loads(request.body)
            new_password = request_data.get('new_password')
            user.set_password(new_password)
            smd['success'], smd['message'] = 'Success', 'Successfully reset password'
            return JsonResponse(data=smd, status=status.HTTP_200_OK)
        return Response(data=smd, status=status.HTTP_400_BAD_REQUEST)

    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response(e, status=status.HTTP_404_NOT_FOUND)
