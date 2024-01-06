from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from .serializers import UserCreateSerializer, FrontendContentSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import FrontendContent


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
    if request.user.user_type == 'supreme_admin':
        user_types = [user_type[0] for user_type in get_user_model().USER_TYPES]
        response = {
            'user_types': user_types,
        }
        return Response(response, status=status.HTTP_200_OK)
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
    serializer = UserCreateSerializer(data=request.data)
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
    if request.user.user_type == 'supreme_admin':
        serializer = UserCreateSerializer(data=request.data)
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
    if request.user.user_type == 'supreme_admin':
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
    if request.user.user_type == 'supreme_admin':
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
    if request.user.user_type == 'supreme_admin':
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
    if request.user.user_type == 'supreme_admin':
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
    if request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin':
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
    if request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin':
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
    if request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin':
        content = get_object_or_404(FrontendContent, pk=pk)
        serializer = FrontendContentSerializer(content)
        return Response(serializer.data)
    else:
        return Response({'error': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def update_frontend_content(request, pk):
    if request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin':
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
    if request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin':
        content = get_object_or_404(FrontendContent, pk=pk)
        content.delete()
        return Response({'message': 'Content Deleted Successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def list_frontend_content(request):
    if request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin':
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
def list_frontend_content_hero_section(request):
    if request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin':
        contents = FrontendContent.objects.filter(content_type='hero_section',title_type='main_content')
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
def list_frontend_content_hero_section_sub_content(request):
    if request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin':
        contents = FrontendContent.objects.filter(content_type='hero_section',title_type='sub_content')
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
def list_frontend_content_about_section(request):
    if request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin':
        contents = FrontendContent.objects.filter(content_type='about_section',title_type='main_content')
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
def list_frontend_content_about_section_sub_content(request):
    if request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin':
        contents = FrontendContent.objects.filter(content_type='about_section',title_type='sub_content')
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
def list_frontend_content_services_section(request):
    if request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin':
        contents = FrontendContent.objects.filter(content_type='services_section',title_type='main_content')
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
def list_frontend_content_services_section_sub_content(request):
    if request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin':
        contents = FrontendContent.objects.filter(content_type='services_section',title_type='sub_content')
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
def list_frontend_content_blog_section(request):
    if request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin':
        contents = FrontendContent.objects.filter(content_type='blog_section',title_type='main_content')
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
def list_frontend_content_blog_section_sub_content(request):
    if request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin':
        contents = FrontendContent.objects.filter(content_type='blog_section',title_type='sub_content')
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
def list_frontend_content_projects_section(request):
    if request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin':
        contents = FrontendContent.objects.filter(content_type='projects_section',title_type='main_content')
        serializer = FrontendContentSerializer(contents, many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response({'error': 'No Content Found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'You do not have permission to access this resource.'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def list_frontend_content_projects_section_sub_content(request):
    if request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin':
        contents = FrontendContent.objects.filter(content_type='projects_section',title_type='sub_content')
        serializer = FrontendContentSerializer(contents, many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response({'error': 'No Content Found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'You do not have permission to access this resource.'},status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def list_frontend_content_protfolio_section(request):
    if request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin':
        contents = FrontendContent.objects.filter(title_type='main_content',content_type='protfolio_section')
        serializer = FrontendContentSerializer(contents, many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response({'error': 'No Content Found'},status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'You do not have permission to access this resource.'},status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def list_frontend_content_protfolio_section_sub_content(request):
    if request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin':
        contents = FrontendContent.objects.filter(title_type='sub_content',content_type='protfolio_section')
        serializer = FrontendContentSerializer(contents, many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response({'error': 'No Content Found'},status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'You do not have permission to access this resource.'},status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def list_frontend_content_reviews_section(request):
    if request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin':
        contents = FrontendContent.objects.filter(title_type='main_content',content_type='reviews_section')
        serializer = FrontendContentSerializer(contents, many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response({'error': 'No Content Found'},status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'You do not have permission to access this resource.'},status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def list_frontend_content_reviews_section_sub_content(request):
    if request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin':
        contents = FrontendContent.objects.filter(title_type='sub_content',content_type='reviews_section')
        serializer = FrontendContentSerializer(contents, many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response({'error': 'No Content Found'},status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'You do not have permission to access this resource.'},status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def list_frontend_content_pricing_section(request):
    if request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin':
        contents = FrontendContent.objects.filter(title_type='main_content',content_type='pricing_section')
        serializer = FrontendContentSerializer(contents, many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response({'error': 'No Content Found'},status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'You do not have permission to access this resource.'},status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def list_frontend_content_pricing_section_sub_content(request):
    if request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin':
        contents = FrontendContent.objects.filter(title_type='sub_content',content_type='pricing_section')
        serializer = FrontendContentSerializer(contents, many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response({'error': 'No Content Found'},status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'You do not have permission to access this resource.'},status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def list_frontend_content_team_section(request):
    if request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin':
        contents = FrontendContent.objects.filter(title_type='main_content',content_type='team_section')
        serializer = FrontendContentSerializer(contents, many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response({'error': 'No Content Found'},status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'You do not have permission to access this resource.'},status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def list_frontend_content_team_section_sub_content(request):
    if request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin':
        contents = FrontendContent.objects.filter(title_type='sub_content',content_type='team_section')
        serializer = FrontendContentSerializer(contents, many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response({'error': 'No Content Found'},status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'You do not have permission to access this resource.'},status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def list_frontend_content_contact_section(request):
    if request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin':
        contents = FrontendContent.objects.filter(title_type='main_content',content_type='contact_section')
        serializer = FrontendContentSerializer(contents, many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response({'error': 'No Content Found'},status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'You do not have permission to access this resource.'},status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def list_frontend_content_contact_section_sub_content(request):
    if request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin':
        contents = FrontendContent.objects.filter(title_type='sub_content',content_type='contact_section')
        serializer = FrontendContentSerializer(contents, many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response({'error': 'No Content Found'},status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'You do not have permission to access this resource.'},status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def list_frontend_content_social_links(request):
    if request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin':
        contents = FrontendContent.objects.filter(content_type='social_links',title_type='main_content')
        serializer = FrontendContentSerializer(contents, many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response({'error':'No Content Found'},status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'You do not have permission to access this resource.'},status=status.HTTP_200_OK)
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def list_frontend_content_social_links_sub_content(request):
    if request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin':
        contents = FrontendContent.objects.filter(content_type='social_links',title_type='sub_content')
        serializer = FrontendContentSerializer(contents, many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response({'error':'No Content Found'},status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'You do not have permission to access this resource.'},status=status.HTTP_200_OK)
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def list_frontend_content_footer_section(request):
    if request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin':
        contents = FrontendContent.objects.filter(content_type='footer_section',title_type='main_content')
        serializer = FrontendContentSerializer(contents, many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response({'error':'No Content Found'},status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'You do not have permission to access this resource.'},status=status.HTTP_200_OK)
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def list_frontend_content_footer_section_sub_content(request):
    if request.user.user_type == 'content_writer' or request.user.user_type == 'supreme_admin':
        contents = FrontendContent.objects.filter(content_type='footer_section',title_type='sub_content')
        serializer = FrontendContentSerializer(contents, many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response({'error':'No Content Found'},status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'You do not have permission to access this resource.'},status=status.HTTP_200_OK)