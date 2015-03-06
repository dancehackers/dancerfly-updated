import datetime

from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.crypto import get_random_string
import floppyforms.__future__ as forms

from brambling.models import (Attendee, Event, Item, ItemOption, Discount,
                              Date, ItemImage, Transaction, Invite, CustomForm,
                              CustomFormField)
from brambling.utils.international import clean_postal_code

from zenaida.forms import (GroupedModelMultipleChoiceField,
                           GroupedModelChoiceField)


STATIC_SLUGS = frozenset(('demo-event',))


class EventForm(forms.ModelForm):
    start_date = forms.DateField()
    end_date = forms.DateField()
    disconnect_stripe = forms.BooleanField(required=False)
    disconnect_dwolla = forms.BooleanField(required=False)
    editors = forms.CharField(help_text='Comma-separated email addresses. Each person will be sent an invitation to join the event as an editor.',
                              widget=forms.Textarea,
                              required=False)
    timezone = forms.ChoiceField(choices=(
        ('America/Anchorage', 'America/Anchorage'),
        ('America/Adak', 'America/Adak'),
        ('America/Phoenix', 'America/Phoenix'),
        ('America/Chicago', 'America/Chicago'),
        ('America/New_York', 'America/New_York'),
        ('America/Indiana/Indianapolis', 'America/Indiana/Indianapolis'),
        ('America/Indiana/Knox', 'America/Indiana/Knox'),
        ('America/Detroit', 'America/Detroit'),
        ('America/Denver', 'America/Denver'),
        ('America/Los_Angeles', 'America/Los_Angeles'),
        ('Pacific/Honolulu', 'Pacific/Honolulu'),

    ))

    class Meta:
        model = Event
        # TODO: When multiple countries are supported, add 'country'
        # and 'check_country' and 'currency' to fields.
        fields = ('name', 'slug', 'description', 'website_url', 'banner_image',
                  'city', 'state_or_province', 'timezone', 'start_time',
                  'end_time', 'dance_styles', 'has_dances', 'has_classes',
                  'liability_waiver', 'privacy', 'collect_housing_data',
                  'collect_survey_data', 'cart_timeout',
                  'check_payment_allowed', 'check_payable_to',
                  'check_postmark_cutoff', 'check_recipient', 'check_address',
                  'check_address_2', 'check_city', 'check_state_or_province',
                  'check_zip', 'facebook_url')

    def __init__(self, request, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].initial = getattr(self.instance,
                                                    'start_date',
                                                    datetime.date.today)
        self.fields['end_date'].initial = getattr(self.instance,
                                                  'end_date',
                                                  datetime.date.today)
        if not self.instance.uses_stripe():
            del self.fields['disconnect_stripe']
        if not self.instance.uses_dwolla():
            del self.fields['disconnect_dwolla']
        self.request = request
        if self.instance.pk is None:
            self.instance.owner = request.user
        if not request.user == self.instance.owner:
            del self.fields['editors']

        if self.instance.pk is not None:
            timezone = self.instance.timezone
            if (timezone, timezone) not in self.fields['timezone'].choices:
                self.fields['timezone'].choices += ((timezone, timezone),)

        if self.instance.slug in STATIC_SLUGS:
            del self.fields['slug']

    def clean_editors(self):
        editors = self.cleaned_data['editors']
        if not editors:
            return []

        validator = EmailValidator()
        # Split email list by commas and trim whitespace:
        editors = [x.strip() for x in editors.split(',')]
        for editor in editors:
            validator(editor)
        return editors

    def clean_check_payment_allowed(self):
        cpa = self.cleaned_data['check_payment_allowed']
        if cpa:
            # TODO: When multiple countries are supported, add 'check_country' to this list:
            for field in ('check_payable_to', 'check_postmark_cutoff',
                          'check_recipient', 'check_address',
                          'check_city', 'check_zip', 'check_state_or_province'):
                self.fields[field].required = True
        return cpa

    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        if cleaned_data['start_date'] > cleaned_data['end_date']:
            raise ValidationError("End date must be before or equal to "
                                  "the start date.")
        if 'check_zip' in cleaned_data:
            country = self.instance.check_country
            code = cleaned_data['check_zip']
            try:
                cleaned_data['check_zip'] = clean_postal_code(country, code)
            except ValidationError, e:
                del cleaned_data['check_zip']
                self.add_error('check_zip', e)
        return cleaned_data

    def has_check_errors(self):
        return any((f in self.errors
                    for f in self.fields
                    if f[:6] == ('check_')))

    def save(self):
        created = self.instance.pk is None
        if self.cleaned_data.get('disconnect_stripe'):
            if self.instance.api_type == Event.LIVE:
                self.instance.stripe_user_id = ''
                self.instance.stripe_access_token = ''
                self.instance.stripe_refresh_token = ''
                self.instance.stripe_publishable_key = ''
            else:
                self.instance.stripe_test_user_id = ''
                self.instance.stripe_test_access_token = ''
                self.instance.stripe_test_refresh_token = ''
                self.instance.stripe_test_publishable_key = ''
        if self.cleaned_data.get('disconnect_dwolla'):
            self.instance.clear_dwolla_data(self.instance.api_type)
        instance = super(EventForm, self).save()
        if {'start_date', 'end_date'} & set(self.changed_data) or created:
            cd = self.cleaned_data
            date_set = {cd['start_date'] + datetime.timedelta(n - 1) for n in
                        xrange((cd['end_date'] - cd['start_date']).days + 2)}
            seen = set(Date.objects.filter(date__in=date_set
                                           ).values_list('date', flat=True))
            Date.objects.bulk_create([
                Date(date=date) for date in date_set
                if date not in seen
            ])
            instance.housing_dates = Date.objects.filter(date__in=date_set)
            date_set.remove(cd['start_date'] - datetime.timedelta(1))
            instance.dates = Date.objects.filter(date__in=date_set)
        if self.request.user == instance.owner and self.cleaned_data['editors']:
            for editor in self.cleaned_data['editors']:
                invite, created = Invite.objects.get_or_create_invite(
                    email=editor,
                    user=self.request.user,
                    kind=Invite.EDITOR,
                    content_id=instance.pk
                )
                if created:
                    invite.send(
                        content=instance,
                        secure=self.request.is_secure(),
                        site=get_current_site(self.request),
                    )
        return instance


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ('event',)

    def __init__(self, event, *args, **kwargs):
        self.event = event
        super(ItemForm, self).__init__(*args, **kwargs)

    def _post_clean(self):
        super(ItemForm, self)._post_clean()
        self.instance.event = self.event


class ItemOptionForm(forms.ModelForm):
    class Meta:
        model = ItemOption
        exclude = ()

    def __init__(self, event, *args, **kwargs):
        self.event = event
        super(ItemOptionForm, self).__init__(*args, **kwargs)
        self.fields['available_end'].initial = event.start_date


class BaseItemOptionFormSet(forms.BaseInlineFormSet):
    def __init__(self, event, *args, **kwargs):
        self.event = event
        super(BaseItemOptionFormSet, self).__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        kwargs['event'] = self.event
        return super(BaseItemOptionFormSet, self)._construct_form(i, **kwargs)

    @property
    def empty_form(self):
        form = self.form(
            self.event,
            auto_id=self.auto_id,
            prefix=self.add_prefix('__prefix__'),
            empty_permitted=True,
        )
        self.add_fields(form, None)
        return form


ItemOptionFormSet = forms.inlineformset_factory(
    Item,
    ItemOption,
    form=ItemOptionForm,
    formset=BaseItemOptionFormSet,
    extra=0,
    min_num=1,
    validate_min=True,
)


ItemImageFormSet = forms.inlineformset_factory(
    Item,
    ItemImage,
    extra=0,
    exclude=(),
)


class DiscountForm(forms.ModelForm):
    generated_code = None
    item_options = GroupedModelMultipleChoiceField(
                        queryset=ItemOption.objects.all(),
                        group_by_field="item",
                        group_label=lambda x: x.name)

    class Meta:
        model = Discount
        exclude = ('event',)

    def __init__(self, event, *args, **kwargs):
        self.event = event
        super(DiscountForm, self).__init__(*args, **kwargs)
        self.fields['item_options'].queryset = ItemOption.objects.filter(item__event=event)
        self.fields['available_end'].initial = event.start_date
        if not self.instance.code:
            self.generated_code = get_random_string(6)
            while Discount.objects.filter(event=self.event,
                                          code=self.generated_code).exists():
                self.generated_code = get_random_string(6)
            self.fields['code'].initial = self.generated_code

    def _post_clean(self):
        super(DiscountForm, self)._post_clean()
        self.instance.event = self.event
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            self._update_errors(e)


class CustomFormForm(forms.ModelForm):
    class Meta:
        model = CustomForm
        exclude = ('event',)

    def __init__(self, event, *args, **kwargs):
        self.event = event
        super(CustomFormForm, self).__init__(*args, **kwargs)

    def _post_clean(self):
        super(CustomFormForm, self)._post_clean()
        self.instance.event = self.event


CustomFormFieldFormSet = forms.inlineformset_factory(
    CustomForm,
    CustomFormField,
    extra=0,
    min_num=1,
    exclude=(),
)


class AttendeeFilterSetForm(forms.Form):
    ORDERING_CHOICES = (
        ("surname", "Surname"),
        ("-surname", "Surname (descending)"),
        ("given_name", "Given Name"),
        ("-given_name", "Given Name (descending)"),
    )
    HOUSING_STATUS_CHOICES = (("", "---------"),) + Attendee.HOUSING_STATUS_CHOICES

    # TODO: Automatically generate fields from the parent filterset.
    bought_items__item_option = GroupedModelChoiceField(label="Bought Item",
                    queryset=ItemOption.objects.all(),
                    group_by_field="item",
                    group_label=lambda x: x.name,
                    required=False)
    bought_items__discounts__discount = forms.ModelChoiceField(label="Discount",
                                                               queryset=Discount.objects.all(),
                                                               required=False)
    housing_status = forms.ChoiceField(label="Housing Status",
                                       choices=HOUSING_STATUS_CHOICES,
                                       required=False)
    o = forms.ChoiceField(label="Sort by",
                          choices=ORDERING_CHOICES,
                          required=False)


class ManualPaymentForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('amount', 'method')

    def __init__(self, order, user, *args, **kwargs):
        super(ManualPaymentForm, self).__init__(*args, **kwargs)
        self.fields['method'].choices = Transaction.METHOD_CHOICES[2:]
        self.order = order
        txn = self.instance
        txn.order = order
        txn.event = order.event
        txn.transaction_type = Transaction.PURCHASE
        txn.created_by = user
        txn.is_confirmed = True
        txn.api_type = txn.event.api_type


class ManualDiscountForm(forms.Form):
    discount = forms.ModelChoiceField(Discount)

    def __init__(self, order, *args, **kwargs):
        super(ManualDiscountForm, self).__init__(*args, **kwargs)
        self.fields['discount'].queryset = Discount.objects.filter(event=order.event)
        self.order = order

    def save(self):
        self.order.add_discount(self.cleaned_data['discount'], force=True)
