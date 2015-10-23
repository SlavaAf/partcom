# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'PostComment.created'
        db.delete_column(u'accounts_postcomment', 'created')

        # Adding field 'PostComment.ts_created'
        db.add_column(u'accounts_postcomment', 'ts_created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 8, 19, 0, 0), auto_now_add=True, blank=True),
                      keep_default=False)

        # Deleting field 'Post.created'
        db.delete_column(u'accounts_post', 'created')

        # Deleting field 'Post.changed'
        db.delete_column(u'accounts_post', 'changed')

        # Adding field 'Post.ts_created'
        db.add_column(u'accounts_post', 'ts_created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 8, 19, 0, 0), auto_now_add=True, blank=True),
                      keep_default=False)

        # Adding field 'Post.ts_changed'
        db.add_column(u'accounts_post', 'ts_changed',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 8, 19, 0, 0), auto_now=True, auto_now_add=True, blank=True),
                      keep_default=False)

        # Adding field 'Post.ts_public'
        db.add_column(u'accounts_post', 'ts_public',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 8, 19, 0, 0)),
                      keep_default=False)

        # Adding field 'Post.is_public'
        db.add_column(u'accounts_post', 'is_public',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'PostComment.created'
        db.add_column(u'accounts_postcomment', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 8, 13, 0, 0), auto_now_add=True, blank=True),
                      keep_default=False)

        # Deleting field 'PostComment.ts_created'
        db.delete_column(u'accounts_postcomment', 'ts_created')

        # Adding field 'Post.created'
        db.add_column(u'accounts_post', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 8, 13, 0, 0), auto_now_add=True, blank=True),
                      keep_default=False)

        # Adding field 'Post.changed'
        db.add_column(u'accounts_post', 'changed',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 8, 13, 0, 0), auto_now=True, auto_now_add=True, blank=True),
                      keep_default=False)

        # Deleting field 'Post.ts_created'
        db.delete_column(u'accounts_post', 'ts_created')

        # Deleting field 'Post.ts_changed'
        db.delete_column(u'accounts_post', 'ts_changed')

        # Deleting field 'Post.ts_public'
        db.delete_column(u'accounts_post', 'ts_public')

        # Deleting field 'Post.is_public'
        db.delete_column(u'accounts_post', 'is_public')


    models = {
        u'accounts.address': {
            'Meta': {'ordering': "['country', 'region', 'city', 'address', 'pk']", 'object_name': 'Address'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'address_index': ('django.db.models.fields.CharField', [], {'default': "'070000'", 'max_length': '10'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "'UKG'", 'max_length': '100'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'KZ'", 'max_length': '3'}),
            'details': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phones': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'region': ('django.db.models.fields.CharField', [], {'default': "'VKO'", 'max_length': '4'})
        },
        u'accounts.chat': {
            'Meta': {'object_name': 'Chat'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'chats'", 'symmetrical': 'False', 'to': u"orm['accounts.UserProfile']"})
        },
        u'accounts.client': {
            'Meta': {'object_name': 'Client'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'client'", 'to': u"orm['accounts.UserProfile']"})
        },
        u'accounts.post': {
            'Meta': {'object_name': 'Post'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'to': u"orm['accounts.UserProfile']"}),
            'content': ('django.db.models.fields.TextField', [], {'max_length': '10000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ts_changed': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 19, 0, 0)', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'ts_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 19, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'ts_public': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 19, 0, 0)'})
        },
        u'accounts.postcomment': {
            'Meta': {'object_name': 'PostComment'},
            'answer_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'post_answers'", 'null': 'True', 'to': u"orm['accounts.UserProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': u"orm['accounts.Post']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '10000'}),
            'ts_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 19, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'post_comments'", 'to': u"orm['accounts.UserProfile']"})
        },
        u'accounts.shop': {
            'Meta': {'object_name': 'Shop'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parts': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'shops'", 'symmetrical': 'False', 'through': u"orm['catalog.PartsInShop']", 'to': u"orm['catalog.Part']"}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shop'", 'to': u"orm['accounts.UserProfile']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'unique': 'True', 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'accounts.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'account_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'addresses': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'profiles'", 'null': 'True', 'to': u"orm['accounts.Address']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'sms_code': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '100'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'catalog.part': {
            'Meta': {'object_name': 'Part'},
            'article': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'})
        },
        u'catalog.partsinshop': {
            'Meta': {'object_name': 'PartsInShop'},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'part': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ps_parts'", 'to': u"orm['catalog.Part']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ps_shops'", 'to': u"orm['accounts.Shop']"}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['accounts']