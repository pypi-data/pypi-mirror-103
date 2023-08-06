# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drf_imgproxy']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.1.0', 'djangorestframework>=3.9.0']

setup_kwargs = {
    'name': 'drf-imgproxy',
    'version': '1.1.0',
    'description': "Serialize Django's ImageField into imgproxy URLs for your Django REST Framework APIs to generate thumbnails.",
    'long_description': "############\ndrf-imgproxy\n############\n\nSerialize Django's ImageField into `imgproxy\n<https://github.com/imgproxy/imgproxy>`_ URLs for your Django REST\nFramework APIs to generate thumbnails.\n\n****************\nImportant Notice\n****************\n\nThis package only provides the serializer class necessary to translate\nyour ImageField to signed imgproxy URLs.\n\nIt does not provide anything to upload images to your object storage\nbucket. We suggest you use another Django storage backend library\nthat's able to communicate with your object storage solution, in\nparticular we recommend the following:\n\n* `django-storages <https://github.com/jschneier/django-storages>`_\n* `django-minio-storage\n  <https://github.com/py-pa/django-minio-storage>`_\n\n*****\nUsage\n*****\n\n0. Installation\n===============\n\nYou can easily install this package from PyPI with ``pip`` by doing:\n\n.. code:: bash\n\n   pip install drf-imgproxy\n\n\n1. Quickstart\n=============\n\nIn ``settings.py``:\n\n.. code:: python\n\n   INSTALLED_APPS = [\n     ...\n     'drf_imgproxy',\n     ...\n   ]\n\n   # Configure this to either of the following:\n   #  - 's3' for Amazon S3, Minio and any other S3-compatible object\n   #    storage\n   #  - 'gs' for Google Cloud Storage\n   #  - 'abs' for Azure Blob Storage\n   IMGPROXY_PROTOCOL = 's3'\n\n   # Set the following to the bucket name that imgproxy uses.\n   IMGPROXY_BUCKET_NAME = 'nerv_angel_captures'\n\n   # Set both of the following to the appropiate values of\n   # `IMGPROXY_KEY` and `IMGPROXY_SALT` of your imgproxy server.\n   IMGPROXY_KEY = 'ThisIsNotASecureKeyAtAll'\n   IMGPROXY_SALT = 'SeriouslyThisSaltIsVeryInsecure'\n\n   # Set the following to the publicly accessible URL of your imgproxy\n   # server.\n   IMGPROXY_HOST = 'https://imgproxy.infra.nerv.tld'\n\n   # Set the following variable to the available resolutions your API\n   # provides.\n   #\n   # The format is `(<width>, <height>)`.\n   IMGPROXY_RESOLUTIONS = (\n       (640,  480),\n       (800,  600),\n       (1024, 768),\n   )\n\n   # In case you want to skip imgproxy url generation, set this flag to True.\n   # When generation is being skipped, all the resolutions return the url of\n   # the source file if possible or None.\n   IMGPROXY_SKIP = False\n\nIn ``serializers.py``:\n\n.. code:: python\n\n   ...\n   from drf_imgproxy.serializers import ImgproxyResizeableImageField\n   ...\n\n\n   class AngelActivity(ModelSerializer):\n       ...\n       captured_photo_thumbs = ImgproxyResizeableImageField(\n           read_only=True,\n           source='captured_photo'\n       )\n       ...\n\n********\nSee also\n********\n\n* `drf-imgproxy-demo <https://github.com/viper-development/drf-imgproxy-demo>`_\n",
    'author': 'VIPER Development UG',
    'author_email': 'info@viper.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/viper-development/drf-imgproxy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
