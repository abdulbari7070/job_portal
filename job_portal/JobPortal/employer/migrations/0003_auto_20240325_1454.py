from django.db import migrations


def create_default_skills(apps, schema_editor):
    Skill = apps.get_model('employer', 'Skill')
    default_skills = ['PHP', 'Java', '.Net', 'Python', 'Ruby']
    for skill_name in default_skills:
        Skill.objects.get_or_create(name=skill_name)


class Migration(migrations.Migration):

    dependencies = [
        ("employer", "0002_skill_job"),
    ]

    operations = [
        migrations.RunPython(create_default_skills),
        ]
