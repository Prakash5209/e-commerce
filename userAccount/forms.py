
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from allauth.account.forms import BaseSignupForm
from allauth.account.adapter import get_adapter
from allauth.account.utils import user_username, user_email
from allauth.account import app_settings
from allauth.account.forms import PasswordField
from allauth.utils import set_form_field_order
from django.contrib.auth import password_validation  # Make sure this import is there

class SignupForm(BaseSignupForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields["password1"] = PasswordField(
            label=_("Password"),
            autocomplete="new-password",
            help_text=None,  # Modified help_text to None
        )
        if app_settings.SIGNUP_PASSWORD_ENTER_TWICE:
            self.fields["password2"] = PasswordField(
                label=_("Password (again)"), autocomplete="new-password"
            )

        if hasattr(self, "field_order"):
            set_form_field_order(self, self.field_order)

        honeypot_field_name = app_settings.SIGNUP_FORM_HONEYPOT_FIELD
        if honeypot_field_name:
            self.fields[honeypot_field_name] = forms.CharField(
                required=False,
                label="",
                widget=forms.TextInput(
                    attrs={
                        "style": "position: absolute; right: -99999px;",
                        "tabindex": "-1",
                        "autocomplete": "nope",
                    }
                ),
            )

    def try_save(self, request):
        """
        override of parent class method that adds additional catching
        of a potential bot filling out the honeypot field and returns a
        'fake' email verification response if honeypot was filled out
        """
        honeypot_field_name = app_settings.SIGNUP_FORM_HONEYPOT_FIELD
        if honeypot_field_name:
            if self.cleaned_data[honeypot_field_name]:
                user = None
                adapter = get_adapter()
                # honeypot fields work best when you do not report to the bot
                # that anything went wrong. So we return a fake email verification
                # sent response but without creating a user
                resp = adapter.respond_email_verification_sent(request, None)
                return user, resp

        return super().try_save(request)

    def clean(self):
        super().clean()

        # `password` cannot be of type `SetPasswordField`, as we don't
        # have a `User` yet. So, let's populate a dummy user to be used
        # for password validation.
        User = get_user_model()
        dummy_user = User()
        user_username(dummy_user, self.cleaned_data.get("username"))
        user_email(dummy_user, self.cleaned_data.get("email"))
        password = self.cleaned_data.get("password1")
        if password:
            try:
                get_adapter().clean_password(password, user=dummy_user)
            except forms.ValidationError as e:
                self.add_error("password1", e)

        if (
            app_settings.SIGNUP_PASSWORD_ENTER_TWICE
            and "password1" in self.cleaned_data
            and "password2" in self.cleaned_data
        ):
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                self.add_error(
                    "password2",
                    _("You must type the same password each time."),
                )
        return self.cleaned_data

