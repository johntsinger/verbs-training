from django.urls import reverse
from django.utils.html import format_html


def reverse_foreignkey_change_links(
    model,
    get_instances,
    description=None,
    empty_text='(None)'
):
    """
    Generate link to the change form for each object in the
    reverse ForeignKey.
    """
    if not description:
        description = model.__name__ + '(s)'

    def model_change_link_function(_, obj):
        instances = get_instances(obj)
        if not instances:
            return empty_text
        links = []
        for instance in instances:
            if model._meta.proxy:
                change_url = reverse(
                    f'admin:{model._meta.app_label}_'
                    f'{model._meta.model_name}_change',
                    args=(instance.id, )
                )
            else:
                change_url = reverse(
                    f'admin:{model._meta.db_table}_change',
                    args=(instance.id, )
                )
            links.append(
                f'<a href="{change_url}" title="Change">'
                f'{str(instance)}</a>'
            )
        return format_html('</br>'.join(links))

    model_change_link_function.short_description = description
    return model_change_link_function
