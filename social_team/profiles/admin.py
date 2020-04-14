from django.contrib import admin

from profiles import models


class MainSkillAdmin(admin.ModelAdmin):
    model = models.MainSkill


class OtherSkillAdmin(admin.ModelAdmin):
    model = models.OtherSkill


class UserProjectAdmin(admin.ModelAdmin):
    model = models.UserProject


admin.site.register(models.MainSkill, MainSkillAdmin)
admin.site.register(models.OtherSkill, OtherSkillAdmin)
admin.site.register(models.UserProject, UserProjectAdmin)
