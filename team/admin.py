from django.contrib import admin
from team.models import Team


class TeamAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "get_member", )
    list_display_links = ("id", "name", )
    search_fields = ("name", )
    filter_horizontal = ("member", )
    fields = ("name", "member", )

    def get_member(self, obj):
        return ' '.join([i.full_name for i in obj.member.all()])

    get_member.short_description = "成员"

    # def save_model(self, request, obj, form, change):
    #     if not change:  # 新增时
    #         self.model.objects.create(name=obj.name)
    #         current_object = self.model.objects.get(pk=obj.pk)
    #         current_object.member.set(member=obj.member)
    #     super(TeamAdmin, self).save_model(request, obj, form, change)


admin.site.register(Team, TeamAdmin)
