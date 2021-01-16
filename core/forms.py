from django import forms 


PAYMENT_CHOICES = (
  ('S', 'Stripe'),
  ('P', 'PayPal'),
)

class CheckoutForm(forms.Form):
  first_name = forms.CharField(widget=forms.TextInput(attrs={
    'class' : 'form-control',
    'id' : 'firstName' 
  }))
  
  last_name = forms.CharField(widget=forms.TextInput(attrs={
    'class' : 'form-control',
    'id' : 'lastName' 
  }))

  phone = forms.CharField(widget=forms.TextInput(attrs={
    'class' : 'form-control',
    'id' : 'phone' 
  }))

  secPhone = forms.CharField(required=False ,widget=forms.TextInput(attrs={
    'class' : 'form-control',
    'id' : 'phone-2' 
  }))

  city = forms.CharField(widget=forms.TextInput(attrs={
    'class' : 'form-control',
    'id' : 'city' 
  }))

  address = forms.CharField(widget=forms.TextInput(attrs={
    'class' : 'form-control',
    'id' : 'address' ,
    'placeholder' : '9 مصطفى النحاس , مدينة نصر'
  }))

  secAddress = forms.CharField(required=False ,widget=forms.TextInput(attrs={
    'class' : 'form-control',
    'id' : 'address-2' 
  })) 

  same_shipping_address = forms.BooleanField(required=False ,widget=forms.CheckboxInput(attrs={
    'class' : 'custom-control-input',
    'id'  : 'same-address'
  }))

  same_info = forms.BooleanField(required=False ,widget=forms.CheckboxInput(attrs={
    'class' : 'custom-control-input',
    'id'  : 'save-info'
  }))

  payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)