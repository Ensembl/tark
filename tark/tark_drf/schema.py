"""Expose existing filter field descriptions through the OpenAPI generator."""

from drf_spectacular.extensions import OpenApiFilterExtension


class TarkFilterExtension(OpenApiFilterExtension):
    target_class = 'rest_framework.filters.BaseFilterBackend'
    match_subclasses = True
    # Let extensions for other filter libraries take precedence.
    priority = -1

    def get_schema_operation_parameters(self, auto_schema):
        if not hasattr(self.target, 'get_schema_fields'):
            return self.target.get_schema_operation_parameters(auto_schema.view)

        parameters = []
        for field in self.target.get_schema_fields(auto_schema.view):
            parameter = {
                'name': field.name,
                'in': field.location,
                'required': field.required or field.location == 'path',
                'description': field.description or '',
                'schema': {'type': field.type or 'string'},
            }
            if field.example is not None:
                parameter['example'] = field.example
            parameters.append(parameter)
        return parameters
