from django.utils import timezone
from announcement.models import Announcement
import os
from teamwork import settings
from announcement.models import image_path


def clean_expired_data():
    data = Announcement.objects.filter(deadline__lte=timezone.now(), active=True)
    if len(data) > 0:
        data_id = list(set(data.values_list("id", flat=True)))
        data.update(content="已过期", active=False)
        data_id = [str(i) for i in data_id]
        dir = os.path.join(settings.MEDIA_ROOT, image_path)
        for file in os.listdir(dir):
            if file.startswith(tuple(data_id)):
                os.remove(os.path.join(dir, file))
