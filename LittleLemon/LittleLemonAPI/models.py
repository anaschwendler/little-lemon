from django.db import models

# Create your models here.
class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255) 
    
    def __str__(self) -> str:
        return self.title
    
    @classmethod
    def get_default_pk(cls):
        category, created = cls.objects.get_or_create(
            title="category one",
        )
        return category.pk

class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.SmallIntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=Category.get_default_pk)
