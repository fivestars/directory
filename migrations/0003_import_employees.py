# -*- coding: utf-8 -*-
import csv
import datetime
from south.v2 import DataMigration


class Migration(DataMigration):

    def forwards(self, orm):
        """
        Imports the employees from the CSV file into the database.
        :param orm: the object relational model
        """

        # get object relational models
        Department = orm["directory.Department"]
        Location = orm["directory.Location"]
        Employee = orm["directory.Employee"]

        # read employees CSV
        with open("loyalty/directory/migrations/0003_employees.csv", "rb") as ff:
            reader = csv.reader(ff)

            # skip the header
            next(reader, None)

            for row in reader:

                # get department
                dept = Department.objects.get(name=row[3])

                # get location
                location = Location.objects.get(name=row[6])

                # parse start date
                start_date = datetime.datetime.strptime(row[8], "%m/%d/%Y")

                # parse birthday if it exists and assume year 1904
                if row[9]:
                    birthday = datetime.datetime.strptime(row[9] + "-1994", "%d-%b-%Y")
                else:
                    birthday = None

                # import employee
                Employee.objects.create(
                    first_name=row[1],
                    last_name=row[2],
                    dept=dept,
                    title=row[4],
                    phone_num=row[5],
                    location=location,
                    email=row[7],
                    start_date=start_date,
                    birthday=birthday,
                    spirit_animal=row[10],
                    buddy=row[11],
                    image_url=row[0]
                )

    def backwards(self, orm):
        """
        Removes all the employees from the database.
        :param orm: the object relational model
        """
        Employee = orm["directory.Employee"]
        Employee.objects.all().delete()

    models = {
        u'directory.department': {
            'Meta': {'object_name': 'Department'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'})
        },
        u'directory.employee': {
            'Meta': {'object_name': 'Employee'},
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'buddy': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'dept': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['directory.Department']"}),
            'email': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['directory.Location']"}),
            'phone_num': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'spirit_animal': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'directory.location': {
            'Meta': {'object_name': 'Location'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'})
        }
    }

    complete_apps = ['directory']
    symmetrical = True
