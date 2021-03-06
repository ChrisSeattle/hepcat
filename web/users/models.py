from django.contrib.auth.models import AbstractUser, UserManager, Group
from django.db import models
from django.db.utils import IntegrityError
from django.utils.functional import cached_property
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

# TODO: Move some of the student vs staff logic to Group
teacher_group, created_teacher = Group.objects.get_or_create(name='teacher')
admin_group, created_admin = Group.objects.get_or_create(name='admin')
staff_group, created_staff = Group.objects.get_or_create(name='staff')
groups_from_role = {'is_teacher': teacher_group, 'is_admin': admin_group, 'is_staff': staff_group}


class UserManagerHC(UserManager):
    """Adding & Modifying some features to the default UserManager.
        Inherits from: UserManager, BaseUserManager, models.Manager, ...
    """

    @staticmethod
    def normalize_email(email):
        """While uppercase characters are technically allowed for the username
            portion of an email address, we are deciding to not allow uppercase
            characters with the understanding that many email systems do not
            respect uppercase as different from lowercase.
            Instead of calling .lower(), which is the default technique used
            by the UserManager, we are using .casefold(), which is better when
            dealing with some international character sets.
        """
        if not email:
            return ''
        if not isinstance(email, str):
            raise TypeError(_("The email should be a string. "))
        # email = super().normalize_email(email)
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError as e:
            raise e
        else:
            email = email_name.casefold() + '@' + domain_part.casefold()
        return email

    def set_user(self, username=None, email=None, password=None, **extra_fields):
        """Called for all user creation methods (create_user, create_superuser, etc).
            Email addresses and login usernames are normalized, allowing no uppercase characters.
            A user must have a unique login username (usually their email address).
            Unless the 'username_not_email' was explicitly set to True, we will use the email as username.
            If a user with that email already exists (or 'username_not_email' is True), and no username was provided,
            then it will create one based on their 'first_name' and 'last_name'.
            Raises Error if a unique username cannot be formed, or otherwise cannot create the user.
            Returns a user instance created with the inherited self._create_user method if successful.
        """
        # print('===== UserManagerHC.set_user was called ========')
        user, message = None, ''
        if not email:
            message += "An email address is preferred to ensure confirmation, "
            message += "but we can create an account without one. "
            if not extra_fields.setdefault('username_not_email', True):
                message += "You requested to use email as your login username, but did not provide an email address. "
                raise ValidationError(_(message))
        else:
            email = self.normalize_email(email)

        if not extra_fields.setdefault('username_not_email', False):
            try:
                user = self._create_user(email, email, password, **extra_fields)
            except IntegrityError:
                message += "A unique email address is preferred, but a user already exists with that email address. "
                extra_fields['username_not_email'] = True
        if extra_fields.get('username_not_email') is True:
            name_fields = ('first_name', 'last_name')
            username = username or '_'.join(extra_fields[key].strip() for key in name_fields if key in extra_fields)
            if not username:
                message += "If you are not using your email as your username/login, "
                message += "then you must either set a username or provide a first and/or last name. "
                raise ValidationError(_(message))
            username = username.casefold()
            try:
                user = self._create_user(username, email, password, **extra_fields)
            except IntegrityError:
                message += "A user already exists with that username, or matching first and last name. "
                message += "Please provide some form of unique user information (email address, username, or name). "
                raise ValidationError(_(message))
        return user

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        """Create a non-superuser account. Defaults to student, but can be any combination of admin, teacher, student.
            Required inputs: must have either email (preferred), username, or have first_name and/or last_name.
            If given an email, the other username techniques are ignored unless 'username_not_email' is set to True.
            If not using email, will try with username (if given), or create username from 'first_name' and 'last_name'.
        """
        # print('================== UserManagerHC.create_user ========================')
        extra_fields['is_superuser'] = False  # This method will never allow creating a superuser.
        if extra_fields.get('is_teacher') is True or extra_fields.get('is_admin') is True:
            extra_fields.setdefault('is_staff', True)
            extra_fields.setdefault('is_student', False)
        else:
            extra_fields.setdefault('is_staff', False)
            extra_fields.setdefault('is_student', True)
        return self.set_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        """Create a superuser account, which will be staff, but could also be a teacher, admin and/or a student.
            If the username is None, or other falsy values, then username will be email (default) or created from name.
        """
        # print('================== UserManagerHC.create_superuser ========================')
        if not extra_fields.setdefault('is_staff', True):
            raise ValidationError(_('Superuser must have is_staff=True.'))
        if not extra_fields.setdefault('is_superuser', True):
            raise ValidationError(_('Superuser must have is_superuser=True.'))
        if not extra_fields.setdefault('is_admin', True):
            raise ValidationError(_('Superuser must have is_admin=True.'))
        if not any([username, 'first_name' in extra_fields, 'last_name' in extra_fields]):
            username = email
        return self.set_user(username, email, password, **extra_fields)

    def find_or_create_for_anon(self, email=None, **kwargs):
        """This is called when someone registers when they are not logged in. If they are a new customer, we want
            no friction, just create a user account. If they might be an existing user, we need to get them logged in.
        """
        email = self.normalize_email(email) if email else None
        first_name, last_name = kwargs.get('first_name'), kwargs.get('last_name')
        q = UserHC.objects
        found_email = q.filter(email=email).count() if email else 0
        q = q.filter(last_name__iexact=last_name) if last_name else q
        q = q.filter(first_name__iexact=first_name) if first_name else q
        found_name = q.count() if first_name or last_name else 0
        if found_email or found_name:
            # TODO: redirect to login, auto-filling appropriate fields. This should also work if they have no account.
            print('---- Maybe they have had classes before? -----')
            found = q.filter(email=email).first()
            return (found, 'existing')  # TODO: ?Update this to cause a redirect?
        else:
            print('----- Creating a new user! -----')
            return self.create_user(self, email=email, **kwargs)  # create a new user with this data
        # end find_or_create_for_anon

    def find_or_create_by_name(self, first_name=None, last_name=None, possible_users=None, **kwargs):
        """This is called when a user signs up someone else """
        # print("======== UserHC.objects.find_or_create_by_name =====")

        def _get_single(q, **kwargs):
            """Helper to get if there is only one. """
            try:
                obj = q.get(**kwargs)
            except UserHC.MultipleObjectsReturned:
                obj = None
            except UserHC.DoesNotExist:
                obj = None
            return obj

        friend = None
        if possible_users:
            if not isinstance(possible_users, models.QuerySet):
                raise TypeError(_('Possible_users must be a QuerySet of Users'))

            friend = _get_single(possible_users, first_name__iexact=first_name, last_name__iexact=last_name) \
                or _get_single(possible_users, first_name__icontains=first_name, last_name__icontains=last_name) \
                or _get_single(possible_users, last_name__icontains=last_name) \
                or _get_single(possible_users, first_name__icontains=first_name) \
                or None
        if not friend:
            friend = _get_single(UserHC.objects, first_name__iexact=first_name, last_name__iexact=last_name) \
                or _get_single(UserHC.objects, first_name__icontains=first_name, last_name__icontains=last_name) \
                or None
        # TODO: Should there be some kind of confirmation page if friend found?
        return friend if friend else self.create_user(self, **kwargs)  # original call should have email in kwargs.


class UserHC(AbstractUser):
    """This will be the custom Users model for the site.
        Inherits from: AbstractUser, AbstractBaseUser, models.Model, ModelBase, ...
    """
    USERNAME_CHOICES = (
        (False, _("Use email address as login. ")),
        (True, _("Create a username. "))
    )

    # first_name, last_name, id, email, and username (often not used directly) - all exist from inherited models.
    is_student = models.BooleanField(_('student'), default=True, )
    is_teacher = models.BooleanField(_('teacher'), default=False, )
    is_admin = models.BooleanField(_('admin'), default=False, )
    # is_superuser, is_staff, is_active exist from inherited models.
    username_not_email = models.BooleanField(_('login type'), choices=USERNAME_CHOICES, default=False,
                                             help_text=_('Typically left empty to use email as your login. '), )
    billing_address_1 = models.CharField(_('street address (line 1)'), max_length=95, blank=True, )
    billing_address_2 = models.CharField(_('street address (continued)'), max_length=95, blank=True, )
    billing_city = models.CharField(_('city'), max_length=95, default=settings.DEFAULT_CITY, blank=True, )
    billing_country_area = models.CharField(_('state'), max_length=2, default=settings.DEFAULT_COUNTRY_AREA_STATE,
                                            # help_text=_('Territory, or Province'),
                                            blank=True, )
    billing_postcode = models.CharField(_('zipcode'), max_length=10, blank=True,
                                        # help_text=_('Postal Code'),
                                        )
    # billing_country_code = models.CharField(_('country'), default=settings.DEFAULT_COUNTRY, max_length=2, blank=True,)
    billing_country_code = CountryField(_('country'), default=settings.DEFAULT_COUNTRY, max_length=2, blank=True,)
    # # # user.student or user.staff holds the linked profile for this user.
    objects = UserManagerHC()

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        username = self.USERNAME_FIELD
        email = self.get_email_field_name()
        # TODO: Determine which of these actually works as expected.
        self._meta.get_field(email).max_length = 191
        self._meta.get_field(email).help_text = _("Used for confirmation and typically for login. ")
        self._meta.get_field(username).help_text = _("Only needed if user does not have a unique email. ")
        self._meta.get_field(username).verbose_name = _("Email or Login")

    @property
    def full_name(self):
        return self.get_full_name() or _("Name Not Found")

    @cached_property
    def display_name(self):
        name = self.get_full_name()
        if not name:
            name = self.get_username()
        return name

    @property
    def user_roles(self):
        user_val, typelist = 0, []
        for i, ea in enumerate((self.is_student, self.is_teacher, self.is_admin, self.is_superuser)):
            if ea:
                user_val += 2 ** i
                typelist.append(getattr(ea, 'verbose_name', getattr(ea, 'name', 'unknown')))
        return (user_val, typelist)

    def make_username(self):
        """Instead of user selecting a username, we will generate it from their info, using casefold()
            instead of lower() since it is better for some international character sets.
        """
        # TODO: Confirm our final username is not in use.
        if self.username_not_email is False:
            return self.email.casefold()
        name_gen = (getattr(self, key).strip() for key in ('first_name', 'last_name') if getattr(self, key, None))
        username = '_'.join(name_gen).casefold()
        return self.normalize_username(username)

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.make_username()
        self.is_staff = True if any([self.is_teacher, self.is_admin, self.is_superuser]) else False
        # TODO: Deal with username (email) being checked as existing even when we want a new user
        super().save(*args, **kwargs)
        for role, group in groups_from_role.items():
            if getattr(self, role, None):
                self.groups.add(group)
            else:
                self.groups.remove(group)

    def __str__(self):
        return self.display_name

    def __repr__(self):
        return '<UserHC: {} >'.format(self.full_name)


class StaffUser(UserHC):

    class Meta(UserHC.Meta):
        proxy = True
        verbose_name = 'Staff User'
        verbose_name_plural = 'Staff Users'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # The folowing modifies the defaults for all of UserHC. This is true even class Meta does not mention UserHC
        # self._meta.get_field('is_student').default = False
        # self._meta.get_field('is_teacher').default = True


class StudentUser(UserHC):

    class Meta(UserHC.Meta):
        proxy = True
        verbose_name = 'Student User'
        verbose_name_plural = 'Student Users'
