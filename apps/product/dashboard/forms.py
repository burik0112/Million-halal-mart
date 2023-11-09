from django import forms
from django.forms import ClearableFileInput
from ..models import Phone, ProductItem, SubCategory, Image, Ticket, Good, Category


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
        fields = ['model_name', 'ram', 'storage',
                  'category', 'color', 'condition']
        widgets = {
            'model_name': forms.TextInput(attrs={'class': 'form-control'}),
            'ram': forms.Select(attrs={'class': 'form-control'}),
            'storage': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'color': forms.Select(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
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
        widget=forms.NumberInput(attrs={"class": "form-control"}), required=False, initial=0
    )
    bonus = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"}), required=False, initial=0
    )
    active = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        initial=True
    )
    images = (
        MultipleFileField()
    )  # New field for multiple images # New field for multiple images

    def save(self, commit=True):
        phone = super().save(commit=False)
        product_item = ProductItem(
            desc=self.cleaned_data['desc'],
            price=self.cleaned_data['price'],
            available_quantity=self.cleaned_data['available_quantity'],
            stock=self.cleaned_data['stock'],
            bonus=self.cleaned_data['bonus'],
            active=self.cleaned_data['active']
        )
        if commit:
            product_item.save()
            phone.product = product_item
            # Category field added
            phone.category = self.cleaned_data['category']
            phone.save()

            # Save multiple images
            for img in self.files.getlist("images"):
                image = Image(
                    image=img,
                    name=f"{self.cleaned_data['model_name']}_{img.name}",
                    product=product_item
                )
                image.save()
        return phone


class PhoneCategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image', 'desc', 'stock', 'bonus', 'active']
        widgets = {
            # 'main_type': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'bonus': forms.NumberInput(attrs={'class': 'form-control'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TicketCategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image', 'desc', 'stock', 'bonus', 'active']
        widgets = {
            # 'main_type': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'bonus': forms.NumberInput(attrs={'class': 'form-control'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TicketProductItemForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["event_name"]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            # Add more fields here
        }
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(main_type="t"),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    event_name = forms.CharField(
        max_length=255, widget=forms.TextInput(attrs={"class": "form-control"})
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
    event_date = forms.DateTimeField()

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
            ticket.category = self.cleaned_data['category']
            ticket.save()

            # Save multiple images
            for img in self.files.getlist("images"):
                image = Image(
                    image=img,
                    name=f"{self.cleaned_data['name']}_{img.name}",
                    product=product_item,
                )
                image.save()
        return ticket


class GoodProductItemForm(forms.ModelForm):
    class Meta:
        model = Good
        fields = ["name", "ingredients", "expire_date"]

    category = forms.ModelChoiceField(
        queryset=SubCategory.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    name = forms.CharField(
        max_length=255, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    ingredients = forms.CharField(
        max_length=255, widget=forms.TextInput(attrs={"class": "form-control"})
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
    expire_date = forms.DateTimeField()

    def save(self, commit=True):
        good = super().save(commit=False)
        product_item = ProductItem(
            category=self.cleaned_data["category"],
            name=self.cleaned_data["name"],
            ingredients=self.cleaned_data["ingredients"],
            desc=self.cleaned_data["desc"],
            price=self.cleaned_data["price"],
            available_quantity=self.cleaned_data["available_quantity"],
            stock=self.cleaned_data["stock"],
            bonus=self.cleaned_data["bonus"],
            active=self.cleaned_data["active"],
            expire_date=self.cleaned_data["expire_date"],
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
