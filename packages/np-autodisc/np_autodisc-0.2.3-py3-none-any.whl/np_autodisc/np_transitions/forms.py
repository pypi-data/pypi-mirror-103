from django import forms
from django.conf import settings


class FilterChoiceIterator(forms.models.ModelChoiceIterator):

    def __iter__(self):
        # Filter on "empty" choice using FILTERS_NULL_CHOICE_VALUE (instead of an empty string)
        if self.field.null_label is not None:
            yield (settings.FILTERS_NULL_CHOICE_VALUE, self.field.null_label)
        queryset = self.queryset.all()

        # Can't use iterator() when queryset uses prefetch_related()
        if not queryset._prefetch_related_lookups:
            queryset = queryset.iterator()
        for obj in queryset:
            yield self.choice(obj)

class FilterChoiceFieldMixin(object):
    iterator = FilterChoiceIterator

    def __init__(self, null_label = None, count_attr = 'filter_count', *args, **kwargs):
        self.null_label = null_label
        self.count_attr = count_attr
        if 'required' not in kwargs:
            kwargs['required'] = False
        if 'widget' not in kwargs:
            kwargs['widget'] = forms.SelectMultiple(attrs = {'size': 6})
        super().__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        label = super().label_from_instance(obj)
        obj_count = getattr(obj, self.count_attr, None)
        if obj_count is not None:
            return f"{label} ({obj_count})"
        return label

class FilterChoiceField(FilterChoiceFieldMixin, forms.ModelMultipleChoiceField):
    pass
