from django.db import models
from django.utils import timezone

from authentication.models import CustomUser
from book.models import Book


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    created_at = models.DateTimeField()
    end_at = models.DateTimeField(null=True, blank=True)
    plated_end_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        end_at = (
            "None"
            if self.end_at is None
            else f"'{self.end_at}'"
        )

        return (
            f"'id': {self.id}, "
            f"'user': {repr(self.user)}, "
            f"'book': {repr(self.book)}, "
            f"'created_at': '{self.created_at}', "
            f"'end_at': {end_at}, "
            f"'plated_end_at': '{self.plated_end_at}'"
        )

    def __repr__(self):
        return f"Order(id={self.id})"

    @staticmethod
    def get_by_id(order_id):
        try:
            return Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return None

    @staticmethod
    def delete_by_id(order_id):
        try:
            order = Order.objects.get(id=order_id)
            order.delete()
            return True
        except Order.DoesNotExist:
            return False

    @staticmethod
    def create(user, book, plated_end_at):
        if user.id is None:
            return None

        if book.count <= 1:
            return None

        try:
            order = Order(
                user=user,
                book=book,
                created_at=timezone.now(),
                plated_end_at=plated_end_at
            )
            order.save()

            book.count -= 1
            book.save()

            return order

        except Exception:
            return None

    def update(self, plated_end_at=None, end_at=None):
        if plated_end_at is not None:
            self.plated_end_at = plated_end_at

        if end_at is not None:
            self.end_at = end_at

        self.save()

    @staticmethod
    def get_all():
        return list(Order.objects.all())

    @staticmethod
    def get_not_returned_books():
        return list(Order.objects.filter(end_at=None))

    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user.id,
            'book': self.book.id,
            'created_at': self.created_at,
            'end_at': self.end_at,
            'plated_end_at': self.plated_end_at,
        }
