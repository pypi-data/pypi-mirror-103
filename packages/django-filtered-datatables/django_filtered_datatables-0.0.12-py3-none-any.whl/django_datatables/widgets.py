import json
from django.forms import MultipleChoiceField
from django.forms.widgets import Widget
from .datatables import DatatableTable
from .columns import DatatableColumn
from django.utils.safestring import mark_safe

class DataTableWidget(Widget):
    template_name = 'datatables/widgets/multiple_choice.html'

    tick = '<i class="fas fa-check-circle"></i>'
    no_tick = '&nbsp;'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        table = DatatableTable(context['widget']['attrs']['id'], model=self.attrs['table_model'])
        table.table_options.update(self.attrs.get('table_options', {}))
        table.table_options['pageLength'] = 400
        if 'filter' in self.attrs:
            table.filter = self.attrs['filter']
        table.add_columns(*self.attrs['fields'], ColumnTick(column_name='Selected', value=value))
        table.table_classes.append('multi-select')
        table.ajax_data = False
        context['tick'] = self.tick
        context['no_tick'] = self.no_tick
        context['selected_column'] = table.find_column('Selected')[1]
        context['id_column'] = table.find_column('id')[1]
        context['table'] = mark_safe(table.render())
        context['hidden'] = json.dumps(value)
        return context


class ColumnTick(DatatableColumn):

    def row_result(self, data_dict, _page_results):
        if data_dict.get(self.field) in self.kwargs['value']:
            return DataTableWidget.tick
        else:
            return DataTableWidget.no_tick
    def col_setup(self):
        self.field = 'id'


class DataTableMultipleChoiceField(MultipleChoiceField):

    def __init__(self, *,  fields, table_model, **kwargs):
        attrs = {'fields': fields, 'table_model': table_model}
        if 'filter' in kwargs:
            attrs['filter'] = kwargs.pop('filter')
        attrs['table_options'] = kwargs.pop('table_options', {})
        super().__init__(
            widget=DataTableWidget(attrs=attrs))

    def to_python(self, value):
        return super().to_python(json.loads(value))
