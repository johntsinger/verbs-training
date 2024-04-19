class GetReadOnlyFieldsMixin:
    """Hide read only fields on creation form but not on change form."""

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing
            return self.readonly_fields
        return ()
