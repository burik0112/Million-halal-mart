from typing import Any
from django import forms
from django.forms import ClearableFileInput
from apps.product.models import (
    Phone,
    ProductItem,
    SubCategory,
    Image,
    Ticket,
    Good,
    Category,
)
from django.core.validators import MinValueValidator
from apps.customer.models import News, Banner
from apps.merchant.models import Information, Service, Bonus, SocialMedia
from django.utils import timezone
from ckeditor.widgets import CKEditorWidget


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"].update(
            {
                "class": "form-control",
                "multiple": True,
            }
        )
        super(MultipleFileInput, self).__init__(*args, **kwargs)


class MultipleFileField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class PhoneProductItemForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = ["model_name", "ram", "storage",
                  "category", "color", "condition"]
        widgets = {
            "model_name": forms.TextInput(attrs={"class": "form-control"}),
            "ram": forms.Select(attrs={"class": "form-control"}),
            "storage": forms.Select(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "color": forms.Select(attrs={"class": "form-control"}),
            "condition": forms.Select(attrs={"class": "form-control"}),
            # Add more fields here
        }

    # Fields for ProductItem
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(main_type="p"),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    desc_uz = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )
    desc_ru = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )
    desc_en = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )
    desc_kr = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )
    new_price = forms.DecimalField(
        decimal_places=0,
        max_digits=10,
        required=False,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    # Eski narx maydoni (agar kerak bo'lsa)
    old_price = forms.DecimalField(
        decimal_places=0,
        max_digits=10,
        required=False,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    available_quantity = forms.IntegerField(
        min_value=0, widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    # stock = forms.IntegerField(
    #     widget=forms.NumberInput(attrs={"class": "form-control"}),
    #     required=False,
    #     initial=0,
    # )
    # bonus = forms.IntegerField(
    #     widget=forms.NumberInput(attrs={"class": "form-control"}),
    #     required=False,
    #     initial=0,
    # )
    active = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}), initial=True
    )
    images = (
        MultipleFileField()
    )  # New field for multiple images # New field for multiple images

    def save(self, commit=True):
        phone = super().save(commit=False)
        product_item = ProductItem(
            desc_uz=self.cleaned_data["desc_uz"],
            desc_ru=self.cleaned_data["desc_ru"],
            desc_en=self.cleaned_data["desc_en"],
            desc_kr=self.cleaned_data["desc_kr"],
            new_price=self.cleaned_data["new_price"],
            old_price=self.cleaned_data.get("old_price"),
            available_quantity=self.cleaned_data["available_quantity"],
            # stock=self.cleaned_data["stock"],
            # bonus=self.cleaned_data["bonus"],
            active=self.cleaned_data["active"],
        )
        if commit:
            product_item.save()
            phone.product = product_item
            # Category field added
            phone.category = self.cleaned_data["category"]
            phone.save()

            # Save multiple images
            for img in self.files.getlist("images"):
                image = Image(
                    image=img,
                    name=f"{self.cleaned_data['model_name']}_{img.name}",
                    product=product_item,
                )
                image.save()
        return phone


class PhoneCategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        exclude = ["main_type"]
        widgets = {
            # 'main_type': forms.Select(attrs={'class': 'form-control'}),
            "name_uz": forms.TextInput(attrs={"class": "form-control"}),
            "name_ru": forms.TextInput(attrs={"class": "form-control"}),
            "name_en": forms.TextInput(attrs={"class": "form-control"}),
            "name_kr": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            # "desc": forms.Textarea(attrs={"class": "form-control"}),
            # "stock": forms.NumberInput(attrs={"class": "form-control"}),
            # "bonus": forms.NumberInput(attrs={"class": "form-control"}),
            "active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "name_uz": "Name (Uzbek)",
            "name_ru": "Name (Russian)",
            "name_en": "Name (English)",
            "name_kr": "Name (Korean)",
        }
        required = {
            "name_uz": True,
            "name_ru": True,
            "name_en": True,
            "name_kr": True,
        }

    def __init__(self, *args, **kwargs):
        super(PhoneCategoryCreateForm, self).__init__(*args, **kwargs)

        # Set required attribute for each field
        self.fields["name_uz"].required = True
        self.fields["name_ru"].required = True
        self.fields["name_en"].required = True
        self.fields["name_kr"].required = True


class PhoneEditForm(forms.ModelForm):
    product_desc_uz = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )
    product_desc_ru = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )
    product_desc_en = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )
    product_desc_kr = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )
    product_old_price = forms.DecimalField(
        decimal_places=0,
        max_digits=10,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    product_new_price = forms.DecimalField(
        decimal_places=0,
        max_digits=10,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    product_measure = forms.ChoiceField(
        choices=ProductItem.CHOICES, widget=forms.Select(
            attrs={"class": "form-select"})
    )
    product_available_quantity = forms.IntegerField(
        min_value=0, widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    images = MultipleFileField(required=False)
    # product_bonus = forms.IntegerField(
    #     min_value=0, widget=forms.NumberInput(attrs={"class": "form-control"})
    # )
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(main_type="p"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    product_active = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    class Meta:
        model = Phone
        fields = [
            "model_name",
            "color",
            "condition",
            "ram",
            "storage",
            "category",
            "images",
            "product_old_price",
            "product_new_price",
            "product_measure",
            "product_available_quantity",
            "product_desc_uz",
            "product_desc_ru",
            "product_desc_en",
            "product_desc_kr",
            "product_active",
        ]
        widgets = {
            "model_name": forms.TextInput(attrs={"class": "form-control"}),
            "color": forms.Select(attrs={"class": "form-select"}),
            "condition": forms.Select(attrs={"class": "form-select"}),
            "ram": forms.Select(attrs={"class": "form-select"}),
            "storage": forms.Select(attrs={"class": "form-select"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "images": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super(PhoneEditForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.product:
            product = self.instance.product
            self.fields["product_old_price"].initial = product.old_price
            self.fields["product_new_price"].initial = product.new_price
            self.fields["product_measure"].initial = product.measure
            self.fields[
                "product_available_quantity"
            ].initial = product.available_quantity
            self.fields["product_desc_uz"].initial = product.desc_uz
            self.fields["product_desc_ru"].initial = product.desc_ru
            self.fields["product_desc_en"].initial = product.desc_en
            self.fields["product_desc_kr"].initial = product.desc_kr
            self.fields["product_active"].initial = product.active

    def save(self, commit=True):
        phone = super(PhoneEditForm, self).save(commit=False)
        if not phone.product_id:
            phone.product = ProductItem()
        product_item = phone.product
        product_item.old_price = self.cleaned_data["product_old_price"]
        product_item.new_price = self.cleaned_data["product_new_price"]
        product_item.measure = self.cleaned_data["product_measure"]
        product_item.available_quantity = self.cleaned_data[
            "product_available_quantity"
        ]
        # product_item.stock = self.cleaned_data["product_stock"]
        # product_item.bonus = self.cleaned_data["product_bonus"]
        product_item.desc_uz = self.cleaned_data["product_desc_uz"]
        product_item.desc_ru = self.cleaned_data["product_desc_ru"]
        product_item.desc_en = self.cleaned_data["product_desc_en"]
        product_item.desc_kr = self.cleaned_data["product_desc_kr"]
        product_item.active = self.cleaned_data["product_active"]
        if commit:
            product_item.save()
            phone.product = product_item

            # Update ticket category
            phone.category = self.cleaned_data["category"]

            # Save the phone
            phone.save()

            # Save or update multiple images
            existing_images = phone.product.images.all()

            # Delete existing images if not present in the form data
            form_images = self.files.getlist("images")
            if form_images:
                for existing_image in existing_images:
                    if existing_image.image.name not in form_images:
                        existing_image.delete()

                # Save new images
                for img in form_images:
                    image = Image(
                        image=img,
                        name=f"{self.cleaned_data['model_name']}_{img.name}",
                        product=product_item,
                    )
                    image.save()
        return phone


class TicketCategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name_uz", "name_ru", "name_en",
                  "name_kr", "image", "desc", "active"]
        widgets = {
            # 'main_type': forms.Select(attrs={'class': 'form-control'}),
            "name_uz": forms.TextInput(attrs={"class": "form-control"}),
            "name_ru": forms.TextInput(attrs={"class": "form-control"}),
            "name_en": forms.TextInput(attrs={"class": "form-control"}),
            "name_kr": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            # "desc": forms.Textarea(attrs={"class": "form-control"}),
            # "stock": forms.NumberInput(attrs={"class": "form-control"}),
            # "bonus": forms.NumberInput(attrs={"class": "form-control"}),
            "active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "name_uz": "Name (Uzbek)",
            "name_ru": "Name (Russian)",
            "name_en": "Name (English)",
            "name_kr": "Name (Korean)",
        }
        required = {
            "name_uz": True,
            "name_ru": True,
            "name_en": True,
            "name_kr": True,
        }

    def __init__(self, *args, **kwargs):
        super(TicketCategoryCreateForm, self).__init__(*args, **kwargs)

        # Set required attribute for each field
        self.fields["name_uz"].required = True
        self.fields["name_ru"].required = True
        self.fields["name_en"].required = True
        self.fields["name_kr"].required = True


class TicketProductItemForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["event_name_uz", "event_name_ru",
                  "event_name_en", "event_name_kr"]
        widgets = {
            "category": forms.Select(attrs={"class": "form-control"}),
            "event_name_uz": forms.TextInput(attrs={"class": "form-control"}),
            "event_name_ru": forms.TextInput(attrs={"class": "form-control"}),
            "event_name_en": forms.TextInput(attrs={"class": "form-control"}),
            "event_name_kr": forms.TextInput(attrs={"class": "form-control"}),
        }

    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(main_type="t"),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    event_date = forms.DateTimeField(
        input_formats=["%Y-%m-%d"],  # Adjust the format as needed
        widget=forms.DateTimeInput(
            attrs={"type": "date", "class": "form-control"}),
    )
    desc_uz = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )
    desc_ru = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )
    desc_en = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )
    desc_kr = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )
    new_price = forms.DecimalField(
        decimal_places=0,
        max_digits=10,
        required=False,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    # Eski narx maydoni (agar kerak bo'lsa)
    old_price = forms.DecimalField(
        decimal_places=0,
        max_digits=10,
        required=False,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    available_quantity = forms.IntegerField(
        min_value=0, widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    active = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}), initial=True
    )
    images = (
        MultipleFileField()
    )  # New field for multiple images # New field for multiple images

    def save(self, commit=True):
        ticket = super().save(commit=False)
        product_item = ProductItem(
            desc_uz=self.cleaned_data["desc_uz"],
            desc_ru=self.cleaned_data["desc_ru"],
            desc_en=self.cleaned_data["desc_en"],
            desc_kr=self.cleaned_data["desc_kr"],
            new_price=self.cleaned_data["new_price"],
            old_price=self.cleaned_data.get("old_price"),
            available_quantity=self.cleaned_data["available_quantity"],
            active=self.cleaned_data["active"],
        )
        if commit:
            product_item.save()
            ticket.product = product_item
            # Category field added
            ticket.category = self.cleaned_data["category"]
            ticket.save()

            # Save multiple images
            for img in self.files.getlist("images"):
                image = Image(
                    image=img,
                    name=f"{self.cleaned_data['event_name_uz']}_{img.name}",
                    product=product_item,
                )
                image.save()
        return ticket


class TicketEditForm(forms.ModelForm):
    product_desc_uz = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )
    product_desc_ru = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )
    product_desc_en = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )
    product_desc_kr = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )
    product_new_price = forms.DecimalField(
        decimal_places=0,
        max_digits=10,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    product_old_price = forms.DecimalField(
        decimal_places=0,
        max_digits=10,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    images = MultipleFileField(required=False)
    product_available_quantity = forms.IntegerField(
        min_value=0, widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(main_type="t"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    product_active = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    class Meta:
        model = Ticket
        exclude = ["event_date"]
        fields = [
            "event_name_uz",
            "event_name_ru",
            "event_name_en",
            "event_name_kr",
            "event_date",
            "category",
            "images",
            "product_old_price",
            "product_new_price",
            "product_available_quantity",
            "product_desc_uz",
            "product_desc_ru",
            "product_desc_en",
            "product_desc_kr",
            "product_active",
        ]
        widgets = {
            "event_name_uz": forms.TextInput(attrs={"class": "form-control"}),
            "event_name_en": forms.TextInput(attrs={"class": "form-control"}),
            "event_name_ru": forms.TextInput(attrs={"class": "form-control"}),
            "event_name_kr": forms.TextInput(attrs={"class": "form-control"}),
            "event_date": forms.Select(attrs={"class": "form-select"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "product_desc_uz": forms.TextInput(attrs={"class": "form-control"}),
            "product_desc_ru": forms.TextInput(attrs={"class": "form-control"}),
            "product_desc_en": forms.TextInput(attrs={"class": "form-control"}),
            "product_desc_kr": forms.TextInput(attrs={"class": "form-control"}),
            "images": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super(TicketEditForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.product:
            product = self.instance.product
            self.fields["product_desc_uz"].initial = product.desc_uz
            self.fields["product_desc_ru"].initial = product.desc_ru
            self.fields["product_desc_en"].initial = product.desc_en
            self.fields["product_desc_kr"].initial = product.desc_kr
            self.fields["product_old_price"].initial = product.old_price
            self.fields["product_new_price"].initial = product.new_price
            self.fields[
                "product_available_quantity"
            ].initial = product.available_quantity
            self.fields["product_active"].initial = product.active

    def save(self, commit=True):
        ticket = super(TicketEditForm, self).save(commit=False)

        if not ticket.product_id:
            # If there is no product associated with the ticket, create a new one
            ticket.product = ProductItem()

        # Populate the product fields with form data
        product_item = ticket.product
        product_item.desc_uz = self.cleaned_data["product_desc_uz"]
        product_item.desc_ru = self.cleaned_data["product_desc_ru"]
        product_item.desc_en = self.cleaned_data["product_desc_en"]
        product_item.desc_kr = self.cleaned_data["product_desc_kr"]
        product_item.new_price = self.cleaned_data["product_old_price"]
        product_item.new_price = self.cleaned_data["product_new_price"]
        product_item.available_quantity = self.cleaned_data[
            "product_available_quantity"
        ]
        product_item.active = self.cleaned_data["product_active"]

        if commit:
            product_item.save()
            ticket.product = product_item

            # Update ticket category
            ticket.category = self.cleaned_data["category"]

            # Save the ticket
            ticket.save()

            # Save or update multiple images
            existing_images = ticket.product.images.all()

            # Delete existing images if not present in the form data
            form_images = self.files.getlist("images")
            if form_images:
                for existing_image in existing_images:
                    if existing_image.image.name not in form_images:
                        existing_image.delete()

                # Save new images
                for img in form_images:
                    image = Image(
                        image=img,
                        name=f"{self.cleaned_data['event_name_uz']}_{img.name}",
                        product=product_item,
                    )
                    image.save()

        return ticket


class GoodMainCategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name_uz", "name_ru", "name_en",
                  "name_kr", "image", "active"]
        widgets = {
            "name_uz": forms.TextInput(attrs={"class": "form-control"}),
            "name_ru": forms.TextInput(attrs={"class": "form-control"}),
            "name_en": forms.TextInput(attrs={"class": "form-control"}),
            "name_kr": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            # "stock": forms.NumberInput(attrs={"class": "form-control"}),
            # "bonus": forms.NumberInput(attrs={"class": "form-control"}),
            "active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "name_uz": "Name (Uzbek)",
            "name_ru": "Name (Russian)",
            "name_en": "Name (English)",
            "name_kr": "Name (Korean)",
        }
        required = {
            "name_uz": True,
            "name_ru": True,
            "name_en": True,
            "name_kr": True,
        }

    def __init__(self, *args, **kwargs):
        super(GoodMainCategoryCreateForm, self).__init__(*args, **kwargs)

        # Set required attribute for each field
        self.fields["name_uz"].required = True
        self.fields["name_ru"].required = True
        self.fields["name_en"].required = True
        self.fields["name_kr"].required = True

        # Filter the category queryset to main_type='f'
        if "category" in self.fields:
            self.fields["category"].queryset = Category.objects.filter(
                main_type="f")

    def save(self, commit=True):
        # Save the category with main_type='f'
        instance = super(GoodMainCategoryCreateForm, self).save(commit=False)
        instance.main_type = "f"
        if commit:
            instance.save()
        return instance


class GoodCategoryCreateForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(main_type="f"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = SubCategory
        fields = [
            "name_uz",
            "name_ru",
            "name_en",
            "name_kr",
            "image",
            "category",
            "active",
        ]
        widgets = {
            "name_uz": forms.TextInput(attrs={"class": "form-control"}),
            "name_ru": forms.TextInput(attrs={"class": "form-control"}),
            "name_en": forms.TextInput(attrs={"class": "form-control"}),
            "name_kr": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "name_uz": "Name (Uzbek)",
            "name_ru": "Name (Russian)",
            "name_en": "Name (English)",
            "name_kr": "Name (Korean)",
        }
        required = {
            "name_uz": True,
            "name_ru": True,
            "name_en": True,
            "name_kr": True,
        }

    def __init__(self, *args, **kwargs):
        super(GoodCategoryCreateForm, self).__init__(*args, **kwargs)

        # Set required attribute for each field
        self.fields["name_uz"].required = True
        self.fields["name_ru"].required = True
        self.fields["name_en"].required = True
        self.fields["name_kr"].required = True

    def save(self, commit=True):
        instance = super(GoodCategoryCreateForm, self).save(commit=False)
        instance.main_type = "f"

        if commit:
            instance.save()
        return instance


class GoodProductItemForm(forms.ModelForm):
    class Meta:
        model = Good
        fields = [
            "category",
            "name_kr",
            "name_uz",
            "name_en",
            "name_ru",
            "expire_date",
            "ingredients",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "ingredients": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "expire_date": forms.DateTimeField(
                input_formats=["%Y-%m-%d"],  # Adjust the format as needed
                widget=forms.DateTimeInput(
                    attrs={"type": "date", "class": "form-control"}
                ),
            ),
        }

    category = forms.ModelChoiceField(
        queryset=SubCategory.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    name_en = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    name_kr = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    name_uz = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    name_ru = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    desc_uz = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )
    desc_ru = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )
    desc_en = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )
    desc_kr = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )
    new_price = forms.DecimalField(
        decimal_places=0,
        max_digits=10,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    # Eski narx maydoni (agar kerak bo'lsa)
    old_price = forms.DecimalField(
        decimal_places=0,
        max_digits=10,
        required=False,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    measure = forms.ChoiceField(
        choices=ProductItem.CHOICES, widget=forms.Select(
            attrs={"class": "form-select"})
    )
    available_quantity = forms.IntegerField(
        min_value=0, widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    # stock = forms.IntegerField(
    #     widget=forms.NumberInput(attrs={"class": "form-control"})
    # )
    # bonus = forms.IntegerField(
    #     widget=forms.NumberInput(attrs={"class": "form-control"})
    # )
    active = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}), initial=True
    )
    images = (
        MultipleFileField()
    )  # New field for multiple images # New field for multiple images
    expire_date = forms.DateTimeField(
        input_formats=["%Y-%m-%d"],  # Adjust the format as needed
        widget=forms.DateTimeInput(
            attrs={"type": "date", "class": "form-control"}),
    )

    def save(self, commit=True):
        good = super().save(commit=False)
        good.name_en = self.cleaned_data.get("name_en")
        good.name_uz = self.cleaned_data.get("name_uz")
        good.name_ru = self.cleaned_data.get("name_ru")
        good.name_kr = self.cleaned_data.get("name_kr")
        good.ingredients_en = self.cleaned_data.get("ingredients_en")
        good.ingredients_uz = self.cleaned_data.get("ingredients_uz")
        good.ingredients_ru = self.cleaned_data.get("ingredients_ru")
        product_item = ProductItem(
            desc_uz=self.cleaned_data["desc_uz"],
            desc_ru=self.cleaned_data["desc_ru"],
            desc_en=self.cleaned_data["desc_en"],
            desc_kr=self.cleaned_data["desc_kr"],
            new_price=self.cleaned_data["new_price"],
            old_price=self.cleaned_data.get("old_price"),
            available_quantity=self.cleaned_data["available_quantity"],
            # stock=self.cleaned_data["stock"],
            # bonus=self.cleaned_data["bonus"],
            active=self.cleaned_data["active"],
        )
        if commit:
            product_item.save()
            good.product = product_item
            good.save()

            # Save multiple images
            for img in self.files.getlist("images"):
                image = Image(
                    image=img,
                    name=f"{self.cleaned_data['name_uz']}_{img.name}",
                    product=product_item,
                )
                image.save()
        return good


class GoodEditForm(forms.ModelForm):
    # Fields for the Good model
    name_uz = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control"}))
    name_ru = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control"}))
    name_en = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control"}))
    name_kr = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control"}))
    expire_date = forms.DateField(
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )
    desc_uz = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )
    desc_ru = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )
    desc_en = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )
    desc_kr = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )
    new_price = forms.DecimalField(
        decimal_places=0,
        max_digits=10,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    images = MultipleFileField(required=False)

    old_price = forms.DecimalField(
        decimal_places=0,
        max_digits=10,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    available_quantity = forms.IntegerField(
        min_value=0, widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    active = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    class Meta:
        model = Good
        fields = [
            "name_uz",
            "name_ru",
            "name_kr",
            "name_en",
            "expire_date",
            "sub_cat",
            "old_price",
            "new_price",
            "images",
            "available_quantity",
            "desc_uz",
            "desc_ru",
            "desc_en",
            "desc_kr",
            "active",
        ]
        widgets = {
            "sub_cat": forms.Select(attrs={"class": "form-select"}),
            "images": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super(GoodEditForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.product:
            product = self.instance.product
            self.fields["old_price"].initial = product.old_price
            self.fields["new_price"].initial = product.new_price
            self.fields["available_quantity"].initial = product.available_quantity
            self.fields["desc_uz"].initial = product.desc_uz
            self.fields["desc_ru"].initial = product.desc_ru
            self.fields["desc_en"].initial = product.desc_kr
            self.fields["desc_kr"].initial = product.desc_en
            self.fields["active"].initial = product.active

    def save(self, commit=True):
        good = super(GoodEditForm, self).save(commit=False)
        if not good.product_id:
            good.product = ProductItem()
        product_item = good.product
        product_item.desc_uz = self.cleaned_data["desc_uz"]
        product_item.desc_ru = self.cleaned_data["desc_ru"]
        product_item.desc_kr = self.cleaned_data["desc_kr"]
        product_item.desc_en = self.cleaned_data["desc_en"]
        product_item.new_price = self.cleaned_data["new_price"]
        product_item.old_price = self.cleaned_data["old_price"]
        product_item.available_quantity = self.cleaned_data["available_quantity"]
        product_item.active = self.cleaned_data["active"]
        if commit:
            product_item.save()
            good.save()
            existing_images = good.product.images.all()

            # Delete existing images if not present in the form data
            form_images = self.files.getlist("images")
            if form_images:
                for existing_image in existing_images:
                    if existing_image.image.name not in form_images:
                        existing_image.delete()

                # Save new images
                for img in form_images:
                    image = Image(
                        image=img,
                        name=f"{self.cleaned_data['name_uz']}_{img.name}",
                        product=product_item,
                    )
                    image.save()
        return good


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = "__all__"
        widgets = {
            "title_uz": forms.TextInput(attrs={"class": "form-control"}),
            "title_ru": forms.TextInput(attrs={"class": "form-control"}),
            "title_en": forms.TextInput(attrs={"class": "form-control"}),
            "title_kr": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "description_uz": forms.Textarea(attrs={"class": "form-control"}),
            "description_ru": forms.Textarea(attrs={"class": "form-control"}),
            "description_en": forms.Textarea(attrs={"class": "form-control"}),
            "description_kr": forms.Textarea(attrs={"class": "form-control"}),
            "active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "title_uz": "Title (Uzbek)",
            "title_ru": "Title (Russian)",
            "title_en": "Title (English)",
            "title_kr": "Title (Korean)",
        }
        required = {
            "title_uz": True,
            "title_ru": True,
            "title_en": True,
            "title_kr": True,
        }

    start_date = forms.DateTimeField(
        input_formats=["%Y-%m-%d"],  # Adjust the format as needed
        widget=forms.DateTimeInput(
            attrs={"type": "date", "class": "form-control"}),
    )
    end_date = forms.DateTimeField(
        input_formats=["%Y-%m-%d"],  # Adjust the format as needed
        widget=forms.DateTimeInput(
            attrs={"type": "date", "class": "form-control"}),
    )

    def save(self, commit=True):
        news = super(NewsForm, self).save(commit=False)

        new_image = self.cleaned_data.get('image', None)
        if new_image:
            news.image = new_image
        if "image" in self.files:
            news.image.delete()  # Delete the old image
            news.image = self.files["image"]  # Assign the new image
        if commit:
            news.save()
        return news


class NewsEditForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        input_formats=["%Y-%m-%d"],  # Adjust the format as needed
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control"}),
        initial=timezone.now(),
    )

    end_date = forms.DateTimeField(
        input_formats=["%Y-%m-%d"],  # Adjust the format as needed
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control"}),
        initial=timezone.now(),
    )
    description_uz = forms.CharField(
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}),
        label="Description (Uzbek)",
        required=True,
    )

    description_ru = forms.CharField(
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}),
        label="Description (Russian)",
        required=True,
    )

    description_en = forms.CharField(
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}),
        label="Description (English)",
        required=True,
    )

    description_kr = forms.CharField(
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}),
        label="Description (Korean)",
        required=True,

    )

    class Meta:
        model = News
        fields = [
            "title_uz",
            "title_ru",
            "title_en",
            "title_kr",
            "image",
            "start_date",
            "end_date",
            "description_uz",
            "description_ru",
            "description_en",
            "description_kr",
            "active",
        ]

        widgets = {
            "title_uz": forms.TextInput(attrs={"class": "form-control"}),
            "title_ru": forms.TextInput(attrs={"class": "form-control"}),
            "title_en": forms.TextInput(attrs={"class": "form-control"}),
            "title_kr": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "description_uz": forms.Textarea(attrs={"class": "form-control"}),
            "description_ru": forms.Textarea(attrs={"class": "form-control"}),
            "description_en": forms.Textarea(attrs={"class": "form-control"}),
            "description_kr": forms.Textarea(attrs={"class": "form-control"}),
            "active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

        labels = {
            "title_uz": "Title (Uzbek)",
            "title_ru": "Title (Russian)",
            "title_en": "Title (English)",
            "title_kr": "Title (Korean)",
            "description_uz": "Description (Uzbek)",
            "description_ru": "Description (Russian)",
            "description_en": "Description (English)",
            "description_kr": "Description (Korean)",
        }

        required = {
            "title_uz": True,
            "title_ru": True,
            "title_en": True,
            "title_kr": True,
            "description_uz": True,
            "description_ru": True,
            "description_en": True,
            "description_kr": True,
        }

    def save(self, commit=False):
        news = super().save(commit=False)
        if not news.start_date:
            news.start_date = self.cleaned_data['start_date']
        if not news.end_date:
            news.end_date = self.cleaned_data['end_date']
        if commit:
            news.save()

        return news


class ServiceEditForm(forms.ModelForm):
    delivery_fee = forms.DecimalField(
        decimal_places=0,
        max_digits=10,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Service
        fields = [
            "delivery_fee",
        ]

    def __init__(self, *args, **kwargs):
        super(ServiceEditForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields["delivery_fee"].initial = self.instance.delivery_fee

    def save(self, commit=True):
        service = super(ServiceEditForm, self).save(commit=False)
        if commit:
            service.save()
        return service


class ReminderForm(forms.ModelForm):
    class Meta:
        model = Information
        fields = [
            "reminder_uz",
            "reminder_ru",
            "reminder_en",
            "reminder_kr",
        ]

    reminder_uz = forms.CharField(
        required=False,
        label="Eslatma UZ",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    reminder_ru = forms.CharField(
        required=False,
        label="Eslatma RU",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    reminder_en = forms.CharField(
        required=False,
        label="Eslatma EN",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    reminder_kr = forms.CharField(
        required=False,
        label="Eslatma KR",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )


class AgrementForm(forms.ModelForm):
    agreement_uz = forms.CharField(
        required=False,
        label="Kelishuv UZ",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    agreement_ru = forms.CharField(
        required=False,
        label="Kelishuv RU",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    agreement_en = forms.CharField(
        required=False,
        label="Kelishuv EN",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    agreement_kr = forms.CharField(
        required=False,
        label="Kelishuv KR",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )

    class Meta:
        model = Information
        fields = [
            "agreement_uz",
            "agreement_ru",
            "agreement_en",
            "agreement_kr",
        ]


class ShipmentForm(forms.ModelForm):
    shipment_terms_uz = forms.CharField(
        required=False,
        label="Yetkazish shartlari UZ",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    shipment_terms_ru = forms.CharField(
        required=False,
        label="Yetkazish shartlari RU",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    shipment_terms_en = forms.CharField(
        required=False,
        label="Yetkazish shartlari EN",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    shipment_terms_kr = forms.CharField(
        required=False,
        label="Yetkazish shartlari KR",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )

    class Meta:
        model = Information
        fields = [
            "shipment_terms_uz",
            "shipment_terms_ru",
            "shipment_terms_en",
            "shipment_terms_kr",
        ]


class PrivacyForm(forms.ModelForm):
    privacy_policy_uz = forms.CharField(
        required=False,
        label="Offerta shartlari UZ",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    privacy_policy_ru = forms.CharField(
        required=False,
        label="Offerta shartlari RU",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    privacy_policy_en = forms.CharField(
        required=False,
        label="Offerta shartlari EN",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    privacy_policy_kr = forms.CharField(
        required=False,
        label="Offerta shartlari KR",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )

    class Meta:
        model = Information
        fields = [
            "privacy_policy_uz",
            "privacy_policy_ru",
            "privacy_policy_en",
            "privacy_policy_kr",
        ]


class AboutUsForm(forms.ModelForm):
    about_us_uz = forms.CharField(
        required=False,
        label="Biz haqimizda UZ",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    about_us_ru = forms.CharField(
        required=False,
        label="Biz haqimizda RU",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    about_us_en = forms.CharField(
        required=False,
        label="Biz haqimizda EN",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    about_us_kr = forms.CharField(
        required=False,
        label="Biz haqimizda KR",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )

    class Meta:
        model = Information
        fields = [
            "about_us_uz",
            "about_us_ru",
            "about_us_en",
            "about_us_kr",
        ]


class SupportForm(forms.ModelForm):
    support_center_uz = forms.CharField(
        required=False,
        label="Qollab quvvatlash markazi UZ",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    support_center_ru = forms.CharField(
        required=False,
        label="Qollab quvvatlash markazi RU",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    support_center_en = forms.CharField(
        required=False,
        label="Qollab quvvatlash markazi EN",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    support_center_kr = forms.CharField(
        required=False,
        label="Qollab quvvatlash markazi KR",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )

    class Meta:
        model = Information
        fields = [
            "support_center_uz",
            "support_center_ru",
            "support_center_en",
            "support_center_kr",
        ]


class PaymentForm(forms.ModelForm):
    payment_data_uz = forms.CharField(
        required=False,
        label="Hisob raqam/Pul o'tkazish shartlari UZ",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    payment_data_ru = forms.CharField(
        required=False,
        label="Hisob raqam/Pul o'tkazish shartlari RU",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    payment_data_en = forms.CharField(
        required=False,
        label="Hisob raqam/Pul o'tkazish shartlari EN",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    payment_data_kr = forms.CharField(
        required=False,
        label="Hisob raqam/Pul o'tkazish shartlari KR",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )

    class Meta:
        model = Information
        fields = [
            "payment_data_uz",
            "payment_data_ru",
            "payment_data_en",
            "payment_data_kr",
        ]


class InformationEditForm(forms.ModelForm):
    reminder_uz = forms.CharField(
        required=False,
        label="Eslatma UZ",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    reminder_ru = forms.CharField(
        required=False,
        label="Eslatma RU",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    reminder_en = forms.CharField(
        required=False,
        label="Eslatma EN",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    reminder_kr = forms.CharField(
        required=False,
        label="Eslatma KR",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    agreement_uz = forms.CharField(
        required=False,
        label="Kelishuv UZ",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    agreement_ru = forms.CharField(
        required=False,
        label="Kelishuv RU",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    agreement_en = forms.CharField(
        required=False,
        label="Kelishuv EN",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    agreement_kr = forms.CharField(
        required=False,
        label="Kelishuv KR",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    shipment_terms_uz = forms.CharField(
        required=False,
        label="Yetkazish shartlari UZ",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    shipment_terms_ru = forms.CharField(
        required=False,
        label="Yetkazish shartlari RU",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    shipment_terms_en = forms.CharField(
        required=False,
        label="Yetkazish shartlari EN",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    shipment_terms_kr = forms.CharField(
        required=False,
        label="Yetkazish shartlari KR",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    privacy_policy_uz = forms.CharField(
        required=False,
        label="Offerta shartlari UZ",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    privacy_policy_ru = forms.CharField(
        required=False,
        label="Offerta shartlari RU",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    privacy_policy_en = forms.CharField(
        required=False,
        label="Offerta shartlari EN",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    privacy_policy_kr = forms.CharField(
        required=False,
        label="Offerta shartlari KR",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    about_us_uz = forms.CharField(
        required=False,
        label="Biz haqimizda UZ",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    about_us_ru = forms.CharField(
        required=False,
        label="Biz haqimizda RU",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    about_us_en = forms.CharField(
        required=False,
        label="Biz haqimizda EN",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    about_us_kr = forms.CharField(
        required=False,
        label="Biz haqimizda KR",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    support_center_uz = forms.CharField(
        required=False,
        label="Qollab quvvatlash markazi UZ",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    support_center_ru = forms.CharField(
        required=False,
        label="Qollab quvvatlash markazi RU",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    support_center_en = forms.CharField(
        required=False,
        label="Qollab quvvatlash markazi EN",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    support_center_kr = forms.CharField(
        required=False,
        label="Qollab quvvatlash markazi KR",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    payment_data_uz = forms.CharField(
        required=False,
        label="Hisob raqam/Pul o'tkazish shartlari UZ",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    payment_data_ru = forms.CharField(
        required=False,
        label="Hisob raqam/Pul o'tkazish shartlari RU",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    payment_data_en = forms.CharField(
        required=False,
        label="Hisob raqam/Pul o'tkazish shartlari EN",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )
    payment_data_kr = forms.CharField(
        required=False,
        label="Hisob raqam/Pul o'tkazish shartlari KR",
        widget=CKEditorWidget(
            attrs={"class": "form-control ckeditor", "rows": 10, "cols": 100}
        ),
    )

    class Meta:
        model = Information
        fields = [
            "reminder_uz",
            "reminder_ru",
            "reminder_en",
            "reminder_kr",
            "agreement_uz",
            "agreement_ru",
            "agreement_en",
            "agreement_kr",
            "shipment_terms_uz",
            "shipment_terms_ru",
            "shipment_terms_en",
            "shipment_terms_kr",
            "privacy_policy_uz",
            "privacy_policy_ru",
            "privacy_policy_en",
            "privacy_policy_kr",
            "about_us_uz",
            "about_us_ru",
            "about_us_en",
            "about_us_kr",
            "support_center_uz",
            "support_center_ru",
            "support_center_en",
            "support_center_kr",
            "payment_data_uz",
            "payment_data_ru",
            "payment_data_en",
            "payment_data_kr",
        ]

    def __init__(self, *args, **kwargs):
        super(InformationEditForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields["reminder_uz"].initial = self.instance.reminder_uz
            self.fields["reminder_ru"].initial = self.instance.reminder_ru
            self.fields["reminder_en"].initial = self.instance.reminder_en
            self.fields["reminder_kr"].initial = self.instance.reminder_kr
            self.fields["agreement_uz"].initial = self.instance.agreement_uz
            self.fields["agreement_ru"].initial = self.instance.agreement_ru
            self.fields["agreement_en"].initial = self.instance.agreement_en
            self.fields["agreement_kr"].initial = self.instance.agreement_kr
            self.fields["shipment_terms_uz"].initial = self.instance.shipment_terms_uz
            self.fields["shipment_terms_ru"].initial = self.instance.shipment_terms_ru
            self.fields["shipment_terms_en"].initial = self.instance.shipment_terms_en
            self.fields["shipment_terms_kr"].initial = self.instance.shipment_terms_kr
            self.fields["privacy_policy_uz"].initial = self.instance.privacy_policy_uz
            self.fields["privacy_policy_ru"].initial = self.instance.privacy_policy_ru
            self.fields["privacy_policy_en"].initial = self.instance.privacy_policy_en
            self.fields["privacy_policy_kr"].initial = self.instance.privacy_policy_kr
            self.fields["about_us_uz"].initial = self.instance.about_us_uz
            self.fields["about_us_ru"].initial = self.instance.about_us_ru
            self.fields["about_us_en"].initial = self.instance.about_us_en
            self.fields["about_us_kr"].initial = self.instance.about_us_kr
            self.fields["support_center_uz"].initial = self.instance.support_center_uz
            self.fields["support_center_ru"].initial = self.instance.support_center_ru
            self.fields["support_center_en"].initial = self.instance.support_center_en
            self.fields["support_center_kr"].initial = self.instance.support_center_kr
            self.fields["payment_data_uz"].initial = self.instance.payment_data_uz
            self.fields["payment_data_ru"].initial = self.instance.payment_data_ru
            self.fields["payment_data_en"].initial = self.instance.payment_data_en
            self.fields["payment_data_kr"].initial = self.instance.payment_data_kr

    def clean(self):
        cleaned_data = super().clean()
        initial_values = {}

        for field_name in self.fields:
            initial_values[field_name] = getattr(self.instance, field_name)

        for field_name, initial_value in initial_values.items():
            new_value = cleaned_data.get(field_name)
            if new_value == initial_value:
                cleaned_data[field_name] = initial_value

        return cleaned_data

    def save(self, commit=True):
        information = super().save(commit=False)
        changed_fields = []

        # Compare cleaned data with initial values
        for field_name, field_value in self.cleaned_data.items():
            if field_value != getattr(information, field_name):
                changed_fields.append(field_name)

        # Set unchanged fields to their initial values
        for field_name in set(self.fields) - set(changed_fields):
            setattr(information, field_name, getattr(
                self.instance, field_name))

        if commit:
            information.save()

        return information


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['title', 'image', 'active']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CategoryEditForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['main_type', "name_uz", "name_ru", "name_en", "name_kr",
                  "image", "active", "desc_uz", "desc_ru", "desc_en", "desc_kr"]
        widgets = {
            'main_type': forms.Select(attrs={'class': 'form-control'}),
            "name_uz": forms.TextInput(attrs={"class": "form-control"}),
            "name_ru": forms.TextInput(attrs={"class": "form-control"}),
            "name_en": forms.TextInput(attrs={"class": "form-control"}),
            "name_kr": forms.TextInput(attrs={"class": "form-control"}),
            "desc_uz": forms.TextInput(attrs={"class": "form-control"}),
            "desc_ru": forms.TextInput(attrs={"class": "form-control"}),
            "desc_en": forms.TextInput(attrs={"class": "form-control"}),
            "desc_kr": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "name_uz": "Name (Uzbek)",
            "name_ru": "Name (Russian)",
            "name_en": "Name (English)",
            "name_kr": "Name (Korean)",
            "desc_uz": "Description (Uzbek)",
            "desc_ru": "Description (Russian)",
            "desc_en": "Description (English)",
            "desc_kr": "Description (Korean)",
        }

    def __init__(self, *args, **kwargs):
        super(CategoryEditForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields["main_type"].initial = self.instance.main_type
            self.fields["name_uz"].initial = self.instance.name_uz
            self.fields["name_ru"].initial = self.instance.name_ru
            self.fields["name_en"].initial = self.instance.name_en
            self.fields["name_kr"].initial = self.instance.name_kr
            self.fields["desc_uz"].initial = self.instance.desc_uz
            self.fields["desc_ru"].initial = self.instance.desc_ru
            self.fields["desc_en"].initial = self.instance.desc_en
            self.fields["desc_kr"].initial = self.instance.name_kr
            self.fields["image"].initial = self.instance.image
            self.fields["active"].initial = self.instance.active


class SubCategoryEditForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ["name_uz", "name_ru", "name_en", "name_kr", "image",
                  "active", "desc_uz", "desc_ru", "desc_en", "desc_kr"]
        widgets = {
            "name_uz": forms.TextInput(attrs={"class": "form-control"}),
            "name_ru": forms.TextInput(attrs={"class": "form-control"}),
            "name_en": forms.TextInput(attrs={"class": "form-control"}),
            "name_kr": forms.TextInput(attrs={"class": "form-control"}),
            "desc_uz": forms.TextInput(attrs={"class": "form-control"}),
            "desc_ru": forms.TextInput(attrs={"class": "form-control"}),
            "desc_en": forms.TextInput(attrs={"class": "form-control"}),
            "desc_kr": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "name_uz": "Name (Uzbek)",
            "name_ru": "Name (Russian)",
            "name_en": "Name (English)",
            "name_kr": "Name (Korean)",
            "desc_uz": "Description (Uzbek)",
            "desc_ru": "Description (Russian)",
            "desc_en": "Description (English)",
            "desc_kr": "Description (Korean)",
        }

    def __init__(self, *args, **kwargs):
        super(SubCategoryEditForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields["name_uz"].initial = self.instance.name_uz
            self.fields["name_ru"].initial = self.instance.name_ru
            self.fields["name_en"].initial = self.instance.name_en
            self.fields["name_kr"].initial = self.instance.name_kr
            self.fields["desc_uz"].initial = self.instance.desc_uz
            self.fields["desc_ru"].initial = self.instance.desc_ru
            self.fields["desc_en"].initial = self.instance.desc_en
            self.fields["desc_kr"].initial = self.instance.desc_kr
            self.fields["image"].initial = self.instance.image
            self.fields["active"].initial = self.instance.active


class CategoryCreateForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = [
            'main_type',
            "name_uz",
            "name_ru",
            "name_en",
            "name_kr",
            "image",
            "active",
        ]
        widgets = {
            'main_type': forms.Select(attrs={'class': 'form-control'}),
            "name_uz": forms.TextInput(attrs={"class": "form-control"}),
            "name_ru": forms.TextInput(attrs={"class": "form-control"}),
            "name_en": forms.TextInput(attrs={"class": "form-control"}),
            "name_kr": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "name_uz": "Name (Uzbek)",
            "name_ru": "Name (Russian)",
            "name_en": "Name (English)",
            "name_kr": "Name (Korean)",
        }
        required = {
            "name_uz": True,
            "name_ru": True,
            "name_en": True,
            "name_kr": True,
        }

    def __init__(self, *args, **kwargs):
        super(CategoryCreateForm, self).__init__(*args, **kwargs)

        # Set required attribute for each field
        self.fields["name_uz"].required = True
        self.fields["name_ru"].required = True
        self.fields["name_en"].required = True
        self.fields["name_kr"].required = True

    def save(self, commit=True):
        instance = super(CategoryCreateForm, self).save(commit=False)

        if commit:
            instance.save()
        return instance


class SubCategoryCreateForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(main_type="f"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = SubCategory
        fields = [
            "name_uz",
            "name_ru",
            "name_en",
            "name_kr",
            "image",
            "category",
            "active",
        ]
        widgets = {
            "name_uz": forms.TextInput(attrs={"class": "form-control"}),
            "name_ru": forms.TextInput(attrs={"class": "form-control"}),
            "name_en": forms.TextInput(attrs={"class": "form-control"}),
            "name_kr": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "name_uz": "Name (Uzbek)",
            "name_ru": "Name (Russian)",
            "name_en": "Name (English)",
            "name_kr": "Name (Korean)",
        }
        required = {
            "name_uz": True,
            "name_ru": True,
            "name_en": True,
            "name_kr": True,
        }

    def __init__(self, *args, **kwargs):
        super(SubCategoryCreateForm, self).__init__(*args, **kwargs)

        # Set required attribute for each field
        self.fields["name_uz"].required = True
        self.fields["name_ru"].required = True
        self.fields["name_en"].required = True
        self.fields["name_kr"].required = True

    def save(self, commit=True):
        instance = super(SubCategoryCreateForm, self).save(commit=False)
        instance.main_type = "f"

        if commit:
            instance.save()
        return instance


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class BonusEditForm(forms.ModelForm):   
    title = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control"}), label='Toifasi')
    amount = forms.DecimalField(
        decimal_places=0,
        max_digits=10,
        required=False,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        label='Buyurtma qiymati'
    )
    percentage = forms.IntegerField(
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        label='Chegirma foizi qiymati'
    )
    active = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False,
        initial=True
    )

    class Meta:
        model = Bonus
        fields = ['title', 'amount', 'percentage', 'active']

    def __init__(self, *args, **kwargs):
        super(BonusEditForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields["title"].initial = self.instance.title
            self.fields["amount"].initial = self.instance.amount
            self.fields["percentage"].initial = self.instance.percentage
            self.fields["active"].initial = self.instance.active

    def save(self, commit=True):
        bonus = super(BonusEditForm, self).save(commit=False)
        if commit:
            bonus.save()
        return bonus


class SocialMediaEditForm(forms.ModelForm):
    telegram = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), label='Telegram', required=False)
    instagram = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), label='Instagram', required=False)
    whatsapp = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), label='Whatsapp', required=False)
    phone_number = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), label='Telefon nomer', required=False)
    imo = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), label='IMO', required=False)
    kakao = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), label='Kakao talk', required=False)
    tiktok = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), label='TikTok', required=False)

    class Meta:
        model = SocialMedia
        fields = ['telegram', 'instagram', 'whatsapp', 'phone_number', 'imo', 'kakao', 'tiktok']

    def clean(self):
        cleaned_data = super().clean()

        for field_name in ['telegram', 'instagram', 'whatsapp', 'tiktok']:
            if cleaned_data.get(field_name) and cleaned_data[field_name] != getattr(self.instance, field_name):
                original_value = getattr(self.instance, field_name)
                cleaned_data[field_name] = self.get_cleaned_url(field_name, cleaned_data[field_name], original_value)

        return cleaned_data

    def get_cleaned_url(self, field_name, value, original_value):
        # Check if the original value already contains any of the prefixes
        if any(original_value.startswith(prefix) for prefix in [f"https://{field_name}.com/", f"https://www.{field_name}.com/", "https://t.me/", "https://wa.me/"]):
            return value  # Don't add the prefix again
        else:
            # Add the prefix based on the social media platform
            if field_name == 'telegram':
                return f"https://t.me/{value}"
            elif field_name == 'instagram':
                return f"https://www.instagram.com/{value}"
            elif field_name == 'whatsapp':
                return f"https://wa.me/{value}"
            elif field_name == 'tiktok':
                return f"https://www.tiktok.com/@{value}"
            else:
                return value

    def __init__(self, *args, **kwargs):
        super(SocialMediaEditForm, self).__init__(*args, **kwargs)
        if self.instance:
            for field_name in ['telegram', 'instagram', 'whatsapp', 'phone_number', 'imo', 'kakao', 'tiktok']:
                self.fields[field_name].initial = getattr(self.instance, field_name)

    def save(self, commit=True):
        media = super(SocialMediaEditForm, self).save(commit=commit)
        return media
