from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
    ('home', '0001_initial'),
]
    operations = [
        migrations.CreateModel(
            name='Gasto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('descripcion', models.CharField(max_length=200)),
                ('monto', models.DecimalField(max_digits=12, decimal_places=2)),
                ('usuario', models.ForeignKey(null=True, on_delete=models.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]