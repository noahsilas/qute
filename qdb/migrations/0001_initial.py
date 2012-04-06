# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Quote'
        db.create_table('qdb_quote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('altered_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
        ))
        db.send_create_signal('qdb', ['Quote'])

        # Adding model 'Vote'
        db.create_table('qdb_vote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('altered_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('quote', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qdb.Quote'])),
            ('score', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal('qdb', ['Vote'])

    def backwards(self, orm):
        # Deleting model 'Quote'
        db.delete_table('qdb_quote')

        # Deleting model 'Vote'
        db.delete_table('qdb_vote')

    models = {
        'qdb.quote': {
            'Meta': {'object_name': 'Quote'},
            'altered_at': ('django.db.models.fields.DateTimeField', [], {}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'})
        },
        'qdb.vote': {
            'Meta': {'object_name': 'Vote'},
            'altered_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'quote': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qdb.Quote']"}),
            'score': ('django.db.models.fields.SmallIntegerField', [], {})
        }
    }

    complete_apps = ['qdb']