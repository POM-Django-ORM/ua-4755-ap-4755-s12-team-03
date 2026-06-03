from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


ROLE_CHOICES = (
    (0, 'visitor'),
    (1, 'admin'),
)


class CustomUser(AbstractBaseUser):

    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=20, null=True, blank=True)
    middle_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    role = models.IntegerField(choices=ROLE_CHOICES, default=0)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return (
            f"'id': {self.id}, "
            f"'first_name': '{self.first_name}', "
            f"'middle_name': '{self.middle_name}', "
            f"'last_name': '{self.last_name}', "
            f"'email': '{self.email}', "
            f"'created_at': {int(self.created_at.timestamp())}, "
            f"'updated_at': {int(self.updated_at.timestamp())}, "
            f"'role': {self.role}, "
            f"'is_active': {self.is_active}"
        )

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    @staticmethod
    def get_by_id(user_id):
        """
        Return user by id or None.
        """
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def get_by_email(email):
        """
        Return user by email or None.
        """
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def delete_by_id(user_id):
        """
        Delete user by id.
        Return True if deleted, False otherwise.
        """
        user = CustomUser.get_by_id(user_id)

        if user:
            user.delete()
            return True

        return False

    @staticmethod
    def create(
        email,
        password,
        first_name=None,
        middle_name=None,
        last_name=None
    ):
        """
        Create user if data is valid.
        Return user object or None.
        """

        try:
            validate_email(email)
        except ValidationError:
            return None

        if CustomUser.objects.filter(email=email).exists():
            return None

        if first_name is not None and len(first_name) > 20:
            return None

        if middle_name is not None and len(middle_name) > 20:
            return None

        if last_name is not None and len(last_name) > 20:
            return None

        try:
            user = CustomUser(
                email=email,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name
            )

            user.set_password(password)
            user.save()

            return user

        except Exception:
            return None

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': int(self.created_at.timestamp()),
            'updated_at': int(self.updated_at.timestamp()),
            'role': self.role,
            'is_active': self.is_active,
        }

    def update(
        self,
        first_name=None,
        last_name=None,
        middle_name=None,
        password=None,
        role=None,
        is_active=None
    ):
        if first_name is not None:
            self.first_name = first_name

        if last_name is not None:
            self.last_name = last_name

        if middle_name is not None:
            self.middle_name = middle_name

        if password is not None:
            self.set_password(password)

        if role is not None:
            self.role = role

        if is_active is not None:
            self.is_active = is_active

        self.save()

    @staticmethod
    def get_all():
        return list(CustomUser.objects.all())

    def get_role_name(self):
        return dict(ROLE_CHOICES).get(self.role)
