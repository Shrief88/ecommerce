from django import forms 


PAYMENT_CHOICES = (
  ('S', 'Stripe'),
  ('C', 'Cash on delivery'),
)

class CheckoutForm(forms.Form):
  first_name = forms.CharField(widget=forms.TextInput(attrs={
    'class' : 'form-control',
    'id' : 'firstName' ,
    
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

  

  payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CoupounForm(forms.Form):
  code = forms.CharField(widget=forms.TextInput(attrs={
    'class' : 'form-control',
    'placeholder' : 'promo code',
    'aria-label' : "'Recipient's username'",
    'aria-describedby' : "basic-addon2",
  }))


class RefundForm(forms.Form):
  ref_code = forms.CharField()
  reason = forms.CharField(widget=forms.Textarea(attrs={
    'rows' : 4
  }))


class AddingForm(forms.Form):
  quantity = forms.IntegerField(min_value=1,widget=forms.NumberInput(attrs={
    'value' : 1,
    'aria-label': 'Search',
    'class' : 'form-control',
    'style' : "width: 60px",
  }))