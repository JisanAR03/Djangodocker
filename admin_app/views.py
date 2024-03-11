from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from .serializers import UserCreateSerializer, FrontendContentSerializer, MenuSerializer, MenuContentSerializer, Contact_formSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model,authenticate,login as auth_login,logout as auth_logout
from django.shortcuts import get_object_or_404, redirect, render
from .models import FrontendContent, CustomUser, Menu, MenuContent, Contact_form
import logging
import os
from django.conf import settings
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.http import HttpResponseRedirect, HttpResponse



logger = logging.getLogger()


@api_view(['POST'])
def login(request):
    """
    Authenticates the user and generates a token if the credentials are valid.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: The response object containing the token and user information if the login is successful,
                  otherwise an error message.

    """
    user = get_object_or_404(get_user_model(), username=request.data['username'])
    if not user.is_verified:
        return Response({'error': 'Your email is not verified.'}, status=status.HTTP_400_BAD_REQUEST)
    if user.check_password(request.data['password']):
        token, _ = Token.objects.get_or_create(user=user)
        response = {
            'token': token.key,
            'user_type': user.user_type,
            'message': 'Login Successful'
        }
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Wrong Credentials'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def user_type_list_supreme(request):
    """
    Retrieves the list of user types for the supreme admin.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: The response object containing the list of user types if the user is a supreme admin,
                  otherwise an error message.

    """
    if request.user.user_type == 'supreme_admin' and request.user.is_verified:
        user_types = [user_type[0] for user_type in get_user_model().USER_TYPES]
        response = {
            'user_types': user_types,
        }
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)


# change_password by admin

@api_view(['PUT'])
def change_password(request):
    # just get the mail and one key 
    mail = request.data.get('email')
    key = request.data.get('key')
    password = request.data.get('password')
    check_key = "adminaltafjisanadmin"
    if key == check_key:
        user = get_object_or_404(CustomUser, email=mail)
        user.set_password(password)
        user.save()
        return Response({'message': 'Password Changed Successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)



@api_view(['GET'])
def user_type_list(request):
    """
    Retrieves the list of user types.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: The response object containing the list of user types.

    """
    user_types = [user_type[0] for user_type in get_user_model().USER_TYPES]
    response = {
        'user_types': user_types[1:],
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_user(request):
    """
    Creates a new user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: The response object containing a success message if the user is created successfully,
                  otherwise an error message.

    """
    data = request.data.copy()
    data['creator'] = None
    serializer = UserCreateSerializer(data=data)
    if serializer.is_valid():
        if request.data.get('user_type') == 'supreme_admin':
            return Response({'error': 'You do not have permission to create a supreme_admin account.'}, status=status.HTTP_403_FORBIDDEN)
        else:
            serializer.save()
            return Response({'message': 'User Created Successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def create_user_supreme(request):
    """
    Creates a new user by the supreme admin.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: The response object containing a success message if the user is created successfully,
                  otherwise an error message.

    """
    if request.user.user_type == 'supreme_admin' and request.user.is_verified:
        data = request.data.copy()
        data['creator'] = request.user.id
        serializer = UserCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User Created Successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
    

@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def all_user_list(request):
    """
    Retrieves the list of all users.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: The response object containing the list of all users if the user is a supreme admin,
                  otherwise an error message.

    """
    if request.user.user_type == 'supreme_admin' and request.user.is_verified:
        users = UserCreateSerializer(get_user_model().objects.all(), many=True)
        return Response(users.data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def user_edit_page(request, pk):
    """
    Retrieves the user information for editing.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the user.

    Returns:
        Response: The response object containing the user information if the user is a supreme admin,
                  otherwise an error message.

    """
    if request.user.user_type == 'supreme_admin' and request.user.is_verified:
        user = get_object_or_404(get_user_model(), pk=pk)
        serializer = UserCreateSerializer(user)
        response_data = serializer.data.copy()  # Make a mutable copy of the response data
        if response_data['creator']:
            user_creator = get_object_or_404(get_user_model(), pk=response_data['creator'])
            response_data['creator'] = user_creator.username
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def user_edit(request, pk):
    """
    Updates the user information.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the user.

    Returns:
        Response: The response object containing a success message if the user is updated successfully,
                  otherwise an error message.

    """
    print(request.user.user_type)
    print(request.user.is_verified)
    if request.user.user_type == 'supreme_admin' and request.user.is_verified:
        user = get_object_or_404(get_user_model(), pk=pk)
        print(request.data)
        serializer = UserCreateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User Updated Successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def user_delete(request, pk):
    """
    Deletes a user.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the user.

    Returns:
        Response: The response object containing a success message if the user is deleted successfully,
                  otherwise an error message.

    """
    if request.user.user_type == 'supreme_admin' and request.user.is_verified:
        if pk == request.user.id:
            return Response({'error': 'You can not delete yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(get_user_model(), pk=pk)
        user.delete()
        return Response({'message': 'User Deleted Successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def logged_user_type(request):
    """ return user type of logged in user """
    response = {
        'user_type': request.user.user_type,
    }
    return Response(response, status=status.HTTP_200_OK)

# at here content writer part is start
@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def content_options(request):
    """ return content options """
    if request.user.user_type == 'content_writer' or request.user.user_type == 'content_writer_admin' or request.user.user_type == 'supreme_admin' and request.user.is_verified:
        content_options = [content_option[0] for content_option in FrontendContent.CONTENT_TYPES]
        title_options = [title_option[0] for title_option in FrontendContent.TITLE_TYPES]
        response = {
            'content_options': content_options,
            'title_options': title_options,
        }
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def create_frontend_content(request):
    if request.user.user_type == 'content_writer' or request.user.user_type == 'content_writer_admin' or request.user.user_type == 'supreme_admin' and request.user.is_verified:
        serializer = FrontendContentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Content Created Successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def edit_frontend_content(request, pk):
    if request.user.user_type == 'content_writer' or request.user.user_type == 'content_writer_admin' or request.user.user_type == 'supreme_admin' and request.user.is_verified:
        content = get_object_or_404(FrontendContent, pk=pk)
        serializer = FrontendContentSerializer(content)
        return Response(serializer.data)
    else:
        return Response({'error': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def update_frontend_content(request, pk):
    print("*"*100)
    print(request.user.user_type)
    print(request.user.is_verified)
    print("*"*100)
    if request.user.user_type == 'content_writer' or request.user.user_type == 'content_writer_admin' or request.user.user_type == 'supreme_admin' and request.user.is_verified:
        content = get_object_or_404(FrontendContent, pk=pk)
        serializer = FrontendContentSerializer(content, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Content Updated Successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
    
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def delete_frontend_content(request, pk):
    if request.user.user_type == 'content_writer_admin' or request.user.user_type == 'supreme_admin' and request.user.is_verified:
        content = get_object_or_404(FrontendContent, pk=pk)
        content.delete()
        return Response({'message': 'Content Deleted Successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
    
    
@api_view(['PUT'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def delete_frontend_content_temp(request, pk):
    if request.user.user_type == 'content_writer' and request.user.is_verified:
        content = get_object_or_404(FrontendContent, pk=pk)
        content.is_deleted = True
        content.save()
        return Response({'message': 'Content Deleted Successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def list_frontend_content(request):
    if request.user.user_type == 'content_writer_admin' or request.user.user_type == 'supreme_admin' and request.user.is_verified:
        contents = FrontendContent.objects.all()
        serializer = FrontendContentSerializer(contents, many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response({'error': 'No Content Found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def list_frontend_content_temp(request):
    if request.user.user_type == 'content_writer' and request.user.is_verified:
        contents = FrontendContent.objects.filter(is_deleted=False)
        serializer = FrontendContentSerializer(contents, many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response({'error': 'No Content Found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
# at here the content pulling part is start

@api_view(['GET'])
def list_frontend_content_hero_section(request):
    # is_deleted can't be true
    contents = FrontendContent.objects.filter(content_type='hero_section',title_type='main_content')
    serializer = FrontendContentSerializer(contents, many=True)
    if serializer.data:
        return Response(serializer.data)
    else:
        return Response({'error': 'No Content Found'},status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def list_frontend_content_hero_section_sub_content(request):
    contents = FrontendContent.objects.filter(content_type='hero_section',title_type='sub_content')
    serializer = FrontendContentSerializer(contents, many=True)
    if serializer.data:
        return Response(serializer.data)
    else:
        return Response({'error': 'No Content Found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def list_frontend_content_about_section(request):
    contents = FrontendContent.objects.filter(content_type='about_section',title_type='main_content')
    serializer = FrontendContentSerializer(contents, many=True)
    if serializer.data:
        return Response(serializer.data)
    else:
        return Response({'error': 'No Content Found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def list_frontend_content_about_section_sub_content(request):
    contents = FrontendContent.objects.filter(content_type='about_section',title_type='sub_content')
    serializer = FrontendContentSerializer(contents, many=True)
    if serializer.data:
        return Response(serializer.data)
    else:
        return Response({'error': 'No Content Found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def list_frontend_content_services_section(request):
    contents = FrontendContent.objects.filter(content_type='services_section',title_type='main_content')
    serializer = FrontendContentSerializer(contents, many=True)
    if serializer.data:
        return Response(serializer.data)
    else:
        return Response({'error': 'No Content Found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def list_frontend_content_services_section_sub_content(request):
    contents = FrontendContent.objects.filter(content_type='services_section',title_type='sub_content')
    serializer = FrontendContentSerializer(contents, many=True)
    if serializer.data:
        return Response(serializer.data)
    else:
        return Response({'error': 'No Content Found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def list_frontend_content_blog_section(request):
    contents = FrontendContent.objects.filter(content_type='blog_section',title_type='main_content')
    serializer = FrontendContentSerializer(contents, many=True)
    if serializer.data:
        return Response(serializer.data)
    else:
        return Response({'error': 'No Content Found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def list_frontend_content_blog_section_sub_content(request):
    contents = FrontendContent.objects.filter(content_type='blog_section',title_type='sub_content')
    serializer = FrontendContentSerializer(contents, many=True)
    if serializer.data:
        return Response(serializer.data)
    else:
        return Response({'error': 'No Content Found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def list_frontend_content_projects_section(request):
    contents = FrontendContent.objects.filter(content_type='projects_section',title_type='main_content')
    serializer = FrontendContentSerializer(contents, many=True)
    if serializer.data:
        return Response(serializer.data)
    else:
        return Response({'error': 'No Content Found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def list_frontend_content_projects_section_sub_content(request):
    contents = FrontendContent.objects.filter(content_type='projects_section',title_type='sub_content')
    serializer = FrontendContentSerializer(contents, many=True)
    if serializer.data:
        return Response(serializer.data)
    else:
        return Response({'error':'No Content Found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def list_frontend_content_protfolio_section(request):
    contents = FrontendContent.objects.filter(content_type='protfolio_section',title_type='main_content')
    serializer = FrontendContentSerializer(contents, many=True)
    if serializer.data:
        return Response(serializer.data)
    else:
        return Response({'error':'No Content Found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def list_frontend_content_protfolio_section_sub_content(request):
    contents = FrontendContent.objects.filter(content_type='protfolio_section',title_type='sub_content')
    serializer = FrontendContentSerializer(contents, many=True)
    if serializer.data:
        return Response(serializer.data)
    else:
        return Response({'error':'No Content Found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def list_frontend_content_reviews_section(request):
    contents = FrontendContent.objects.filter(content_type='reviews_section',title_type='main_content')
    serializer = FrontendContentSerializer(contents, many=True)
    if serializer.data:
        return Response(serializer.data)
    else:
        return Response({'error':'No Content Found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def list_frontend_content_reviews_section_sub_content(request):
    contents = FrontendContent.objects.filter(content_type='reviews_section',title_type='sub_content')
    serializer = FrontendContentSerializer(contents, many=True)
    if serializer.data:
        return Response(serializer.data)
    else:
        return Response({'error':'No Content Found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def list_frontend_content_pricing_section(request):
    contents = FrontendContent.objects.filter(content_type='pricing_section',title_type='main_content')
    serializer = FrontendContentSerializer(contents, many=True)
    if serializer.data:
        return Response(serializer.data)
    else:
        return Response({'error':'No Content Found'},status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def list_frontend_content_pricing_section_sub_content(request):
    contents = FrontendContent.objects.filter(content_type='pricing_section',title_type='sub_content')
    serializer = FrontendContentSerializer(contents, many=True)
    if serializer.data:
        return Response(serializer.data)
    else:
        return Response({'error':'No Content Found'},status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def list_frontend_content_team_section(request):
    contents = FrontendContent.objects.filter(content_type='team_section',title_type='main_content')
    serializer = FrontendContentSerializer(contents, many=True)
    if serializer.data:
        return Response(serializer.data)
    else:
        return Response({'error':'No Content Found'},status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def list_frontend_content_team_section_sub_content(request):
    contents = FrontendContent.objects.filter(content_type='team_section',title_type='sub_content')
    serializer = FrontendContentSerializer(contents, many=True)
    if serializer.data:
        return Response(serializer.data)
    else:
        return Response({'error':'No Content Found'},status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def list_frontend_content_contact_section(request):
    contents = FrontendContent.objects.filter(content_type='contact_section',title_type='main_content')
    serializer = FrontendContentSerializer(contents, many=True)
    if serializer.data:
        return Response(serializer.data)
    else:
        return Response({'error':'No Content Found'},status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def list_frontend_content_contact_section_sub_content(request):
    contents = FrontendContent.objects.filter(content_type='contact_section',title_type='sub_content')
    serializer = FrontendContentSerializer(contents, many=True)
    if serializer.data:
        return Response(serializer.data)
    else:
        return Response({'error':'No Content Found'},status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def list_frontend_content_social_links(request):
    contents = FrontendContent.objects.filter(content_type='social_links',title_type='main_content')
    serializer = FrontendContentSerializer(contents, many=True)
    if serializer.data:
        return Response(serializer.data)
    else:
        return Response({'error':'No Content Found'},status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def list_frontend_content_social_links_sub_content(request):
    contents = FrontendContent.objects.filter(content_type='social_links',title_type='sub_content')
    serializer = FrontendContentSerializer(contents, many=True)
    if serializer.data:
        return Response(serializer.data)
    else:
        return Response({'error':'No Content Found'},status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def list_frontend_content_footer_section(request):
    contents = FrontendContent.objects.filter(content_type='footer_section',title_type='main_content')
    serializer = FrontendContentSerializer(contents, many=True)
    if serializer.data:
        return Response(serializer.data)
    else:
        return Response({'error':'No Content Found'},status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def list_frontend_content_footer_section_sub_content(request):
    contents = FrontendContent.objects.filter(content_type='footer_section',title_type='sub_content')
    serializer = FrontendContentSerializer(contents, many=True)
    if serializer.data:
        return Response(serializer.data)
    else:
        return Response({'error':'No Content Found'},status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def verify_email(request):
    # this is verify email function
    if request.GET.get('unique_id'):
        user = get_object_or_404(CustomUser, unique_id=request.GET.get('unique_id'))
        if user.is_verified:
            return Response({'message': 'Your email is already verified.'})
        else:
            user.is_verified = True
            user.save()
            return Response({'message': 'Your email is verified.'})
    else:
        return Response({'error': 'No unique_id found.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def resend_verification_email(request):
    # this is resend verification email function
    try:
        email = request.data.get('email')
        user = get_object_or_404(CustomUser, email=email)
        if user.email_verification_send_count < 5:
            serializer = UserCreateSerializer()
            serializer.send_verification_email(user)
            return Response({'message': 'Verification email resent.'})
        else:
            return Response({'error': 'Verification email resend limit reached.'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'error': 'No email found.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def create_not_admin_user(request):
    ALLOWED_USER_TYPES = ['content_writer_admin', 'ad_manager_admin', 'accountant_admin', 'hr_admin', 'developer_admin', 'data_scientist_admin', 'blogger_admin', 'designer_admin']
    if request.user.user_type in ALLOWED_USER_TYPES and request.user.is_verified:
        data = request.data.copy()
        data['creator'] = request.user.id
        user_type = request.user.user_type
        data['user_type'] = user_type[:-6]
        serializer = UserCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User Created Successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def create_menu(request):
    if request.user.user_type == 'content_writer_admin' or request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin' and request.user.is_verified:
        # also have to pass created_by and it's value is request.user.id
        created_by = request.user.id
        menu_name = request.data.get('menu_name') #required
        if request.data.get('parent_menu') == '':
            parent_menu = None
        else:
            parent_menu = request.data.get('parent_menu')
        if request.data.get('sequence') == '':
            sequence = None
        else:
            sequence = request.data.get('sequence')
        if request.data.get('menu_link') == '':
            menu_link = None
        else:
            menu_link = request.data.get('menu_link')
        if request.data.get('menu_image') == '':
            menu_image = None
        else:
            menu_image = request.data.get('menu_image')
        if request.data.get('menu_title') == '':
            menu_title = None
        else:
            menu_title = request.data.get('menu_title')
        if request.data.get('menu_description') == '':
            menu_description = None
        else:
            menu_description = request.data.get('menu_description')
        if request.data.get('menu_meta_title') == '':
            menu_meta_title = None
        else:
            menu_meta_title = request.data.get('menu_meta_title')
        serializer = MenuSerializer(data={'menu_name': menu_name,'parent_menu': parent_menu,'sequence': sequence,'menu_link': menu_link,'created_by': created_by})
        if serializer.is_valid():
            menu_instance = serializer.save()  # Save and get the instance

            # Now that the menu instance is saved, we can use its id
            menuContentSerializer = MenuContentSerializer(data={'menu_id': menu_instance.id,'image': menu_image,'title': menu_title,'description': menu_description,'meta_title': menu_meta_title})
            if menuContentSerializer.is_valid():
                menuContentSerializer.save()
                return Response({'message': 'Menu Created Successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response(menuContentSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
    

@api_view(['GET'])
def list_menu(request):
    # this is for list all menu and not which is_deleted is true
    menus = Menu.objects.filter(is_deleted=False)
    serializer = MenuSerializer(menus, many=True)
    if serializer.data:
        menu_data = [{'id': menu['id'], 'menu_name': menu['menu_name']} for menu in serializer.data]
        return Response(menu_data)
    else:
        return Response({'error': 'No Menu Found'}, status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['GET'])
def list_all_menu_temp(request):
    menus = Menu.objects.filter(is_deleted=True)
    serializer = MenuSerializer(menus, many=True)
    if serializer.data:
        menu_data = [{'id': menu['id'], 'menu_name': menu['menu_name']} for menu in serializer.data]
        return Response(menu_data)
    else:
        return Response({'error': 'No Menu Found'}, status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def edit_menu(request, pk):
    if request.user.user_type == 'content_writer_admin' or request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin' and request.user.is_verified:
        menu = get_object_or_404(Menu, pk=pk)
        serializer = MenuSerializer(menu)
        menuContentSerializer = MenuContentSerializer(MenuContent.objects.filter(menu_id=pk), many=True)
        menu_data = {
            'menu': serializer.data,
            'menu_content': menuContentSerializer.data
        }
        return Response(menu_data)
    else:
        return Response({'error': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
    
    
@api_view(['PUT'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def update_menu(request, pk):
    print(request.data)
    logger.info(request.user.user_type)
    if request.user.user_type == 'content_writer_admin' or request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin' and request.user.is_verified:
        menu_name = request.data.get('menu_name') #required
        logger.info(request.data.get('parent_menu'))
        if request.data.get('parent_menu') == '' or request.data.get('parent_menu') == None:
            parent_menu = None
        else:
            parent_menu = request.data.get('parent_menu')
        if request.data.get('sequence') == '':
            sequence = None
        else:
            sequence = request.data.get('sequence')
        if request.data.get('menu_link') == '' or request.data.get('menu_link') == None:
            menu_link = None
        else:
            menu_link = request.data.get('menu_link')
        if request.data.get('menu_image') == '' or request.data.get('menu_image') == None:
            menu_content_image = MenuContent.objects.filter(menu_id=pk)
            if menu_content_image:
                if menu_content_image[0].image:
                    menu_image = menu_content_image[0].image
                else:
                    menu_image = None
            else:
                menu_image = None
        else:
            menu_image = request.data.get('menu_image')
        menu_title = request.data.get('menu_title')
        menu_description = request.data.get('menu_description')
        if request.data.get('menu_meta_title') == 'null':
            menu_meta_title = None
        else:
            menu_meta_title = request.data.get('menu_meta_title')
        menu = get_object_or_404(Menu, pk=pk)
        serializer = MenuSerializer(menu, data={'menu_name': menu_name,'parent_menu': parent_menu,'sequence': sequence,'menu_link': menu_link})
        if serializer.is_valid():
            serializer.save()
            menu_content = get_object_or_404(MenuContent, menu_id=pk)
            # if there is not any menu_content then create new one
            if not menu_content:
                menuContentSerializer = MenuContentSerializer(data={'menu_id': pk,'image': menu_image,'title': menu_title,'description': menu_description,'meta_title': menu_meta_title})
                if menuContentSerializer.is_valid():
                    menuContentSerializer.save()
                    return Response({'message': 'Menu Updated Successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response(menuContentSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                menu_content.image = menu_image
                menu_content.title = menu_title
                menu_content.description = menu_description
                menu_content.meta_title = menu_meta_title
                menu_content.save()
                return Response({'message': 'Menu Updated Successfully'}, status=status.HTTP_200_OK)
        else:
            logger.info(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        logger.info("You do not have permission to access this resource.")
        return Response({'error': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
    
    
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def delete_menu(request, pk):
    if request.user.user_type == 'content_writer_admin' or request.user.user_type == 'supreme_admin' and request.user.is_verified:
        menu = get_object_or_404(Menu, pk=pk)
        menu_content = MenuContent.objects.filter(menu_id=pk)
        # delete image too from media this code added for delete image
        menu_image = menu_content[0].image
        if menu_image:
            image_path = os.path.join(settings.MEDIA_ROOT, str(menu_image))
            if os.path.isfile(image_path):
                os.remove(image_path)
        menu_content.delete()
        menu.delete()
        return Response({'message': 'Menu Deleted Successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def delete_menu_temp(request, pk):
    if request.user.user_type == 'content_writer' and request.user.is_verified:
        menu = get_object_or_404(Menu, pk=pk)
        menu.is_deleted = True
        MenuContent.objects.filter(menu_id=pk).update(is_deleted=True)
        menu.save()
        return Response({'message': 'Menu Deleted Successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
    


def get_nested_menus(menu_id):
    sub_menus = Menu.objects.filter(parent_menu=menu_id, is_deleted=False)
    nested_menus = []
    for sub_menu in sub_menus:
        sub_menu_data = {
            'menu_id': sub_menu.id,
            'label': sub_menu.menu_name,
            'url': sub_menu.menu_link,
            'anothersubmenu': get_nested_menus(sub_menu.id)  # Recursive call
        }
        nested_menus.append(sub_menu_data)
    return nested_menus

@api_view(['GET'])
def list_menu_content(request):
    root_menus = Menu.objects.filter(is_deleted=False, parent_menu=None).order_by('sequence')
    menu_data = []
    
    for menu in root_menus:
        menu_data.append({
            'menu_id': menu.id,
            'label': menu.menu_name,
            'url': menu.menu_link,
            'submenu': get_nested_menus(menu.id)  # Use the recursive function
        })
    
    if menu_data:
        return Response(menu_data)
    else:
        return Response({'error': 'No Menu Found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def menu_content_by_menu_link(request, menu_link):
    try:
        menu = get_object_or_404(Menu, menu_link=menu_link)
        serializer = MenuSerializer(menu)
        menuContentSerializer = MenuContentSerializer(MenuContent.objects.filter(menu_id=menu.id), many=True)
        menu_data = {
            'menu_name': serializer.data['menu_name'],
            'menu_title': menuContentSerializer.data[0]['title'],
            'menu_description': menuContentSerializer.data[0]['description'],
            'menu_meta_title': menuContentSerializer.data[0]['meta_title'],
            'menu_image': menuContentSerializer.data[0]['image'],
            'created_at': menuContentSerializer.data[0]['created_at'],
        }
        return Response(menu_data)
    except:
        return Response({'error': 'No Menu Found'}, status=status.HTTP_404_NOT_FOUND)
    
    
    
    
def index(request):
    return render(request, 'index.html')

@api_view(['GET'])
def hero_part(request):
    # return randor title , meta_title and a url as json for a api
    title = "Lorem Ipsum is simply"
    meta_title = "standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make standard dumm"
    url = "https://www.youtube.com/watch?v=t0Q2otsqC4I"
    
    hero_data = {
        'title' : title,
        'meta_title' : meta_title,
        'video_url' : url
    }
    
    return Response(hero_data)

topics = [
        {
            'id': 1,
            'title': 'Lorem Ipsum is simply',
            'menu_link': 'lorem-ipsum-is-simply',
            'meta_title': 'It is a long established fact that a reader will be distracted by the readable content ',
            'description': 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using Content here, content here, making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for lorem ipsum will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).',
            'image': 'https://via.placeholder.com/300',
        },
        {
            'id': 2,
            'title': 'It is a long establishedt',
            'menu_link': 'it-is-a-long-establishedt',
            'meta_title': 'It is a long established fact that a reader will be distracted by the readable content ',
            'description': 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using Content here, content here, making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for lorem ipsum will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).',
            'image': 'https://via.placeholder.com/300',
        },
        {
            'id': 3,
            'title': 'It is a long establishedt',
            'menu_link': 'it-is-a-long-establishedt',
            'meta_title': 'It is a long established fact that a reader will be distracted by the readable content ',
            'description': 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using Content here, content here, making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for lorem ipsum will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).',
            'image': 'https://via.placeholder.com/300',
        }]

@api_view(['GET'])
def all_topics(request):
    # return latest topics as json for a api
    topics_list = [
        {'id': topic['id'], 'title': topic['title'], 'meta_title': topic['meta_title'], 'image': topic['image'], 'menu_link': topic['menu_link']}
        for topic in topics
    ]
    return Response(topics_list)

@api_view(['GET'])
# get data by menu_link
def topic_details(request, menu_link):
    # return topic details as json for a api
    topic = next((topic for topic in topics if topic['menu_link'] == menu_link), None)
    if topic:
        return Response(topic)
    else:
        return Response({'error': 'No Topic Found'}, status=status.HTTP_404_NOT_FOUND)
    
Employee = [
    {
        'id': 1,
        'name': 'John Doe',
        'position': 'Software Developer',
        'linkdin': 'https://www.linkedin.com/in/johndoe',
        'image': 'https://via.placeholder.com/300',
        'created_at': '2021-07-15T09:00:00Z',
    },
    {
        'id': 2,
        'name': 'Jane Doe',
        'position': 'Software Developer',
        'linkdin': 'https://www.linkedin.com/in/janedoe',
        'image': 'https://via.placeholder.com/300',
        'created_at': '2021-07-15T09:00:00Z',
    },
    {
        'id': 3,
        'name': 'Tom Doe',
        'position': 'Software Developer',
        'linkdin': 'https://www.linkedin.com/in/tomdoe',
        'image': 'https://via.placeholder.com/300',
        'created_at': '2021-07-15T09:00:00Z',
    },
    {
        'id':4,
        'name': 'Jerry Doe',
        'position': 'Software Developer',
        'linkdin': 'https://www.linkedin.com/in/jerrydoe',
        'image': 'https://via.placeholder.com/300',
        'created_at': '2021-07-15T09:00:00Z',
    },
    {
        'id': 5,
        'name': 'Jerry Doe',
        'position': 'Software Developer',
        'linkdin': 'https://www.linkedin.com/in/jerrydoe',
        'image': 'https://via.placeholder.com/300',
        'created_at': '2021-07-15T09:00:00Z',
    }
]

@api_view(['GET'])
def latest_employees(request):
    # return latest employees as json for a api and first 4 employees
    latest_employees = Employee[:4]

    # Convert the employees to a list of dictionaries
    employees_list = [
        {
            'id': employee['id'],
            'name': employee['name'],
            'position': employee['position'],
            'linkedin': employee['linkdin'],
            'image': employee['image'],
        }
        for employee in latest_employees
    ]
    return Response(employees_list)

@api_view(['GET'])
def all_employees(request):
    # return all employees as json for a api
    employees_list = [
        {
            'id': employee['id'],
            'name': employee['name'],
            'position': employee['position'],
            'linkedin': employee['linkdin'],
            'image': employee['image'],
        }
        for employee in Employee
    ]
    return Response(employees_list)


Blogs = [
    # each blog should have image, title meta_tile, description, author, created_at
    {
        'id': 1,
        'title': 'Lorem Ipsum is simply',
        'meta_title': 'It is a long established fact that a reader will be distracted by the readable content ',
        'description': 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using Content here, content here, making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for lorem ipsum will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).',
        'image': 'https://via.placeholder.com/600',
        'author': 'John Doe',
        'created_at': '2021-07-15T09:00:00Z',
    },
    {
        'id': 2,
        'title': 'Another Blog',
        'meta_title': 'This is another blog',
        'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam auctor, nisl at lacinia tincidunt, metus nunc tincidunt urna, nec tincidunt justo nunc id nunc. Sed auctor, nunc id consequat aliquam, nunc nunc tincidunt urna, nec tincidunt justo nunc id nunc.',
        'image': 'https://via.placeholder.com/600',
        'author': 'Jane Doe',
        'created_at': '2021-07-16T10:00:00Z',
    },
    {
        'id': 3,
        'title': 'Third Blog',
        'meta_title': 'This is the third blog',
        'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam auctor, nisl at lacinia tincidunt, metus nunc tincidunt urna, nec tincidunt justo nunc id nunc. Sed auctor, nunc id consequat aliquam, nunc nunc tincidunt urna, nec tincidunt justo nunc id nunc.',
        'image': 'https://via.placeholder.com/600',
        'author': 'Tom Doe',
        'created_at': '2021-07-17T11:00:00Z',
    },
    {
        'id': 4,
        'title': 'Fourth Blog',
        'meta_title': 'This is the fourth blog',
        'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam auctor, nisl at lacinia tincidunt, metus nunc tincidunt urna, nec tincidunt justo nunc id nunc. Sed auctor, nunc id consequat aliquam, nunc nunc tincidunt urna, nec tincidunt justo nunc id nunc.',
        'image': 'https://via.placeholder.com/600',
        'author': 'Jerry Doe',
        'created_at': '2021-07-18T12:00:00Z',
    }
]

@api_view(['GET'])
def all_blogs(request):
    # return latest blogs as json for a api
    blogs_list = [
        {'id': blog['id'], 'title': blog['title'], 'meta_title': blog['meta_title'], 'image': blog['image']}
        for blog in Blogs
    ]
    return Response(blogs_list)

@api_view(['GET'])
def blog_details(request, blog_id):
    # return blog details as json for a api
    blog = next((blog for blog in Blogs if blog['id'] == blog_id), None)
    if blog:
        return Response(blog)
    else:
        return Response({'error': 'No Blog Found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def privacy_policy(request):
    # return privacy policy as json for a api
    privacy_policy = {
        'title': 'Privacy Policy',
        'content': 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using Content here, content here, making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for lorem ipsum will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).It is a long established fact that a reader will be distracted by the readable content It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using Content here, content here, making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for lorem ipsum will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).It is a long established fact that a reader will be distracted by the readable content It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using Content here, content here, making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for lorem ipsum will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).It is a long established fact that a reader will be distracted by the readable contentIt is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using Content here, content here, making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for lorem ipsum will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).It is a long established fact that a reader will be distracted by the readable content',
    }
    return Response(privacy_policy)





# backend views are here
def logout(request):
    auth_logout(request)
    return redirect('index')

def sitelogin(request):
    if request.method == 'POST':
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            messages.success(request, 'your are login successfully')
            auth_login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Email or Password is incorrect')
    return render(request, 'index.html')

def createUser(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User Created Successfully')
        else:
            messages.error(request, form.errors.as_text())
    else:
        form = CustomUserCreationForm()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def users(request):
    users = CustomUser.objects.all()
    return render(request, 'users.html', {'users': users})

def verify_user(request, id):
    user = get_object_or_404(CustomUser, id=id)
    # if verified make it unverified and not verified make it verified
    if user.is_verified:
        messages.success(request, 'User Unverified Successfully')
        user.is_verified = False
        user.save()
    else:
        messages.success(request, 'User Verified Successfully')
        user.is_verified = True
        user.save()
    return redirect('users')

def delete_user(request, id):
    user = get_object_or_404(CustomUser, id=id)
    user.delete()
    messages.success(request, 'User Deleted Successfully')
    return redirect('users')

def createFrontendContent(request):
    if request.method == 'POST':
        if request.POST.get('content_type') == 'hero_section':
            return render(request, 'create_hero_section.html')
        elif request.POST.get('content_type') == 'topic_section':
            return render(request, 'create_topic_section.html')
        elif request.POST.get('content_type') == 'middle_section':
            return render(request, 'create_middle_section.html')
        elif request.POST.get('content_type') == 'employee_section':
            return render(request, 'create_employee_section.html')
        elif request.POST.get('content_type') == 'customer_review_section':
            return render(request, 'create_customer_review_section.html')
        elif request.POST.get('content_type') == 'tems_and_condition_section':
            return render(request, 'create_tems_and_condition_section.html')
        elif request.POST.get('content_type') == 'privacy_policy_section':
            return render(request, 'create_privacy_policy_section.html')
        elif request.POST.get('content_type') == 'faq_section':
            return render(request, 'create_faq_section.html')
    return render(request, 'create_frontend_content.html')

def submitContent(request):
    if request.method == 'POST':
        if request.POST.get('content_type') == 'hero_section':
            try:
                if FrontendContent.objects.filter(content_type='hero_section').exists():
                    messages.error(request, 'Hero Section Already Exist')
                else:
                    author = request.user
                    title = request.POST.get('title')
                    short_des = request.POST.get('short_des')
                    video_url = request.POST.get('video_url')
                    content = {'title': title, 'short_des': short_des, 'video_url': video_url}
                    FrontendContent.objects.create(content_type='hero_section', author=author, content=content)
                    messages.success(request, 'Hero Section Created Successfully')
            except:
                messages.error(request, 'Something went wrong')
        elif request.POST.get('content_type') == 'topic_section':
            try:
                if FrontendContent.objects.filter(content_type='topic_section').count() == 3:
                    messages.error(request, 'You can not create more than 3 topic section')
                else:
                    image = request.FILES.get('image')
                    author = request.user
                    title = request.POST.get('title')
                    short_des = request.POST.get('short_des')
                    content = {'title': title, 'short_des': short_des}
                    FrontendContent.objects.create(content_type='topic_section', author=author, content=content, image=image)
                    messages.success(request, 'Topic Section Created Successfully')
            except:
                messages.error(request, 'Something went wrong')
        elif request.POST.get('content_type') == 'middle_section':
            try:
                if FrontendContent.objects.filter(content_type='middle_section').exists():
                    messages.error(request, 'Middle Section Already Exist')
                else:
                    image = request.FILES.get('image')
                    author = request.user
                    title = request.POST.get('title')
                    short_des = request.POST.get('short_des')
                    link = request.POST.get('link')
                    content = {'title': title, 'short_des': short_des, 'link': link}
                    FrontendContent.objects.create(content_type='middle_section', author=author, content=content, image=image)
                    messages.success(request, 'Middle Section Created Successfully')
            except:
                messages.error(request, 'Something went wrong')
        elif request.POST.get('content_type') == 'employee_section':
            try:
                image = request.FILES.get('image')
                author = request.user
                name = request.POST.get('name')
                position = request.POST.get('position')
                short_des = request.POST.get('short_des')
                content = {'name': name, 'position': position, 'short_des': short_des}
                FrontendContent.objects.create(content_type='employee_section', author=author, content=content, image=image)
                messages.success(request, 'Employee Section Created Successfully')
            except:
                messages.error(request, 'Something went wrong')
        elif request.POST.get('content_type') == 'customer_review_section':
            try:
                image = request.FILES.get('image')
                author = request.user
                name = request.POST.get('name')
                status = request.POST.get('status')
                rating = request.POST.get('rating')
                short_des = request.POST.get('short_des')
                content = {'name': name, 'status': status, 'rating': rating, 'short_des': short_des}
                FrontendContent.objects.create(content_type='customer_review_section', author=author, content=content, image=image)
                messages.success(request, 'Customer Review Section Created Successfully')
            except:
                messages.error(request, 'Something went wrong')
        elif request.POST.get('content_type') == 'tems_and_condition_section':
            try:
                if FrontendContent.objects.filter(content_type='tems_and_condition_section').exists():
                    messages.error(request, 'Tems and Condition Section Already Exist')
                else:
                    author = request.user
                    if (request.FILES.get('image')):
                        image = request.FILES.get('image')
                    else:
                        image = None
                    title = request.POST.get('title')
                    short_des = request.POST.get('short_des')
                    content = {'title': title, 'short_des': short_des}
                    FrontendContent.objects.create(content_type='tems_and_condition_section', author=author, content=content, image=image)
                    messages.success(request, 'Tems and Condition Section Created Successfully')
            except:
                messages.error(request, 'Something went wrong')
        elif request.POST.get('content_type') == 'privacy_policy_section':
            try:
                if FrontendContent.objects.filter(content_type='privacy_policy_section').exists():
                    messages.error(request, 'Privacy Policy Section Already Exist')
                else:
                    author = request.user
                    if (request.FILES.get('image')):
                        image = request.FILES.get('image')
                    else:
                        image = None
                    title = request.POST.get('title')
                    short_des = request.POST.get('short_des')
                    content = {'title': title, 'short_des': short_des}
                    FrontendContent.objects.create(content_type='privacy_policy_section', author=author, content=content, image=image)
                    messages.success(request, 'Privacy Policy Section Created Successfully')
            except:
                messages.error(request, 'Something went wrong')
        elif request.POST.get('content_type') == 'faq_section':
            try:
                if FrontendContent.objects.filter(content_type='faq_section').exists():
                    messages.error(request, 'FAQ Section Already Exist')
                else:
                    author = request.user
                    title = request.POST.get('title')
                    short_des = request.POST.get('short_des')
                    questions = request.POST.getlist('question[]')
                    answers = request.POST.getlist('answer[]')
                    faq = []
                    for i in range(len(questions)):
                        faq.append({'question': questions[i], 'answer': answers[i]})
                    content = {'title': title, 'short_des': short_des, 'faq': faq}
                    FrontendContent.objects.create(content_type='faq_section', author=author, content=content)
                    messages.success(request, 'FAQ Section Created Successfully')
            except:
                messages.error(request, 'Something went wrong')
    return redirect('contentList')

def contentList(request):
    contents = FrontendContent.objects.all()
    return render(request, 'content_list.html', {'contents': contents})

def deleteContent(request, id):
    content = get_object_or_404(FrontendContent, id=id)
    content.delete()
    messages.success(request, 'Content Deleted Successfully')
    return redirect('contentList')

def editContent(request, id):
    content = get_object_or_404(FrontendContent, id=id)
    if request.method == 'POST':
        if content.content_type == 'hero_section':
            try:
                if request.POST.get('title'):
                    content.content['title'] = request.POST.get('title')
                if request.POST.get('short_des'):
                    content.content['short_des'] = request.POST.get('short_des')
                if request.POST.get('video_url'):
                    content.content['video_url'] = request.POST.get('video_url')
                content.save()
                messages.success(request, 'Content Updated Successfully')
                return redirect('contentList')
            except:
                messages.error(request, 'Something went wrong')
        elif content.content_type == 'topic_section':
            try:
                if request.POST.get('title'):
                    content.content['title'] = request.POST.get('title')
                if request.POST.get('short_des'):
                    content.content['short_des'] = request.POST.get('short_des')
                if request.FILES.get('image'):
                    content.image = request.FILES.get('image')
                content.save()
                messages.success(request, 'Content Updated Successfully')
                return redirect('contentList')
            except:
                messages.error(request, 'Something went wrong')
        elif content.content_type == 'middle_section':
            try:
                if request.POST.get('title'):
                    content.content['title'] = request.POST.get('title')
                if request.POST.get('short_des'):
                    content.content['short_des'] = request.POST.get('short_des')
                if request.POST.get('link'):
                    content.content['link'] = request.POST.get('link')
                if request.FILES.get('image'):
                    content.image = request.FILES.get('image')
                content.save()
                messages.success(request, 'Content Updated Successfully')
                return redirect('contentList')
            except:
                messages.error(request, 'Something went wrong')
        elif content.content_type == 'employee_section':
            try:
                if request.POST.get('name'):
                    content.content['name'] = request.POST.get('name')
                if request.POST.get('position'):
                    content.content['position'] = request.POST.get('position')
                if request.POST.get('short_des'):
                    content.content['short_des'] = request.POST.get('short_des')
                if request.FILES.get('image'):
                    content.image = request.FILES.get('image')
                content.save()
                messages.success(request, 'Content Updated Successfully')
                return redirect('contentList')
            except:
                messages.error(request, 'Something went wrong')
        elif content.content_type == 'customer_review_section':
            try:
                if request.POST.get('name'):
                    content.content['name'] = request.POST.get('name')
                if request.POST.get('status'):
                    content.content['status'] = request.POST.get('status')
                if request.POST.get('rating'):
                    content.content['rating'] = request.POST.get('rating')
                if request.POST.get('short_des'):
                    content.content['short_des'] = request.POST.get('short_des')
                if request.FILES.get('image'):
                    content.image = request.FILES.get('image')
                content.save()
                messages.success(request, 'Content Updated Successfully')
                return redirect('contentList')
            except:
                messages.error(request, 'Something went wrong')
        elif content.content_type == 'tems_and_condition_section':
            try:
                if request.POST.get('title'):
                    content.content['title'] = request.POST.get('title')
                if request.POST.get('short_des'):
                    content.content['short_des'] = request.POST.get('short_des')
                if request.FILES.get('image'):
                    content.image = request.FILES.get('image')
                content.save()
                messages.success(request, 'Content Updated Successfully')
                return redirect('contentList')
            except:
                messages.error(request, 'Something went wrong')
        elif content.content_type == 'privacy_policy_section':
            try:
                if request.POST.get('title'):
                    content.content['title'] = request.POST.get('title')
                if request.POST.get('short_des'):
                    content.content['short_des'] = request.POST.get('short_des')
                if request.FILES.get('image'):
                    content.image = request.FILES.get('image')
                content.save()
                messages.success(request, 'Content Updated Successfully')
                return redirect('contentList')
            except:
                messages.error(request, 'Something went wrong')
        elif content.content_type == 'faq_section':
            try:
                if request.POST.get('title'):
                    content.content['title'] = request.POST.get('title')
                if request.POST.get('short_des'):
                    content.content['short_des'] = request.POST.get('short_des')
                questions = request.POST.getlist('question[]')
                answers = request.POST.getlist('answer[]')
                faq = []
                for i in range(len(questions)):
                    faq.append({'question': questions[i], 'answer': answers[i]})
                content.content['faq'] = faq
                content.save()
                messages.success(request, 'Content Updated Successfully')
                return redirect('contentList')
            except:
                messages.error(request, 'Something went wrong')
    
    if content.content_type == 'hero_section':
        return render(request, 'edit_hero_section.html', {'content': content})
    elif content.content_type == 'topic_section':
        return render(request, 'edit_topic_section.html', {'content': content})
    elif content.content_type == 'middle_section':
        return render(request, 'edit_middle_section.html', {'content': content})
    elif content.content_type == 'employee_section':
        return render(request, 'edit_employee_section.html', {'content': content})
    elif content.content_type == 'customer_review_section':
        return render(request, 'edit_customer_review_section.html', {'content': content})
    elif content.content_type == 'tems_and_condition_section':
        return render(request, 'edit_tems_and_condition_section.html', {'content': content})
    elif content.content_type == 'privacy_policy_section':
        return render(request, 'edit_privacy_policy_section.html', {'content': content})
    elif content.content_type == 'faq_section':
        return render(request, 'edit_faq_section.html', {'content': content})
    return redirect('contentList')

def userMessages(request):
    messages = Contact_form.objects.all()
    template = 'user_messages.html'
    return render(request, template, {'messages': messages})

def deleteMessage(request, id):
    message = get_object_or_404(Contact_form, id=id)
    message.delete()
    messages.success(request, 'Message Deleted Successfully')
    return redirect('userMessages')

def viewMessage(request, id):
    message = get_object_or_404(Contact_form, id=id)
    return render(request, 'view_message.html', {'message': message})

def menuList(request):
    menus = Menu.objects.filter(is_deleted=False)
    # include 'icon' data fron MenuContent
    return render(request, 'menu_list.html', {'menus': menus})    

def createMenu(request):
    all_menus = Menu.objects.filter(is_deleted=False)
    try:
        if request.method == 'POST':
            menu_name = request.POST.get('menu_name')
            menu_link = menu_name.replace(' ', '-').lower()
            parent_menu = request.POST.get('parent_menu')
            sequence = request.POST.get('sequence')
            created_by = request.user
            title = request.POST.get('title')
            meta_title = request.POST.get('meta_title')
            description = request.POST.get('description')
            description = {'description': description}
            image = request.FILES.get('image')
            icon = request.FILES.get('icon')
            if parent_menu:
                parent_menu = Menu.objects.get(id=parent_menu)
            else:
                parent_menu = None
            if not sequence:
                sequence = None
            if not meta_title:
                meta_title = None
            if not image:
                image = None
            if not description:
                description = None
            if icon:
                urrent_icon_count = MenuContent.objects.exclude(icon='').exclude(icon__isnull=True).count()
                if urrent_icon_count >= 7:
                    messages.error(request, 'You can not create more than 8 menu with icon')
                    return redirect('menuList')
            else:
                icon = None        
            Menu.objects.create(menu_name=menu_name, menu_link=menu_link, parent_menu=parent_menu, sequence=sequence, created_by=created_by)
            menu = Menu.objects.get(menu_name=menu_name, menu_link=menu_link, parent_menu=parent_menu, sequence=sequence, created_by=created_by)
            MenuContent.objects.create(menu=menu, title=title, meta_title=meta_title, description=description, image=image, icon=icon)
            messages.success(request, 'Menu Created Successfully')
            return redirect('menuList')
    except:
        messages.error(request, 'Something went wrong')   
    return render(request, 'create_menu.html', {'all_menus': all_menus})

def deleteMenu(request, id):
    menu = get_object_or_404(Menu, id=id)
    menu.delete()
    messages.success(request, 'Menu Deleted Successfully')
    return redirect('menuList')

def editMenu(request, id):
    menu = get_object_or_404(Menu, id=id)
    all_menus = Menu.objects.filter(is_deleted=False)
    if request.method == 'POST':
        menu_name = request.POST.get('menu_name')
        menu_link = menu_name.replace(' ', '-').lower()
        parent_menu = request.POST.get('parent_menu')
        sequence = request.POST.get('sequence')
        title = request.POST.get('title')
        meta_title = request.POST.get('meta_title')
        description = request.POST.get('description')
        description = {'description': description}
        image = request.FILES.get('image')
        icon = request.FILES.get('icon')
        if menu_name:
            menu.menu_name = menu_name
            menu.menu_link = menu_link
        if sequence:
            menu.sequence = sequence
        if parent_menu:
            parent_menu = Menu.objects.get(id=parent_menu)
            menu.parent_menu = parent_menu
        menu.save()
        menu_content = MenuContent.objects.get(menu=menu)
        if title:
            menu_content.title = title
        if meta_title:
            menu_content.meta_title = meta_title
        if description:
            menu_content.description = description
        if image:
            menu_content.image = image
        if icon:
            if menu.menucontent.icon:
                pass
            else:
                urrent_icon_count = MenuContent.objects.exclude(icon='').exclude(icon__isnull=True).count()
                if urrent_icon_count >= 7:
                    messages.error(request, 'You can not create more than 8 menu with icon')
                    return redirect('menuList')
            menu_content.icon = icon
        menu_content.save()
        messages.success(request, 'Menu Updated Successfully')
        return redirect('menuList')
    return render(request, 'edit_menu.html', {'menu': menu, 'all_menus': all_menus})




# now make a api which will return all the contents "hero_section", "topic_section", "middle_section", "employee_section", "customer_review_section" for the frontend
@api_view(['GET'])
def home_page_content(request):
    domain = settings.DOMAIN_NAME
    contents = FrontendContent.objects.all()
    content_list = []
    all_topics = []
    all_employees = []
    all_customer_reviews = []
    all_menu_contents = []
    for content in contents:
        if content.content_type == 'hero_section':
            content_list.append({'hero_section': content.content})
        elif content.content_type == 'topic_section':
            all_topics.append({'title': content.content['title'], 'short_des': content.content['short_des'], 'image': domain + content.image.url})
        elif content.content_type == 'middle_section':
            all_middle_content = {
                'title': content.content['title'],
                'short_des': content.content['short_des'],
                'link': content.content['link'],
                'image': domain + content.image.url
            }
            content_list.append({'middle_section': all_middle_content})
        elif content.content_type == 'employee_section':
            all_employees.append({'id': content.id,'name': content.content['name'], 'position': content.content['position'], 'image': domain + content.image.url})
        elif content.content_type == 'customer_review_section':
            all_customer_reviews.append({'name': content.content['name'], 'status': content.content['status'], 'rating': content.content['rating'], 'short_des': content.content['short_des'], 'image': domain + content.image.url})

    content_list.append({'topic_section': all_topics})
    content_list.append({'employee_section': all_employees})
    content_list.append({'customer_review_section': all_customer_reviews})
    menu_contents = MenuContent.objects.exclude(icon='').exclude(icon__isnull=True)[:8]
    if menu_contents:
        for menu_content in menu_contents:
            all_menu_contents.append({'name': menu_content.menu.menu_name, 'icon': domain + menu_content.icon.url})
        content_list.append({'menu_content': all_menu_contents})
    if content_list:
        return Response(content_list, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'No Content Found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def employee_details(request, id):
    employee = get_object_or_404(FrontendContent, id=id)
    if employee.content_type == 'employee_section':
        employee_data = {
            'name': employee.content['name'],
            'position': employee.content['position'],
            'short_des': employee.content['short_des'],
            'image': settings.DOMAIN_NAME + employee.image.url
        }
        return Response(employee_data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'No Employee Found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def tems_and_condition(request):
    content = FrontendContent.objects.filter(content_type='tems_and_condition_section').first()
    if content:
        return Response(content.content, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'No Content Found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def privacy_policy(request):
    content = FrontendContent.objects.filter(content_type='privacy_policy_section').first()
    if content:
        return Response(content.content, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'No Content Found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def faq(request):
    content = FrontendContent.objects.filter(content_type='faq_section').first()
    if content:
        return Response(content.content, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'No Content Found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def contact_us(request):
    serializer = Contact_formSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Your Query Submitted Successfully'}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def menu_details(request, menu_link):
    menu = get_object_or_404(Menu, menu_link=menu_link)
    if menu:
        content = MenuContent.objects.filter(menu=menu).first()
        if content.image:
            imageURL = settings.DOMAIN_NAME + content.image.url
        else:
            imageURL = None
        if content.icon:
            iconURL = settings.DOMAIN_NAME + content.icon.url
        else:
            iconURL = None
        if content.description:
            # the description data is {'description': 'value'} 
            description = content.description['description']
        else:
            description = None
        if content.meta_title:
            meta_title = content.meta_title
        else:
            meta_title = None
        if content:
            menu_data = {
                'title': content.title,
                'meta_title': meta_title,
                'description': description,
                'image': imageURL,
                'icon': iconURL
            }
            return Response(menu_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No Content Found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'No Menu Found'}, status=status.HTTP_404_NOT_FOUND)