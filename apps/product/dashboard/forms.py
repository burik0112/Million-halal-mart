from django import forms
from django.forms import ClearableFileInput
from ..models import Phone, ProductItem, SubCategory, Image, Ticket, Good, Category

from apps.customer.models import News


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
        fields = ["model_name", "ram", "storage", "category", "color", "condition"]
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
    desc = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )
    price = forms.DecimalField(
        decimal_places=1,
        max_digits=10,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    available_quantity = forms.IntegerField(
        min_value=0, widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    stock = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        required=False,
        initial=0,
    )
    bonus = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        required=False,
        initial=0,
    )
    active = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}), initial=True
    )
    images = (
        MultipleFileField()
    )  # New field for multiple images # New field for multiple images

    def save(self, commit=True):
        phone = super().save(commit=False)
        product_item = ProductItem(
            desc=self.cleaned_data["desc"],
            price=self.cleaned_data["price"],
            available_quantity=self.cleaned_data["available_quantity"],
            stock=self.cleaned_data["stock"],
            bonus=self.cleaned_data["bonus"],
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
        fields = ["name", "image", "desc", "stock", "bonus", "active"]
        widgets = {
            # 'main_type': forms.Select(attrs={'class': 'form-control'}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "desc": forms.Textarea(attrs={"class": "form-control"}),
            "stock": forms.NumberInput(attrs={"class": "form-control"}),
            "bonus": forms.NumberInput(attrs={"class": "form-control"}),
            "active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class TicketCategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "image", "desc", "stock", "bonus", "active"]
        widgets = {
            # 'main_type': forms.Select(attrs={'class': 'form-control'}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "desc": forms.Textarea(attrs={"class": "form-control"}),
            "stock": forms.NumberInput(attrs={"class": "form-control"}),
            "bonus": forms.NumberInput(attrs={"class": "form-control"}),
            "active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class TicketProductItemForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["event_name"]
        widgets = {
            "category": forms.Select(attrs={"class": "form-control"}),
            "event_name": forms.TextInput(attrs={"class": "form-control"}),
        }

    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(main_type="t"),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    event_date = forms.DateTimeField(
        input_formats=["%Y-%m-%d"],  # Adjust the format as needed
        widget=forms.DateTimeInput(attrs={"type": "date", "class": "form-control"}),
    )
    desc = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )
    price = forms.DecimalField(
        decimal_places=1,
        max_digits=10,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    available_quantity = forms.IntegerField(
        min_value=0, widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    stock = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"}), initial=0
    )
    bonus = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"}), initial=0
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
            desc=self.cleaned_data["desc"],
            price=self.cleaned_data["price"],
            available_quantity=self.cleaned_data["available_quantity"],
            stock=self.cleaned_data["stock"],
            bonus=self.cleaned_data["bonus"],
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
                    name=f"{self.cleaned_data['event_name']}_{img.name}",
                    product=product_item,
                )
                image.save()
        return ticket


class GoodCategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "image", "desc", "stock", "bonus", "active"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "desc": forms.Textarea(attrs={"class": "form-control"}),
            "stock": forms.NumberInput(attrs={"class": "form-control"}),
            "bonus": forms.NumberInput(attrs={"class": "form-control"}),
            "active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class GoodProductItemForm(forms.ModelForm):
    class Meta:
        model = Good
        fields = [
            "category",
            "name",
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
    ingredients_en = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    ingredients_uz = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    ingredients_ru = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    desc = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )
    price = forms.DecimalField(
        decimal_places=1,
        max_digits=10,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    measure = forms.ChoiceField(
        choices=ProductItem.CHOICES, widget=forms.Select(attrs={"class": "form-select"})
    )
    available_quantity = forms.IntegerField(
        min_value=0, widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    stock = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    bonus = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    active = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )
    images = (
        MultipleFileField()
    )  # New field for multiple images # New field for multiple images
    expire_date = forms.DateTimeField(
        input_formats=["%Y-%m-%d"],  # Adjust the format as needed
        widget=forms.DateTimeInput(attrs={"type": "date", "class": "form-control"}),
    )

    def save(self, commit=True):
        good = super().save(commit=False)
        good.name_en = self.cleaned_data.get("name_en")
        good.name_uz = self.cleaned_data.get("name_uz")
        good.name_ru = self.cleaned_data.get("name_ru")
        good.ingredients_en = self.cleaned_data.get("ingredients_en")
        good.ingredients_uz = self.cleaned_data.get("ingredients_uz")
        good.ingredients_ru = self.cleaned_data.get("ingredients_ru")
        product_item = ProductItem(
            desc=self.cleaned_data["desc"],
            price=self.cleaned_data["price"],
            available_quantity=self.cleaned_data["available_quantity"],
            stock=self.cleaned_data["stock"],
            bonus=self.cleaned_data["bonus"],
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
                    name=f"{self.cleaned_data['name']}_{img.name}",
                    product=product_item,
                )
                image.save()
        return good


class PhoneEditForm(forms.ModelForm):
    product_desc = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )
    product_price = forms.DecimalField(
        decimal_places=1,
        max_digits=10,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    product_measure = forms.ChoiceField(
        choices=ProductItem.CHOICES, widget=forms.Select(attrs={"class": "form-select"})
    )
    product_available_quantity = forms.IntegerField(
        min_value=0, widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    product_stock = forms.IntegerField(
        min_value=0, widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    product_bonus = forms.IntegerField(
        min_value=0, widget=forms.NumberInput(attrs={"class": "form-control"})
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
            "product_desc",
            "product_price",
            "product_measure",
            "product_available_quantity",
            "product_stock",
            "product_bonus",
            "product_active",
        ]
        widgets = {
            "model_name": forms.TextInput(attrs={"class": "form-control"}),
            "color": forms.Select(attrs={"class": "form-select"}),
            "condition": forms.Select(attrs={"class": "form-select"}),
            "ram": forms.Select(attrs={"class": "form-select"}),
            "storage": forms.Select(attrs={"class": "form-select"}),
            "category": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super(PhoneEditForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.product:
            product = self.instance.product
            self.fields["product_desc"].initial = product.desc
            self.fields["product_price"].initial = product.price
            self.fields["product_measure"].initial = product.measure
            self.fields[
                "product_available_quantity"
            ].initial = product.available_quantity
            self.fields["product_stock"].initial = product.stock
            self.fields["product_bonus"].initial = product.bonus
            self.fields["product_active"].initial = product.active

    def save(self, commit=True):
        phone = super(PhoneEditForm, self).save(commit=False)
        if not phone.product_id:
            phone.product = ProductItem()
        product_item = phone.product
        product_item.desc = self.cleaned_data["product_desc"]
        product_item.price = self.cleaned_data["product_price"]
        product_item.measure = self.cleaned_data["product_measure"]
        product_item.available_quantity = self.cleaned_data[
            "product_available_quantity"
        ]
        product_item.stock = self.cleaned_data["product_stock"]
        product_item.bonus = self.cleaned_data["product_bonus"]
        product_item.active = self.cleaned_data["product_active"]
        if commit:
            product_item.save()
            phone.save()
        return phone


class TicketEditForm(forms.ModelForm):
    product_desc = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )
    product_price = forms.DecimalField(
        decimal_places=1,
        max_digits=10,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    product_available_quantity = forms.IntegerField(
        min_value=0, widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    product_stock = forms.IntegerField(
        min_value=0, widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    product_bonus = forms.IntegerField(
        min_value=0, widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    product_active = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    class Meta:
        model = Ticket
        exclude = ["event_date"]
        fields = [
            "event_name",
            "event_date",
            "category",
            "product_desc",
            "product_price",
            "product_available_quantity",
            "product_stock",
            "product_bonus",
            "product_active",
        ]
        widgets = {
            "event_name": forms.TextInput(attrs={"class": "form-control"}),
            "event_date": forms.Select(attrs={"class": "form-select"}),
            "category": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super(TicketEditForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.product:
            product = self.instance.product
            self.fields["product_desc"].initial = product.desc
            self.fields["product_price"].initial = product.price
            self.fields[
                "product_available_quantity"
            ].initial = product.available_quantity
            self.fields["product_stock"].initial = product.stock
            self.fields["product_bonus"].initial = product.bonus
            self.fields["product_active"].initial = product.active

    def save(self, commit=True):
        ticket = super(TicketEditForm, self).save(commit=False)
        if not ticket.product_id:
            ticket.product = ProductItem()
        product_item = ticket.product
        product_item.desc = self.cleaned_data["product_desc"]
        product_item.price = self.cleaned_data["product_price"]
        product_item.available_quantity = self.cleaned_data[
            "product_available_quantity"
        ]
        product_item.stock = self.cleaned_data["product_stock"]
        product_item.bonus = self.cleaned_data["product_bonus"]
        product_item.active = self.cleaned_data["product_active"]
        if commit:
            product_item.save()
            ticket.save()
        return ticket


class GoodEditForm(forms.ModelForm):
    # Fields for the Good model
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    ingredients = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )
    expire_date = forms.DateField(
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )

    # Fields for the related ProductItem
    product_desc = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )
    product_price = forms.DecimalField(
        decimal_places=2,
        max_digits=10,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    product_available_quantity = forms.IntegerField(
        min_value=0, widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    product_stock = forms.IntegerField(
        min_value=0, widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    product_bonus = forms.IntegerField(
        min_value=0, widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    product_active = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    class Meta:
        model = Good
        fields = [
            "name",
            "ingredients",
            "expire_date",
            "sub_cat",
            "product_desc",
            "product_price",
            "product_available_quantity",
            "product_stock",
            "product_bonus",
            "product_active",
        ]
        widgets = {
            "sub_cat": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super(GoodEditForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.product:
            product = self.instance.product
            self.fields["product_desc"].initial = product.desc
            self.fields["product_price"].initial = product.price
            self.fields[
                "product_available_quantity"
            ].initial = product.available_quantity
            self.fields["product_stock"].initial = product.stock
            self.fields["product_bonus"].initial = product.bonus
            self.fields["product_active"].initial = product.active

    def save(self, commit=True):
        good = super(GoodEditForm, self).save(commit=False)
        if not good.product_id:
            good.product = ProductItem()
        product_item = good.product
        product_item.desc = self.cleaned_data["product_desc"]
        product_item.price = self.cleaned_data["product_price"]
        product_item.available_quantity = self.cleaned_data[
            "product_available_quantity"
        ]
        product_item.stock = self.cleaned_data["product_stock"]
        product_item.bonus = self.cleaned_data["product_bonus"]
        product_item.active = self.cleaned_data["product_active"]
        if commit:
            product_item.save()
            good.save()
        return good


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ["title", "description", "image", "active"]

    widgets = {
        "start_date": forms.TextInput(attrs={"type": "datetime-local"}),
        "end_date": forms.TextInput(attrs={"type": "datetime-local"}),
    }
