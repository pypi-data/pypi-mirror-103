# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class PivotTable(Component):
    """A PivotTable component.
PivotTable is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- cols (boolean | number | string | dict | list; optional):
    The cols displayed in the input.

- data (boolean | number | string | dict | list; optional):
    The data displayed in the input.

- label (string; required):
    A label that will be printed when this component is rendered.

- rows (boolean | number | string | dict | list; optional):
    The row displayed in the input.

- value (boolean | number | string | dict | list; optional):
    The value displayed in the input."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, label=Component.REQUIRED, value=Component.UNDEFINED, rows=Component.UNDEFINED, cols=Component.UNDEFINED, data=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'cols', 'data', 'label', 'rows', 'value']
        self._type = 'PivotTable'
        self._namespace = 'pivot_table'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'cols', 'data', 'label', 'rows', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in ['label']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(PivotTable, self).__init__(**args)
