# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Department'
        db.create_table(u'directory_department', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
        ))
        db.send_create_signal(u'directory', ['Department'])

        # Adding model 'Location'
        db.create_table(u'directory_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
        ))
        db.send_create_signal(u'directory', ['Location'])

        # Adding model 'Employee'
        db.create_table(u'directory_employee', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
            ('dept', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['directory.Department'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('phone_num', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['directory.Location'])),
            ('email', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('birthday', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('spirit_animal', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('buddy', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('image_url', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal(u'directory', ['Employee'])


    def backwards(self, orm):
        # Deleting model 'Department'
        db.delete_table(u'directory_department')

        # Deleting model 'Location'
        db.delete_table(u'directory_location')

        # Deleting model 'Employee'
        db.delete_table(u'directory_employee')


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