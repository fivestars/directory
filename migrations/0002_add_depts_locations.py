# -*- coding: utf-8 -*-
from south.v2 import DataMigration


class Migration(DataMigration):

    def forwards(self, orm):
        """
        Adds all the departments and locations to the database.
        :param orm: the object relational model
        """

        # get object relational models
        Department = orm["directory.Department"]
        Location = orm["directory.Location"]

        # create departments
        Department.objects.create(name="Co-Founders")
        Department.objects.create(name="Customer Success")
        Department.objects.create(name="Design")
        Department.objects.create(name="Engineering")
        Department.objects.create(name="Finance")
        Department.objects.create(name="Inside Sales")
        Department.objects.create(name="Marketing")
        Department.objects.create(name="National Sales")
        Department.objects.create(name="Outside Sales")
        Department.objects.create(name="People")
        Department.objects.create(name="Product")
        Department.objects.create(name="Sales Operations")
        Department.objects.create(name="Supply Chain")

        # create locations
        Location.objects.create(name="Chicago")
        Location.objects.create(name="Dallas")
        Location.objects.create(name="Denver")
        Location.objects.create(name="Fort Collins")
        Location.objects.create(name="Houston")
        Location.objects.create(name="Los Angeles")
        Location.objects.create(name="Miami")
        Location.objects.create(name="Michigan")
        Location.objects.create(name="Minneapolis")
        Location.objects.create(name="Phoenix")
        Location.objects.create(name="Portland")
        Location.objects.create(name="San Diego")
        Location.objects.create(name="San Francisco")
        Location.objects.create(name="Seattle")

    def backwards(self, orm):
        """
        Removes all the departments and locations from the database.
        :param orm: the object relational model
        """

        Department = orm["directory.Department"]
        Department.objects.all().delete()
        Location = orm["directory.Location"]
        Location.objects.all().delete()

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
