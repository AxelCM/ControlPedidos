#Django
from django import forms

from user.models import User

class SignUpForm(forms.Form):
    """Sign up form"""

    # username = forms.CharField(min_length=4, max_length=50)
    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput()
    )
    """password confirmation field"""
    password_confirmation = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput()
    )

    first_name = forms.CharField(min_length=2, max_length=50)
    last_name = forms.CharField(min_length=2, max_length=50)

    email = forms.CharField(
        min_length=6,
        max_length=70,
        widget=forms.EmailInput()
    )
    phone_number = forms.CharField(min_length=8, max_length=9)

    def clean_username(self):
        """Username must be unique."""
        username = self.cleaned_data['email']
        username_taken = User.objects.filter(username=username).exists()
        if username_taken:
            raise forms.ValidationError('Este correo ya se encuentra en uso')
        return username


    def clean_phone_number(self):
        """Username must be unique."""
        phone_number = self.cleaned_data['phone_number']
        phone_taken = User.objects.filter(phone_number=phone_number).exists()
        if phone_taken:
            raise forms.ValidationError('Hubo un error al agregar este numero de telefono')
        return phone_number

    def clean(self):
        """Verify password confirmation match."""
        data = super().clean()

        password = data['password']
        password_confirmation = data['password_confirmation']
        if password != password_confirmation:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return data

    def save(self):
        """Create user"""
        data = self.cleaned_data
        data.pop('password_confirmation')
        data['username'] = data['email']
        user = User.objects.create_user(**data)

# class SignUpForm(forms.ModelForm):
#
#     class Meta:
#         model = User
#         fields = '__all__'
#
#     def clean_date_joined(self):
#         """Add Date now"""
#         date_joined = self.cleaned_data['date_joined']
#         now = datetime.now()
#         date_joined = now
#         return date_joined

class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name' , 'last_name' , 'email' , 'groups')
