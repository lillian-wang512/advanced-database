from django.urls import re_path as url
 
from . import view
 
urlpatterns = [
    url(r'^$', view.homePage),
    url(r'^query2/$', view.query2),
    url(r'^query1/$', view.query1),
    url(r'^query3/$', view.query3),
]