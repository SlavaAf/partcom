# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Delivery'
        db.create_table(u'delivery_delivery', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client_del', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='dd_client', null=True, to=orm['accounts.UserProfile'])),
            ('payment', self.gf('django.db.models.fields.CharField')(default=0, max_length=10)),
            ('shipping', self.gf('django.db.models.fields.CharField')(default=0, max_length=10)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=2)),
        ))
        db.send_create_signal(u'delivery', ['Delivery'])

        # Adding model 'PartInDelivery'
        db.create_table(u'delivery_partindelivery', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('part_del', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='ps_del', null=True, blank=True, to=orm['delivery.Delivery'])),
            ('part_in_shop', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='ps_part_in_del', null=True, blank=True, to=orm['catalog.PartsInShop'])),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=100)),
        ))
        db.send_create_signal(u'delivery', ['PartInDelivery'])

        # Adding M2M table for field del_in_shop on 'PartInDelivery'
        m2m_table_name = db.shorten_name(u'delivery_partindelivery_del_in_shop')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('partindelivery', models.ForeignKey(orm[u'delivery.partindelivery'], null=False)),
            ('shop', models.ForeignKey(orm[u'accounts.shop'], null=False))
        ))
        db.create_unique(m2m_table_name, ['partindelivery_id', 'shop_id'])


    def backwards(self, orm):
        # Deleting model 'Delivery'
        db.delete_table(u'delivery_delivery')

        # Deleting model 'PartInDelivery'
        db.delete_table(u'delivery_partindelivery')

        # Removing M2M table for field del_in_shop on 'PartInDelivery'
        db.delete_table(db.shorten_name(u'delivery_partindelivery_del_in_shop'))


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
        },
        u'delivery.delivery': {
            'Meta': {'object_name': 'Delivery'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '2'}),
            'client_del': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'dd_client'", 'null': 'True', 'to': u"orm['accounts.UserProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parts_in_del': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'dd_parts'", 'symmetrical': 'False', 'through': u"orm['delivery.PartInDelivery']", 'to': u"orm['catalog.PartsInShop']"}),
            'payment': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '10'}),
            'shipping': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '10'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'delivery.partindelivery': {
            'Meta': {'object_name': 'PartInDelivery'},
            'del_in_shop': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'pd_dis'", 'default': 'None', 'to': u"orm['accounts.Shop']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'part_del': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'ps_del'", 'null': 'True', 'blank': 'True', 'to': u"orm['delivery.Delivery']"}),
            'part_in_shop': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'ps_part_in_del'", 'null': 'True', 'blank': 'True', 'to': u"orm['catalog.PartsInShop']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '100'})
        }
    }

    complete_apps = ['delivery']