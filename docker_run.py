import docker
from docker.errors import NotFound

PROJECT_NAME = 'simple_flask_app'
VERSION = '0.1'

IMAGE_TAG = '%s:%s' % (PROJECT_NAME, VERSION)

CONTANIER_NAME = '%s_cont' % PROJECT_NAME

CLIENT = docker.from_env()


def find_image(imagename):
    list = CLIENT.images.list()
    for img in list:
        for tag in img.tags:
            if imagename in tag:
                return img


def find_container(name):
    list = CLIENT.containers.list()
    for cont in list:
        for tag in cont.tags:
            if name in tag:
                return cont


def build_image(name, path):
    return CLIENT.images.build(tag=name, path=path)[0]


def remove_image(name):
    return CLIENT.images.remove(name)


def run_container(name, host_posrt, container_port, image_tag):
    host_key = '%s/tcp' % host_posrt
    return CLIENT.containers.run(name=name, detach=True, ports={host_key: container_port}, image=image_tag)


def if_exist_img_then_remove(project_name):
    img = find_image(project_name)
    if img is not None:
        tag = img.tags[0]
        remove_image(img.id)
        print('remove image(%s)' % tag)


def if_exist_cont_then_remove(contanier_name):
    try:
        cont = CLIENT.containers.get(contanier_name)

        cont_name = cont.name
        cont.remove(force=True)
        print('remove container(%s)' % cont_name)
    except NotFound as e:
        print('not exist constainer(%s)' % contanier_name)


def run():
    if_exist_cont_then_remove(CONTANIER_NAME)
    if_exist_img_then_remove(PROJECT_NAME)

    img = build_image(IMAGE_TAG, '.')
    print('build image(%s)' % img.tags[0])

    cont = run_container(CONTANIER_NAME, 5000, 5000, IMAGE_TAG)
    print('run container(%s)' % cont.name)


run()
