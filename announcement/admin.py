from django.contrib import admin
from announcement.models import Announcement, AnnouncementRecord
import datetime


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "title", "content", "get_to_group", "get_to_people", "require_upload",
                    "get_unread_count", "edit_datetime", "url_address", "active")
    list_display_links = ("id", "title",)
    search_fields = ("author", "title", "content",)
    filter_horizontal = ('to_group', 'to_people',)
    fields = ('title', 'content', 'to_group', 'to_people', 'require_upload', 'deadline', 'author', 'get_to_group',
              'get_to_people', 'get_read_names', 'get_unread_names', 'get_read_count', 'get_unread_count',
              'issue_datetime', 'edit_datetime', 'url_address', "active")  # 设置添加/修改详细信息时，哪些字段显示，在这里 remark 字段将不显示
    readonly_fields = ('author', 'get_to_group', 'get_to_people', 'get_read_names', 'get_unread_names',
                       'get_read_count', 'get_unread_count', 'issue_datetime', 'edit_datetime',)

    def get_to_group(self, obj):
        return ' '.join([i.name for i in obj.to_group.all()])

    get_to_group.short_description = "阅读组"

    def get_to_people(self, obj):
        return ' '.join([i.full_name for i in obj.to_people.all()])

    get_to_people.short_description = "阅读人"

    def get_names(self, obj):
        to_group_obj = obj.to_group.all()
        to_people_obj = obj.to_people.all()
        to_people = [i.full_name for i in to_people_obj] if len(to_people_obj) != 0 else []
        if len(to_group_obj) != 0:
            for group_obj in to_group_obj:
                group_mamber = [i.full_name for i in group_obj.member.all()]
                to_people += group_mamber
        if len(to_people) != 0:
            to_people = list(set(to_people))
        read_names = AnnouncementRecord.objects.filter(aid=obj.id)
        read_names = list(read_names.values_list("reader", flat=True))
        unread_names = [name for name in to_people if name not in read_names] if len(read_names) != 0 else to_people
        return read_names, unread_names

    # 定义list_display中的自定义方法
    def get_read_count(self, obj):
        read_names, _ = self.get_names(obj)
        return len(read_names)

    get_read_count.short_description = u'已读人数'

    # 定义list_display中的自定义方法
    def get_unread_count(self, obj):
        _, unread_names = self.get_names(obj)
        return len(unread_names)

    get_unread_count.short_description = u'未读人数'

    # 定义read_only_fields中的自定义方法
    def get_read_names(self, obj):
        read_names, _ = self.get_names(obj)
        return ' '.join(read_names)

    get_read_names.short_description = u'已读人员'

    # 定义fields中的自定义方法
    def get_unread_names(self, obj):
        _, unread_names = self.get_names(obj)
        return ' '.join(unread_names)

    get_unread_names.short_description = u'未读人员'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        user = request.user.full_name
        obj.author = user
        # request.META储存客户端header信息，是个字典
        obj.url_address = '标题:' + obj.title + '\n截止时间:' + datetime.datetime.strftime(obj.deadline, "%Y-%m-%d %H:%M:%S") + '\nhttp://' + request.META['HTTP_HOST'] + "/announcement/" + str(obj.id)
        obj.save()


class AnnouncementRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "aid", "reader", "read_datetime", "image", "read_status")
    list_display_links = ("id",)
    search_fields = ("reader",)
    readonly_fields = ("aid", "reader", "read_datetime", "image", "read_status")


admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(AnnouncementRecord, AnnouncementRecordAdmin)
