from datetime import date

from django.db.models import CharField, DateField, ForeignKey, Model


class Department(Model):
    """
    Department model for FiveStars internal directory
    """
    name = CharField("Name", max_length=32, db_index=True)

    def __unicode__(self):
        return self.name


class Location(Model):
    """
    Location model for FiveStars internal directory
    """
    name = CharField("Name", max_length=32, db_index=True)

    def __unicode__(self):
        return self.name


class Employee(Model):
    """
    Employee model for FiveStars internal directory
    """
    first_name = CharField("First Name", max_length=32, db_index=True)
    last_name = CharField("Last Name", max_length=32, db_index=True)
    dept = ForeignKey(Department)
    title = CharField(max_length=64)
    phone_num = CharField("Phone Number", max_length=12)
    location = ForeignKey(Location)
    email = CharField(max_length=64, unique=True)
    start_date = DateField("Start Date")
    birthday = DateField(null=True, blank=True)
    spirit_animal = CharField("Spirit Animal", max_length=32, null=True, blank=True)
    buddy = CharField(max_length=32, null=True, blank=True)
    image_url = CharField("Image URL", max_length=256, null=True, blank=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    @property
    def is_new(self):
        """
        Is the employee new, i.e. started within the past 30 days?
        :return: true if the employee is new; false otherwise
        """
        return (date.today() - self.start_date).days < 30

    @property
    def is_birthday_today(self):
        """
        Is the employee's birthday today?
        :return: true if the employee's birthday is today; false otherwise
        """
        return self.birthday.month == date.today().month and self.birthday.day == date.today().day


class Pet(Model):
    """
    Pet model for FiveStars internal directory
    """
    name = CharField("Name", max_length=32, db_index=True)
    owner = ForeignKey(Employee)
    hobbies = CharField("Favorite Hobbies", max_length=256, null=True, blank=True)
    dislikes = CharField("Least Favorite Things", max_length=256, null=True, blank=True)
    image_url = CharField("Image URL", max_length=256, null=True, blank=True)

    def __unicode__(self):
        return self.name
