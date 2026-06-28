from django.db import models

from core.models import UUIDBaseModel

class Menu(UUIDBaseModel):

    cook = models.OneToOneField(
        "cooks.CookProfile",
        on_delete=models.CASCADE,
        related_name="menu"
    )

    title = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"

    def __str__(self):
        return self.title
    
class MenuItem(UUIDBaseModel):

    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name="items"
    )

    name = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    price = models.PositiveIntegerField(help_text="Price in Toman")

    image = models.ImageField(
        upload_to="menu_items/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    favorites_count = models.PositiveIntegerField(
    default=0
    )
    
    orders_count = models.PositiveIntegerField(
    default=0
    )
    
    average_rating = models.DecimalField(
    max_digits=3,
    decimal_places=2,
    null=True,
    blank=True,
    default=None
)

    class Meta:
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"

    def __str__(self):
        return self.name
    
class MenuItemAvailability(UUIDBaseModel):

    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        related_name="availabilities"
    )

    date = models.DateField()

    max_quantity = models.PositiveIntegerField()

    reserved_quantity = models.PositiveIntegerField(
        default=0
    )

    class Meta:

        constraints = [
        models.UniqueConstraint(
            fields=["menu_item", "date"],
            name="unique_menu_item_date"
        )
    ]

        verbose_name = "Menu Item Availability"
        verbose_name_plural = "Menu Item Availabilities"

    def __str__(self):
        return (
            f"{self.menu_item.name}"
            f" - {self.date}"
        )
