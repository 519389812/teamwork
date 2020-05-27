from django.shortcuts import render, redirect, reverse
from user.models import User
from django.contrib.auth.hashers import check_password
import os
from announcement.models import Announcement, AnnouncementRecord
from django.http import HttpResponse
from PIL import Image
from announcement.models import image_path
from teamwork import settings
from teamwork.settings import MEDIA_URL
# from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from django.utils import timezone


def check_authority(func):
    def wrapper(*args, **kwargs):
        username = args[0].session.get("login_user", "")
        if username == "":
            args[0].session["path"] = args[0].path
            return redirect(reverse("login"))
        return func(*args, **kwargs)
    return wrapper


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
            is_valid = check_password(password, user.password)
        except:
            is_valid = False
        if is_valid:
            request.session["login_user"] = username
            request.session.set_expiry(1209600)
            return redirect(request.session["path"])
        else:
            return HttpResponse("登录失败，请确认用户名和密码是否正确")
    else:
        return render(request, "login.html")


@check_authority
def make_announcement(request, id):
    current_username = request.user.full_name
    announcement = Announcement.objects.get(id=id)
    to_group_obj = announcement.to_group.all()
    to_people_obj = announcement.to_people.all()
    to_people = [i.full_name for i in to_people_obj] if len(to_people_obj) != 0 else []
    to_people_extend = to_people.copy()
    group_dict = {}
    if len(to_group_obj) != 0:
        for group_obj in to_group_obj:
            group_mamber = [i.full_name for i in group_obj.member.all()]
            group_dict[group_obj.name] = [group_mamber]
            to_people_extend += group_mamber
    if len(to_people_extend) != 0:
        to_people_extend = list(set(to_people_extend))
    read_names = AnnouncementRecord.objects.filter(aid=id)
    read_names = list(read_names.values_list("reader", flat=True))
    if current_username not in to_people_extend:
        is_read = True
    else:
        is_read = True if current_username in read_names else False
    if len(read_names) != 0:
        if len(group_dict) != 0:
            for name, member in group_dict.items():
                group_dict[name].append([i for i in read_names if i in member[0]])
                group_dict[name].append([i for i in member[0] if i not in member[1]])
        unread_names = [name for name in to_people if name not in read_names]
    else:
        if len(group_dict) != 0:
            for name, member in group_dict.items():
                group_dict[name].append([])
                group_dict[name].append(member[0])
        unread_names = to_people
    to_people_length = (len(read_names) + len(unread_names))
    values = {'id': id, 'announcement': announcement, 'group_dict': group_dict, 'read_names': read_names,
              'unread_names': unread_names, 'is_read': is_read, 'to_people_length': to_people_length}
    return render(request, 'announcement.html', values)


@check_authority
def read_confirm(request, id, require_upload):
    # 对应action中 <form action = "{% url 'confirm' id %}" method = "post"> 的 {% url 'confirm' id %} 方法，
    # confirm指向urls.py中name=confirm的url
    user = request.session.get("login_user", "")
    user = User.objects.get(username=user).full_name
    if len(AnnouncementRecord.objects.filter(aid=id, reader=user)) > 0:
        return HttpResponse("您已经提交确认，请勿重复提交！")
    else:
        if require_upload == "True":
            try:
                img = request.FILES["img"]
            except:
                img = None
            if img is not None:
                img_name = img.name.lower()
                if img_name.endswith("jpg") or img_name.endswith("jpeg") or img_name.endswith("png"):
                    img_type = img_name.split(".")[-1]
                    img = Image.open(img)
                    img = img.resize((281, 500))
                    img.save(os.path.join(settings.MEDIA_ROOT, image_path, (id + '_' + user + '.' + img_type)))
                    AnnouncementRecord.objects.create(aid=id, reader=user, image=os.path.join(image_path, (
                                id + '_' + user + '.' + img_type)))
                    return redirect(request.META['HTTP_REFERER'])
                else:
                    return HttpResponse("图片格式错误，请重新上传")
            else:
                return HttpResponse("图片未上传")
        else:
            AnnouncementRecord.objects.create(aid=id, reader=user)
            return redirect(request.META['HTTP_REFERER'])


@check_authority
def show_upload(request, id, names):
    if request.method == "POST":
        values = AnnouncementRecord.objects.filter(aid=id)
        values = {"reader_upload": {values.get(reader=name).reader: values.get(reader=name).image
                                    for name in values.values_list("reader", flat=True) if name in names},
                  "media_url": MEDIA_URL}
        return render(request, "show-upload.html", values)


# scheduler = BackgroundScheduler()
# scheduler.add_jobstore(DjangoJobStore(), "default")
#
#
# @register_job(scheduler, "interval", hours=1, id="clean_expired_data")
# def clean_expired_data():
#     data = Announcement.objects.filter(deadline__lte=timezone.now(), active=True)
#     if len(data) > 0:
#         data_id = list(set(data.values_list("id", flat=True)))
#         data.update(content="已过期", active=False)
#         data_id = [str(i) for i in data_id]
#         dir = os.path.join(settings.MEDIA_ROOT, image_path)
#         for file in os.listdir(dir):
#             if file.startswith(tuple(data_id)):
#                 os.remove(os.path.join(dir, file))
#
#
# register_events(scheduler)
# scheduler.start()


# $(document).ready(function(){
# 	$('#name1').blur(function(){
# 		var name = $('#name1').val();
#
# 		$.get("/validate/",{'name':name}, function(ret){
# 			$('#result1').html(ret);
# 		});
# 	});
# });

# def validate(request):
# 	name = request.GET['name']
# 	namelist = []
# 	allname = Staff.objects.all()
# 	for get in allname:
# 		namelist.append(get.name)
# 	if name in namelist:
# 		return HttpResponse('输入正确！')
# 	elif name == '无':
# 		return HttpResponse('')
# 	else:
# 		return HttpResponse('姓名错误或未录入档案！')
