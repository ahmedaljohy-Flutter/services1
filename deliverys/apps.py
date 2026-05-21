from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_groups_and_test_users(sender, **kwargs):
    if sender.name != 'deliverys':
        return
        
    from django.contrib.auth.models import Group, Permission, User
    from django.contrib.contenttypes.models import ContentType
    
    # 1. إنشاء المجموعات
    manager_group, _ = Group.objects.get_or_create(name='Manager')
    employee_group, _ = Group.objects.get_or_create(name='Employee')
    
    # 2. جلب وتعيين صلاحيات التوصيل
    try:
        content_type = ContentType.objects.get(app_label='deliverys', model='delivery')
        permissions = Permission.objects.filter(content_type=content_type)
        
        # يحصل المدير على صلاحيات الإضافة والتعديل والحذف
        for perm in permissions:
            if perm.codename in ['add_delivery', 'change_delivery', 'delete_delivery']:
                manager_group.permissions.add(perm)
    except ContentType.DoesNotExist:
        pass
        
    # 3. إنشاء مستخدمين تجريبيين للتجربة المباشرة وسرعة التحقق
    if not User.objects.filter(username='manager').exists():
        manager_user = User.objects.create_user(username='manager', email='manager@example.com', password='manager123')
        manager_user.groups.add(manager_group)
        manager_user.is_staff = True  # ليتمكن من دخول لوحة التحكم أيضاً إن أراد
        manager_user.save()
        
    if not User.objects.filter(username='employee').exists():
        employee_user = User.objects.create_user(username='employee', email='employee@example.com', password='employee123')
        employee_user.groups.add(employee_group)
        employee_user.save()

    # إنشاء مستخدم مسؤول (Superuser) للتجربة الشاملة
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(username='admin', email='admin@example.com', password='admin123')

class DeliverysConfig(AppConfig):
    name = "deliverys"

    def ready(self):
        post_migrate.connect(create_groups_and_test_users, sender=self)
