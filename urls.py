from django.conf.urls import patterns, url

from directory import views

urlpatterns = patterns("",
    url(r"^$", views.index, name="index"),
    url(r"^all_depts/$", views.all_depts, name="all_depts"),
    url(r"^all_locations/$", views.all_locations, name="all_locations"),
    url(r"^pets/$", views.pets, name="pets"),
    url(r"^birthdays/$", views.birthdays, name="birthdays"),
    url(r"^login/$", views.login, name="login_employee"),
    url(r"^search/$", views.search, name="search_employees"),
    url(r"^search_by_dept/$", views.search_by_dept, name="search_by_dept"),
    url(r"^search_by_location/$", views.search_by_location, name="search_by_location"),
    url(r"^(?P<user_id>\d+)/$", views.user_view, name="view_employee"),
    url(r"^(?P<user_id>\d+)/edit/$", views.edit, name="edit_employee"),
    url(r"^pet/(?P<pet_id>\d+)/$", views.pet_view, name="view_pet"),
    url(r"^pet/(?P<pet_id>\d+)/edit/$", views.pet_edit, name="edit_pet"),
    url(r"^access_denied/$", views.access_denied, name="access_denied")
)
