# -*- coding: utf-8 -*-
from datetime import date

import mock
import pytest
from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from django.utils.encoding import force_text

from barbeque.exporter import Exporter, action_export_factory
from barbeque.tests.resources.mockapp.models import MockModel, RelatedMockModel


@pytest.mark.django_db
class TestExporter:
    def setup(self):
        self.exporter = Exporter('csv', None, ('id', 'parent__id', 'value'), True)

        self.modeladmin = admin.ModelAdmin(RelatedMockModel, admin.site)

        parent = MockModel.objects.create()
        for i in range(0, 3):
            RelatedMockModel.objects.create(parent=parent, value='汉')
        self.objects = RelatedMockModel.objects.all().order_by('pk')

    def test_get_filename(self):
        expected = 'mockapp_relatedmockmodel_%s.csv' % date.today().strftime('%Y-%m-%d')
        assert self.exporter.get_filename(self.modeladmin) == expected

        self.exporter.export_type = 'xlsx'
        expected = 'mockapp_relatedmockmodel_%s.xlsx' % date.today().strftime('%Y-%m-%d')
        assert self.exporter.get_filename(self.modeladmin) == expected

    def test_get_header(self):
        assert self.exporter.get_header(self.objects) == [
            'ID',
            'ID',  # Parent id
            'value'
        ]

    def test_get_header_unknown_field(self):
        self.exporter.fields += ('unknown_field',)
        assert self.exporter.get_header(self.objects) == [
            'ID',
            'ID',  # Parent id
            'value',
            'unknown_field'
        ]

    def test_get_data(self):
        data = self.exporter.get_data(self.objects)
        assert data[0] == self.exporter.fields
        assert len(data[1]) == len(self.objects)

    def test_export_csv(self, rf):
        response = self.exporter.export_as_csv(self.modeladmin, rf.get('/'), self.objects)
        assert response['Content-type'] == 'text/csv'

        lines = force_text(response.content).split('\n')

        # Test header
        assert 'ID' in lines[0]

        # Test data
        for i, obj in enumerate(self.objects, start=1):
            assert lines[i].startswith(str(obj.pk))

    def test_export_xlsx(self, rf):
        response = self.exporter.export_as_xlsx(self.modeladmin, rf.get('/'), self.objects)
        exp = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        assert response['Content-type'] == exp

    def test_export_csv_no_header(self, rf):
        self.exporter.header = False
        response = self.exporter.export_as_csv(self.modeladmin, rf.get('/'), self.objects)
        assert response['Content-type'] == 'text/csv'

        lines = force_text(response.content).split('\n')
        assert 'ID' not in lines[0]

    def test_export_csv_unicode(self, rf):
        response = self.exporter.export_as_csv(self.modeladmin, rf.get('/'), self.objects)
        assert response['Content-type'] == 'text/csv'

        lines = force_text(response.content).split('\n')
        assert lines == [u'ID,ID,value\r', u'1,1,\u6c49\r', u'2,1,\u6c49\r', u'3,1,\u6c49\r', u'']

    def test_factory(self):
        func = action_export_factory('csv')
        assert func.__name__ == 'export_csv_func'

        func = action_export_factory('xlsx')
        assert func.__name__ == 'export_xlsx_func'

        with pytest.raises(ImproperlyConfigured):
            action_export_factory('test')

    @mock.patch('barbeque.exporter.Exporter.export_as_xlsx')
    @mock.patch('barbeque.exporter.Exporter.export_as_csv')
    def test_factory_call_csv(self, func_mock, func_mock2):
        func = action_export_factory('csv')
        func()
        assert func_mock.call_count == 1
        assert func_mock2.call_count == 0

    @mock.patch('barbeque.exporter.Exporter.export_as_xlsx')
    @mock.patch('barbeque.exporter.Exporter.export_as_csv')
    def test_factory_call_xlsx(self, func_mock, func_mock2):
        func = action_export_factory('xlsx')
        func()
        assert func_mock.call_count == 0
        assert func_mock2.call_count == 1
