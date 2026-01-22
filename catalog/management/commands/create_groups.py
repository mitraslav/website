from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from products_proj.models import Product

class Command(BaseCommand):
    help = "Create product moderator group and assign permissions"

    def handle(self, *args, **kwargs):
        content_type = ContentType.objects.get_for_model(Product)
        try:
            perm_unpublish = Permission.objects.get(codename='can_unpublish_product', content_type=content_type)
        except Permission.DoesNotExist:
            self.stderr.write("Permission can_unpublish_product not found. Run makemigrations/migrate after adding it.")
            return

        try:
            perm_delete = Permission.objects.get(codename='delete_product', content_type=content_type)
        except Permission.DoesNotExist:
            self.stderr.write("Permission delete_product not found.")
            return

        group, created = Group.objects.get_or_create(name='Product Moderators')
        group.permissions.add(perm_unpublish, perm_delete)
        group.save()
        self.stdout.write(self.style.SUCCESS(f"Group '{group.name}' created/updated with permissions."))