from celery import shared_task
import time
import os, requests

@shared_task
def add(x,y):
    time.sleep(5)
    return x+y


@shared_task
def download_image(image_url, save_directory, image_name):
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    image_path = os.path.join(save_directory, image_name)
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        with open(image_name,'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
    return image_url
# from .models import News

# @shared_task
# def create_news():
#     News.objects.create(
#         title ="title",
#         description = "description",
#         image = ,
#         external_link = 
#     )