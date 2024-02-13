from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from .serializers import UserCreateSerializer, FrontendContentSerializer, MenuSerializer, MenuContentSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import FrontendContent, CustomUser, Menu, MenuContent


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
        return Response(serializer.data, status=status.HTTP_200_OK)
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
    if request.user.user_type == 'supreme_admin' and request.user.is_verified:
        user = get_object_or_404(get_user_model(), pk=pk)
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
        menu_link = request.data.get('menu_link') #required
        if request.data.get('menu_image') == '':
            menu_image = None
        else:
            menu_image = request.data.get('menu_image')
        menu_title = request.data.get('menu_title') #required
        menu_description = request.data.get('menu_description') #required
        if request.data.get('menu_meta_title') == 'null':
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
    menus = Menu.objects.all()
    serializer = MenuSerializer(menus, many=True)
    if serializer.data:
        menu_data = [{'id': menu['id'], 'menu_name': menu['menu_name']} for menu in serializer.data]
        return Response(menu_data)
    else:
        return Response({'error': 'No Menu Found'}, status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['GET'])
def list_all_menu_temp(request):
    menus = Menu.objects.filter(is_deleted=False)
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
    if request.user.user_type == 'content_writer_admin' or request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin' and request.user.is_verified:
        menu_name = request.data.get('menu_name') #required
        if request.data.get('parent_menu') == '':
            parent_menu = None
        else:
            parent_menu = request.data.get('parent_menu')
        if request.data.get('sequence') == '':
            sequence = None
        else:
            sequence = request.data.get('sequence')
        menu_link = request.data.get('menu_link')
        if request.data.get('menu_image') == '':
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
            menuContentSerializer = MenuContentSerializer(menu_content, data={'image': menu_image,'title': menu_title,'description': menu_description,'meta_title': menu_meta_title})
            if menuContentSerializer.is_valid():
                menuContentSerializer.save()
                return Response({'message': 'Menu Updated Successfully'}, status=status.HTTP_200_OK)
            else:
                return Response(menuContentSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
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
            if os.path.isfile(settings.MEDIA_ROOT + '/' + menu_image):
                os.remove(settings.MEDIA_ROOT + '/' + menu_image)
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
        created_by = get_object_or_404(CustomUser, pk=serializer.data['created_by'])
        menu_data = {
            'menu_name': serializer.data['menu_name'],
            'menu_title': menuContentSerializer.data[0]['title'],
            'menu_description': menuContentSerializer.data[0]['description'],
            'menu_meta_title': menuContentSerializer.data[0]['meta_title'],
            'menu_image': menuContentSerializer.data[0]['image'],
            'created_at': menuContentSerializer.data[0]['created_at'],
            'created_by': created_by.username,
        }
        return Response(menu_data)
    except:
        return Response({'error': 'No Menu Found'}, status=status.HTTP_404_NOT_FOUND)