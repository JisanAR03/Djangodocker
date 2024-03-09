from django.urls import re_path, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('api/heroPart/', views.hero_part, name="hero_part"),
    path('api/topics/', views.all_topics, name='all_topics'),
    # teh topic topic get data with wenu_link
    path('api/topics/<str:menu_link>/', views.topic_by_menu_link, name='topic_by_menu_link'),
    path('api/latestEmployees/', views.latest_employees, name='latest_employees'),
    path('api/employees/', views.all_employees, name='all_employees'),
    path('api/blogs/', views.all_blogs, name='all_blogs'),
    path('api/blogs/<int:blog_id>/', views.blog_details, name='blog_details'),
    path('api/privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('api/menu/', views.list_menu_content, name='list-menu-content'),
    
    
    
    
    
    re_path('login/', views.login, name='login'), #post request
    re_path('user_type/', views.user_type_list, name='user_type'), #get request
    re_path('change_password/', views.change_password, name='change_password'), #put request --->new added
    re_path('user_type_supreme/', views.user_type_list_supreme, name='user_type_supreme'), #get request
    re_path('create_user/', views.create_user, name='create_user'), #post request
    re_path('create_user_supreme/', views.create_user_supreme, name='create_user_supreme'), #post request
    re_path('all_users/', views.all_user_list, name='all_users'), #get request
    re_path('user_detail/(?P<pk>\w+)/', views.user_edit_page, name='user_detail'), #get request
    re_path('user_edit/(?P<pk>\w+)/', views.user_edit, name='user_edit'), #put request
    re_path('user_delete/(?P<pk>\w+)/', views.user_delete, name='user_delete'), #delete request
    re_path('return_user_detail/', views.logged_user_type, name='logged_user_type'), #get request
    re_path('verify-email/', views.verify_email, name='verify-email'), #get request
    re_path('resend-verification-email/', views.resend_verification_email, name='resend-verification-email'), #post request
    re_path('create_not_admin_user/', views.create_not_admin_user, name='create_not_admin_user'), #post request --->new added
    # frontend data manupulation from here
    re_path('content/options/', views.content_options, name='content-options'), #get request
    re_path('content/create/', views.create_frontend_content, name='create-frontend-content'), #post request
    re_path('content/edit/(?P<pk>\w+)/', views.edit_frontend_content, name='edit-frontend-content'), #get request
    re_path('content/update/(?P<pk>\w+)/', views.update_frontend_content, name='update-frontend-content'), #put request
    re_path('content/delete/(?P<pk>\w+)/', views.delete_frontend_content, name='delete-frontend-content'), #delete request
    re_path('content/delete_temp/(?P<pk>\w+)/', views.delete_frontend_content_temp, name='delete-temp-frontend-content'), #put request --->new added
    re_path('content/list_temp/all/', views.list_frontend_content_temp, name='list-all-temp'), #get request --->new added
    # frontend data present from here
    re_path('content/list/hero_mains/', views.list_frontend_content_hero_section, name='list-hero-main'), #get request
    re_path('content/list/hero_subs/', views.list_frontend_content_hero_section_sub_content, name='list-hero-sub'), #get request
    re_path('content/list/about_mains/', views.list_frontend_content_about_section, name='list-about-main'), #get request
    re_path('content/list/about_subs/', views.list_frontend_content_about_section_sub_content, name='list-about-sub'), #get request
    re_path('content/list/services_mains/', views.list_frontend_content_services_section, name='list-services-main'), #get request
    re_path('content/list/services_subs/', views.list_frontend_content_services_section_sub_content, name='list-services-sub'), #get request
    re_path('content/list/blog_mains/', views.list_frontend_content_blog_section, name='list-blog-main'), #get request
    re_path('content/list/blog_subs/', views.list_frontend_content_blog_section_sub_content, name='list-blog-sub'), #get request
    re_path('content/list/projects_mains/', views.list_frontend_content_projects_section, name='list-projects-main'), #get request
    re_path('content/list/projects_subs/', views.list_frontend_content_projects_section_sub_content, name='list-projects-sub'), #get request
    re_path('content/list/protfolio_mains/', views.list_frontend_content_protfolio_section, name='list-protfolio-main'), #get request
    re_path('content/list/protfolio_subs/', views.list_frontend_content_protfolio_section_sub_content, name='list-protfolio-sub'), #get request
    re_path('content/list/reviews_mains/', views.list_frontend_content_reviews_section, name='list-reviews-main'), #get request
    re_path('content/list/reviews_subs/', views.list_frontend_content_reviews_section_sub_content, name='list-reviews-sub'), #get request
    re_path('content/list/pricing_mains/', views.list_frontend_content_pricing_section, name='list-pricing-main'), #get request
    re_path('content/list/pricing_subs/', views.list_frontend_content_pricing_section_sub_content, name='list-pricing-sub'), #get request
    re_path('content/list/team_mains/', views.list_frontend_content_team_section, name='list-team-main'), #get request
    re_path('content/list/team_subs/', views.list_frontend_content_team_section_sub_content, name='list-team-sub'), #get request
    re_path('content/list/contact_mains/', views.list_frontend_content_contact_section, name='list-contact-main'), #get request
    re_path('content/list/contact_subs/', views.list_frontend_content_contact_section_sub_content, name='list-contact-sub'), #get request
    re_path('content/list/social_links/', views.list_frontend_content_social_links, name='list-social-links'), #get request
    re_path('content/list/social_links_subs/', views.list_frontend_content_social_links_sub_content, name='list-social-links-sub'), #get request
    re_path('content/list/footer_mains/', views.list_frontend_content_footer_section, name='list-footer-main'), #get request
    re_path('content/list/footer_subs/', views.list_frontend_content_footer_section_sub_content, name='list-footer-sub'), #get request
    re_path('content/list/all/', views.list_frontend_content, name='list-all'), #get request
    
    
    # menu part from here
    re_path('menu/create/', views.create_menu, name='create-menu'), #post request  the field name is required is : menu_name, parent_menu, sequence, menu_link, menu_image, menu_title, menu_meta_title, menu_description
    re_path('menu/list/all/', views.list_menu, name='list-menu'), #get request   the field return menu_name and id and use id as value and menu_name as label
    re_path('menu/list/all_temp/', views.list_all_menu_temp, name='list-all-menu-temp'), #get request
    re_path('menu/edit/(?P<pk>\w+)/', views.edit_menu, name='edit-menu'), #get request
    re_path('menu/update/(?P<pk>\w+)/', views.update_menu, name='update-menu'), #put request
    re_path('menu/delete/(?P<pk>\w+)/', views.delete_menu, name='delete-menu'), #delete request
    re_path('menu/delete_temp/(?P<pk>\w+)/', views.delete_menu_temp, name='delete-menu-temp'), #put request 
    
    # now start menu content part for frontend
    re_path('menu/content/list_frontend/', views.list_menu_content, name='list-menu-content'), #get request
    # show menu content by menu_link value
    re_path('menu/menu_content/(?P<menu_link>\w+)/', views.menu_content_by_menu_link, name='menu-content-by-menu-link'), #get request
    
    
    # re_path('', views.index, name='index'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)