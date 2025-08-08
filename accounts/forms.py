from .models import CustomUser
from django import forms
class SignupForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "phone", "gender", "date_Birth","image")
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number"}),
            "gender": forms.Select(attrs={"class": "form-select"}),
            "date_Birth": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control",
                "placeholder": "Date of Birth"
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control border border-2 shadow-sm",
                "style": "padding: 10px;"
            }),
        }
        labels = {
            "email": "Email",
            "first_name": "First Name",
            "last_name": "Last Name",
            "phone": "Phone Number",
            "gender": "Gender",
            "date_Birth": "Date of Birth",
            "image": "Profile Image"
        }

    def clean_password2(self):
        if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
            raise forms.ValidationError("Not mached")
        return self.cleaned_data["password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.username = f"{user.first_name} {user.last_name}" 
        if not self.cleaned_data.get("image"):
            user.image = "account/default_user.jpg"
        if commit:
            user.save()
        return user
    

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "phone","image"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control border border-2 shadow-sm",
                "style": "padding: 10px;",
            })
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = f"{user.first_name} {user.last_name}"
        if self.cleaned_data.get("image") is False:
            user.image = "account/default_user.jpg" 
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)