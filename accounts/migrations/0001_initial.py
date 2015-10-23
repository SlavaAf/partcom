# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Address'
        db.create_table(u'accounts_address', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.CharField')(default='KZ', max_length=3)),
            ('region', self.gf('django.db.models.fields.CharField')(default='VKO', max_length=4)),
            ('city', self.gf('django.db.models.fields.CharField')(default='UKG', max_length=100)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address_index', self.gf('django.db.models.fields.CharField')(default='070000', max_length=10)),
            ('phones', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('details', self.gf('django.db.models.fields.CharField')(default='', max_length=1000, null=True, blank=True)),
        ))
        db.send_create_signal(u'accounts', ['Address'])

        # Adding model 'UserProfile'
        db.create_table(u'accounts_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, to=orm['auth.User'])),
            ('phone', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('sms_code', self.gf('django.db.models.fields.CharField')(default=0, max_length=100)),
            ('account_type', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'accounts', ['UserProfile'])

        # Adding M2M table for field addresses on 'UserProfile'
        m2m_table_name = db.shorten_name(u'accounts_userprofile_addresses')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm[u'accounts.userprofile'], null=False)),
            ('address', models.ForeignKey(orm[u'accounts.address'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userprofile_id', 'address_id'])

        # Adding model 'Shop'
        db.create_table(u'accounts_shop', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='shop', to=orm['accounts.UserProfile'])),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', unique=True, max_length=50)),
        ))
        db.send_create_signal(u'accounts', ['Shop'])

        # Adding model 'Client'
        db.create_table(u'accounts_client', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='client', to=orm['accounts.UserProfile'])),
        ))
        db.send_create_signal(u'accounts', ['Client'])

        # Adding model 'Chat'
        db.create_table(u'accounts_chat', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'accounts', ['Chat'])

        # Adding M2M table for field users on 'Chat'
        m2m_table_name = db.shorten_name(u'accounts_chat_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('chat', models.ForeignKey(orm[u'accounts.chat'], null=False)),
            ('userprofile', models.ForeignKey(orm[u'accounts.userprofile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['chat_id', 'userprofile_id'])

        # Adding model 'Post'
        db.create_table(u'accounts_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='posts', to=orm['accounts.UserProfile'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('content', self.gf('django.db.models.fields.TextField')(max_length=10000)),
        ))
        db.send_create_signal(u'accounts', ['Post'])

        # Adding model 'PostComment'
        db.create_table(u'accounts_postcomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comments', to=orm['accounts.Post'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='post_comments', to=orm['accounts.UserProfile'])),
            ('answer_to', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='post_answers', null=True, to=orm['accounts.UserProfile'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=10000)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'accounts', ['PostComment'])


    def backwards(self, orm):
        # Deleting model 'Address'
        db.delete_table(u'accounts_address')

        # Deleting model 'UserProfile'
        db.delete_table(u'accounts_userprofile')

        # Removing M2M table for field addresses on 'UserProfile'
        db.delete_table(db.shorten_name(u'accounts_userprofile_addresses'))

        # Deleting model 'Shop'
        db.delete_table(u'accounts_shop')

        # Deleting model 'Client'
        db.delete_table(u'accounts_client')

        # Deleting model 'Chat'
        db.delete_table(u'accounts_chat')

        # Removing M2M table for field users on 'Chat'
        db.delete_table(db.shorten_name(u'accounts_chat_users'))

        # Deleting model 'Post'
        db.delete_table(u'accounts_post')

        # Deleting model 'PostComment'
        db.delete_table(u'accounts_postcomment')


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
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'accounts.postcomment': {
            'Meta': {'object_name': 'PostComment'},
            'answer_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'post_answers'", 'null': 'True', 'to': u"orm['accounts.UserProfile']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': u"orm['accounts.Post']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '10000'}),
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