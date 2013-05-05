from userena.forms import EditProfileForm
from django import forms


class EditProfileFormExtra(EditProfileForm):
    balance = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))

    def clean_balance(self):
        return self.instance.balance