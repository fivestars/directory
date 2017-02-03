from datetime import date, timedelta

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response

from directory.forms import EditForm, PetEditForm
from directory.models import Department, Location, Employee, Pet

from itertools import chain

DIRECTORY_ADMIN_EMAILS = []


def get_all_depts():
    """
    :return: all the departments sorted by name
    """
    return Department.objects.order_by("name")


def get_all_locations():
    """
    :return: all the locations sorted by name
    """
    return Location.objects.order_by("name")


def is_logged_in(request):
    """
    Checks if the current user is logged in.

    :param request: the current request
    :return: true if the user is logged in, false otherwise
    """

    # check if logged in
    return request.user.is_authenticated()


def is_fivestars_employee(request):
    """
    Checks if the current user is a FiveStars employee.

    :param request: the current request
    :return: true if the user is a FiveStars employee, false otherwise
    """
    # check if user email ends in @fivestars.com
    fivestars_email = "@fivestars.com"
    user_email = request.user.profile.email
    if not (user_email and user_email.endswith(fivestars_email)):
        return False
    # check if has permissions
    return request.user.profile.permissions


def index(request):
    """
    Displays all the users sorted by start date and name and paginated.
    :param request: the current request.
    :return: the response with all the users rendered
    """

    # check if directory access allowed
    if not is_logged_in(request):
        return HttpResponseRedirect(reverse("directory:login_employee"))
    if not is_fivestars_employee(request):
        return HttpResponseRedirect(reverse("directory:access_denied"))

    # get all users sorted by start date descending, first name, last name
    user_list = Employee.objects.order_by("-start_date", "first_name", "last_name")

    # add pets to users
    user_pet_list = add_pets(user_list, cmp_start_date)

    # paginate the list of users and pets
    users_pets = paginate(request, user_pet_list)

    return render_to_response("index.html", {"depts": get_all_depts(), "locations":
        get_all_locations(), "users": users_pets, "home_page": True})


def login(request):
    """
    Displays the login form.
    :param request: the current request.
    :return: the response with the login form
    """

    # check if needs to login
    if is_logged_in(request):
        if is_fivestars_employee(request):
            return HttpResponseRedirect(reverse("directory:index"))
        return HttpResponseRedirect(reverse("directory:access_denied"))

    return render_to_response("login.html")


def access_denied(request):
    """
    Displays the access denied page.
    :param request: the current request.
    :return: the response with the access denied page
    """

    # check if directory access allowed
    if not is_logged_in(request):
        return HttpResponseRedirect(reverse("directory:login_employee"))
    if is_fivestars_employee(request):
        return HttpResponseRedirect(reverse("directory:index"))

    return render_to_response("access_denied.html")


def all_depts(request):
    """
    Displays all the users sorted by department and name and paginated.
    :param request: the current request.
    :return: the response with all the users rendered
    """

    # check if directory access allowed
    if not is_logged_in(request):
        return HttpResponseRedirect(reverse("directory:login_employee"))
    if not is_fivestars_employee(request):
        return HttpResponseRedirect(reverse("directory:access_denied"))

    # get all users sorted by department name, first name, last name
    user_list = Employee.objects.order_by("dept__name", "first_name", "last_name")

    # paginate the list of users
    users = paginate(request, user_list)

    return render_to_response("index.html", {"depts": get_all_depts(), "locations":
        get_all_locations(), "users": users, "heading": "All Departments", "all_dept_page": True})


def all_locations(request):
    """
    Displays all the users sorted by location and name and paginated.
    :param request: the current request.
    :return: the response with all the users rendered
    """

    # check if directory access allowed
    if not is_logged_in(request):
        return HttpResponseRedirect(reverse("directory:login_employee"))
    if not is_fivestars_employee(request):
        return HttpResponseRedirect(reverse("directory:access_denied"))

    # get all users sorted by location name, first name, last name
    user_list = Employee.objects.order_by("location__name", "first_name", "last_name")

    # add pets to users
    user_pet_list = add_pets(user_list, cmp_location)

    # paginate the list of users
    users = paginate(request, user_pet_list)

    return render_to_response("index.html", {"depts": get_all_depts(), "locations":
        get_all_locations(), "users": users, "heading": "All Locations", "all_locations_page":
        True})


def user_view(request, user_id):
    """
    Displays the specified user.
    :param request: the current request.
    :param user_id: the ID of the user to display
    :return: the response with the specified user rendered
    """

    # check if directory access allowed
    if not is_logged_in(request):
        return HttpResponseRedirect(reverse("directory:login_employee"))
    if not is_fivestars_employee(request):
        return HttpResponseRedirect(reverse("directory:access_denied"))

    # get FiveStars user
    user = get_object_or_404(Employee, pk=user_id)

    # get user's pets
    pets = Pet.objects.filter(owner=user)

    # set flag for whether edit button should be displayed
    profile_email = request.user.profile.email
    can_edit = user.email == profile_email or profile_email in DIRECTORY_ADMIN_EMAILS

    # display user
    return render(request, "user/index.html", {"depts": get_all_depts(), "locations":
        get_all_locations(), "user": user, "pets": pets, "can_edit": can_edit})


def edit(request, user_id):
    """
    Edits or displays the edit form for the specified user.
    :param request: the current request.
    :param user_id: the ID of the user to display
    :return: the response with the edit form or the specified user rendered after editing
    """

    # check if directory access allowed
    if not is_logged_in(request):
        return HttpResponseRedirect(reverse("directory:login_employee"))
    if not is_fivestars_employee(request):
        return HttpResponseRedirect(reverse("directory:access_denied"))

    # get FiveStars user
    user = get_object_or_404(Employee, pk=user_id)

    # check if allowed to edit
    profile_email = request.user.profile.email
    if user.email != profile_email and profile_email not in DIRECTORY_ADMIN_EMAILS:
        return HttpResponseRedirect(reverse("directory:view_employee", args=(user.id,)))

    # if the form has been submitted...
    if request.method == "POST":

        # get form bound to the POST data
        form = EditForm(request.POST, instance=user)

        # check if all validation rules pass
        if form.is_valid():

            # update user with information from request
            form.save()
            return HttpResponseRedirect(reverse("directory:view_employee", args=(user.id,)))
    else:
        # display edit (unbound) form if GET request
        form = EditForm()

    return render(request, "user/edit.html", {"depts": get_all_depts(), "locations":
        get_all_locations(), "form": form, "user": user})


def pets(request):
    """
    Displays all the pets sorted by name.
    :param request: the current request.
    :return: the response with all the pets rendered
    """

    # check if directory access allowed
    if not is_logged_in(request):
        return HttpResponseRedirect(reverse("directory:login_employee"))
    if not is_fivestars_employee(request):
        return HttpResponseRedirect(reverse("directory:access_denied"))

    # get all pets sorted by name
    pets = Pet.objects.order_by("name")

    return render_to_response("pets.html", {"depts": get_all_depts(), "locations":
        get_all_locations(), "pets": pets, "heading": "All Locations", "all_locations_page":
        True})


def pet_view(request, pet_id):
    """
    Displays the specified pet.
    :param request: the current request.
    :param pet_id: the ID of the pet to display
    :return: the response with the specified pet rendered
    """

    # check if directory access allowed
    if not is_logged_in(request):
        return HttpResponseRedirect(reverse("directory:login_employee"))
    if not is_fivestars_employee(request):
        return HttpResponseRedirect(reverse("directory:access_denied"))

    # get FiveStars pet
    pet = get_object_or_404(Pet, pk=pet_id)

    # set flag for whether edit button should be displayed
    profile_email = request.user.profile.email
    can_edit = pet.owner.email == profile_email or profile_email in DIRECTORY_ADMIN_EMAILS

    # display pet
    return render(request, "pet/index.html", {"depts": get_all_depts(), "locations":
        get_all_locations(), "pet": pet, "can_edit": can_edit})


def pet_edit(request, pet_id):
    """
    Edits or displays the edit form for the specified pet.
    :param request: the current request.
    :param pet_id: the ID of the pet to display
    :return: the response with the edit form or the specified pet rendered after editing
    """

    # check if directory access allowed
    if not is_logged_in(request):
        return HttpResponseRedirect(reverse("directory:login_employee"))
    if not is_fivestars_employee(request):
        return HttpResponseRedirect(reverse("directory:access_denied"))

    # get FiveStars pet
    pet = get_object_or_404(Pet, pk=pet_id)

    # check if allowed to edit
    profile_email = request.user.profile.email
    if pet.owner.email != profile_email and profile_email not in DIRECTORY_ADMIN_EMAILS:
        return HttpResponseRedirect(reverse("directory:view_pet", args=(pet.id,)))

    # if the form has been submitted...
    if request.method == "POST":

        # get form bound to the POST data
        form = PetEditForm(request.POST, instance=pet)

        # check if all validation rules pass
        if form.is_valid():

            # update pet with information from request
            form.save()
            return HttpResponseRedirect(reverse("directory:view_pet", args=(pet.id,)))
    else:
        # display edit (unbound) form if GET request
        form = EditForm()

    return render(request, "pet/edit.html", {"depts": get_all_depts(), "locations":
        get_all_locations(), "form": form, "pet": pet})


def birthdays(request):
    """
    Displays all the users whose birthdays are within the next 30 days.
    :param request: the current request
    :return: the response with all the users with upcoming birthdays
    """

    # check if directory access allowed
    if not is_logged_in(request):
        return HttpResponseRedirect(reverse("directory:login_employee"))
    if not is_fivestars_employee(request):
        return HttpResponseRedirect(reverse("directory:access_denied"))

    # get users whose birthdays are in the next 30 days
    today = date.today()
    end_date = today + timedelta(days=30)
    if today.month == 12:
        user_list_1 = Employee.objects.extra(
            where=["(EXTRACT(month FROM birthday), EXTRACT(day FROM birthday)) between (%d,%d) and "
                   "(%d, %d)" % (today.month, today.day, today.month, 31)])
        user_list_2 = Employee.objects.extra(
            where=["(EXTRACT(month FROM birthday), EXTRACT(day FROM birthday)) between (%d,%d) and "
                   "(%d, %d)" % (end_date.month, 1, end_date.month, end_date.day)])
        user_list = (user_list_1 | user_list_2).extra(
            select={"birth_month": "EXTRACT(month FROM birthday)",
                "birth_day": "EXTRACT(day FROM birthday)"},
            order_by=["birth_month", "birth_day"])
    else:
        user_list = Employee.objects.extra(
            select={"birth_month": "EXTRACT(month FROM birthday)",
                "birth_day": "EXTRACT(day FROM birthday)"},
            where=["(EXTRACT(month FROM birthday), EXTRACT(day FROM birthday)) between (%d,%d) and "
                   "(%d, %d)" % (today.month, today.day, end_date.month, end_date.day)],
            order_by=["birth_month", "birth_day"])

    # paginate the list of users
    users = paginate(request, user_list)

    return render_to_response("index.html", {"depts": get_all_depts(), "locations":
        get_all_locations(), "users": users, "birthdays_page": True})


def search(request):

    # check if directory access allowed
    if not is_logged_in(request):
        return HttpResponseRedirect(reverse("directory:login_employee"))
    if not is_fivestars_employee(request):
        return HttpResponseRedirect(reverse("directory:access_denied"))

    if "q" in request.GET and request.GET["q"]:
        query = request.GET["q"]

        if "@" in query:
            user_list = search_by_email(query)
        else:
            names = query.split(" ")
            if len(names) == 1:
                user_list = search_by_name(first_name=names[0])
            else:
                user_list = search_by_name(first_name=names[0], last_name=names[1])

        # add pets
        pet_list = Pet.objects.filter(name__icontains=query).order_by("name")
        user_pet_list = sorted(chain(user_list, pet_list), cmp=cmp_name)

        users = paginate(request, user_pet_list)

        return render(request, "index.html",
                      {"depts": get_all_depts(), "locations": get_all_locations(), "users": users,
                          "query": query, "input": query, "search_page": True})


def search_by_dept(request):

    # check if directory access allowed
    if not is_logged_in(request):
        return HttpResponseRedirect(reverse("directory:login_employee"))
    if not is_fivestars_employee(request):
        return HttpResponseRedirect(reverse("directory:access_denied"))

    if "q" in request.GET and request.GET["q"]:
        query = request.GET["q"]

        dept = Department.objects.get(id=query)
        user_list = Employee.objects.filter(dept=dept).order_by("first_name", "last_name")

        users = paginate(request, user_list)

        return render(request, "index.html",
                      {"depts": get_all_depts(), "locations": get_all_locations(), "users": users,
                          "query": query, "heading": dept.name, "dept_page": True})


def search_by_location(request):

    # check if directory access allowed
    if not is_logged_in(request):
        return HttpResponseRedirect(reverse("directory:login_employee"))
    if not is_fivestars_employee(request):
        return HttpResponseRedirect(reverse("directory:access_denied"))

    if "q" in request.GET and request.GET["q"]:
        query = request.GET["q"]

        location = Location.objects.get(id=query)
        user_list = Employee.objects.filter(location=location).order_by("first_name", "last_name")

        # add pets
        pet_list = Pet.objects.filter(owner__location=location).order_by("name")
        user_pet_list = sorted(chain(user_list, pet_list), cmp=cmp_location)

        users = paginate(request, user_pet_list)

        return render(request, "index.html",
                      {"depts": get_all_depts(), "locations": get_all_locations(), "users": users,
                          "query": query, "heading": location.name, "location_page": True})


def search_by_email(email):
    """
    Searches for all users with the specified email address.
    """
    return Employee.objects.filter(email__icontains=email)


def search_by_name(first_name, last_name=None):
    """
    Searches for all users with the specified name.
    """

    # If only first name then search by first name. If nothing found search by last name.
    if not last_name:
        users = search_by_first_name(first_name)
        if users:
            return users
        return search_by_last_name(first_name)

    # Search by first name AND last name.
    users = search_by_first_name(first_name)
    if users:
        users = search_by_last_name(last_name, users)
    else:
        users = search_by_last_name(first_name)
        if users:
            users = search_by_last_name(first_name, users)

    return users


def search_by_first_name(first_name, users=None):
    """
    Searches for users with the specified first name.
    :param first_name: the first name to search by
    :param users: if specified search only within these users
    :return: the list of users with the specified first name
    """
    if users:
        return users.filter(first_name__icontains=first_name)
    return Employee.objects.filter(first_name__icontains=first_name)


def search_by_last_name(last_name, users=None):
    """
    Searches for users with the specified last name.
    :param last_name: the last name to search by
    :param users: if specified search only within these users
    :return: the list of users with the specified last name
    """
    if users:
        return users.filter(last_name__icontains=last_name)
    return Employee.objects.filter(last_name__icontains=last_name)


def paginate(request, user_list):
    """
    Paginates the user list into 200 per page.
    :param request: the current request
    :param user_list: the list of users to paginate
    :return: the list of users for the current page
    """

    # Show 200 users per page
    paginator = Paginator(user_list, 200)

    # If page parameter is specified and valid then display that page. If not specified display
    # first page. If not valid display last page.
    page = request.GET.get("page")
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        users = paginator.page(paginator.num_pages)

    return users


def add_pets(users, cmp):
    """
    Adds pets to the list of users and then sorts them using the cmp function.
    """

    # get all pets sorted by name
    pets = Pet.objects.order_by("name")

    # combine the users and pets and sort them
    return sorted(chain(users, pets), cmp=cmp)


def cmp_location(x, y):
    """
    Compares employees with other employees or pets by location.
    """

    # if a pet, use its owner's information for comparison
    if hasattr(x, "owner"):
        x = x.owner
    if hasattr(y, "owner"):
        y = y.owner

    if x.location.name != y.location.name:
        return cmp(x.location.name, y.location.name)

    if x.first_name != y.first_name:
        return cmp(x.first_name, y.first_name)

    return cmp(x.last_name, y.last_name)


def cmp_name(x, y):
    """
    Compares employees with other employees or pets by name.
    """

    # if a pet, use name for first name, owner's last name for last name
    if hasattr(x, "owner"):
        x_first_name = x.name
        x_last_name = x.owner.last_name
    else:
        x_first_name = x.first_name
        x_last_name = x.last_name
    if hasattr(y, "owner"):
        y_first_name = y.name
        y_last_name = y.owner.last_name
    else:
        y_first_name = y.first_name
        y_last_name = y.last_name

    if x_first_name != y_first_name:
        return cmp(x_first_name, y_first_name)

    return cmp(x_last_name, y_last_name)


def cmp_start_date(x, y):
    """
    Compares employees with other employees or pets by start date.
    """

    # if a pet, use its owner's information for comparison
    if hasattr(x, "owner"):
        x = x.owner
    if hasattr(y, "owner"):
        y = y.owner

    if x.start_date != y.start_date:
        return cmp(y.start_date, x.start_date)

    if x.first_name != y.first_name:
        return cmp(x.first_name, y.first_name)

    return cmp(x.last_name, y.last_name)
