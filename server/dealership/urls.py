from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from djangoapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/csrf', views.csrf),
    path('djangoapp/user', views.user),
    path('djangoapp/login', views.login_user),
    path('djangoapp/logout', views.logout_user),
    path('djangoapp/registration', views.register),
    path('djangoapp/get_dealers', views.dealers),
    path('djangoapp/get_dealers/<str:state>', views.dealers),
    path('djangoapp/dealer/<int:dealer_id>', views.dealer),
    path('djangoapp/reviews/dealer/<int:dealer_id>', views.reviews),
    path('djangoapp/add_review', views.add_review),
    path('djangoapp/get_cars', views.cars),
    path('djangoapp/analyze_review', views.analyze),
    path('about', views.about), path('contact', views.contact),
    re_path(r'^(?:|login|register|dealer/\d+|postreview/\d+)/?$', views.index),
]
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
