from django import forms
from django.forms import ClearableFileInput
from ..models import Phone, ProductItem, SubCategory, Image

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].update({
            'class': 'form-control',
            'multiple': True,
        })
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
        fields = ['brand_name', 'model_name', 'ram', 'storage']
        widgets = {
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_name': forms.TextInput(attrs={'class': 'form-control'}),
            'ram': forms.Select(attrs={'class': 'form-control'}),
            'storage': forms.Select(attrs={'class': 'form-control'}),
            # Add more fields here
        }

    # Fields for ProductItem
    category = forms.ModelChoiceField(queryset=SubCategory.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    desc = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    price = forms.DecimalField(decimal_places=1, max_digits=10, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    measure = forms.ChoiceField(choices=ProductItem.CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    available_quantity = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    stock = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    bonus = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    active = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    images = MultipleFileField() # New field for multiple images # New field for multiple images

    def save(self, commit=True):
        phone = super().save(commit=False)
        product_item = ProductItem(
            category=self.cleaned_data['category'],
            name=self.cleaned_data['name'],
            desc=self.cleaned_data['desc'],
            price=self.cleaned_data['price'],
            measure=self.cleaned_data['measure'],
            available_quantity=self.cleaned_data['available_quantity'],
            stock=self.cleaned_data['stock'],
            bonus=self.cleaned_data['bonus'],
            active=self.cleaned_data['active']
        )
        if commit:
            product_item.save()
            phone.product = product_item
            phone.save()

            # Save multiple images
            for img in self.files.getlist('images'):
                image = Image(
                    image=img,
                    name=f"{self.cleaned_data['name']}_{img.name}",
                    product=product_item
                )
                image.save()
        return phone
