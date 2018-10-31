import docker

PROJECT_NAME = 'simple_flask_app'
VERSION = '0.1'

IMAGE_TAG = '%s/%s' % (PROJECT_NAME, VERSION)

CLIENT = docker.from_env()

def find_image(imagename):
    list = CLIENT.images.list()
    for img in list:
        for tag in img.tags:
            if imagename in tag:
                return img



img = find_image('flask')
print(img)

