import json

import docker
from docker.errors import NotFound

# input field
PROJECT_NAME = 'simple_flask_app'
VERSION = '0.1'

# will made use input field
IMAGE_TAG = '%s:%s' % (PROJECT_NAME, VERSION)
CONTANIER_NAME = '%s_cont' % PROJECT_NAME

HOST_PORT = 5000
CONT_PORT = 5000

CLIENT = docker.from_env()
CLIENT_API = docker.APIClient(base_url='unix://var/run/docker.sock')


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
    print('start build')

    generator = CLIENT_API.build(tag=name, path=path)

    for output in generator:
        oo = output.decode('utf-8').strip('\r\n')
        json_output = json.loads(oo)

        if 'stream' in json_output:
            print(json_output['stream'].strip('\n'))

    return find_image(IMAGE_TAG)


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

    cont = run_container(CONTANIER_NAME, HOST_PORT, CONT_PORT, IMAGE_TAG)
    print('run container(%s)' % cont.name)


run()
