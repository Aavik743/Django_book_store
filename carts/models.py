from django.db import models

from accounts.models import User
from books.models import Book


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    book_quantity = models.IntegerField()
    total_price = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.book.name

    @staticmethod
    def add_to_cart_validation(user, book, cart, book_quantity):
        if book:
            if book.book_quantity >= book_quantity:
                if cart:
                    if cart.user == user:
                        if cart.book == book:
                            cart.book_quantity += book_quantity
                            book.book_quantity -= book_quantity
                            cart.total_price = cart.book_quantity * book.price
                            cart.save()
                            book.save()
                        book.book_quantity -= book_quantity
                        total_price = book.price * book_quantity

                        cart = Cart.objects.create(user=user, book=book,
                                                   book_quantity=book_quantity, total_price=total_price)
                        cart.save()
                        book.save()
                book.book_quantity -= book_quantity
                total_price = book.price * book_quantity

                cart = Cart.objects.create(user=user, book=book,
                                           book_quantity=book_quantity, total_price=total_price)
                cart.save()
                book.save()

    @staticmethod
    def update_cart_validation(user, request):
        cart = Cart.objects.filter(user=user).first()
        book = Book.objects.filter(pk=cart.book_id).first()
        if book:
            if cart:
                book_quantity = int(request.data.get('book_quantity'))

                if cart.book_quantity > book_quantity:
                    count = cart.book_quantity - book_quantity

                    book.book_quantity += count

                if cart.book_quantity < book_quantity:
                    count = book_quantity - cart.book_quantity

                    book.book_quantity -= count

                cart.book_quantity = book_quantity
                cart.save()
                book.save()
                return cart.book_quantity
