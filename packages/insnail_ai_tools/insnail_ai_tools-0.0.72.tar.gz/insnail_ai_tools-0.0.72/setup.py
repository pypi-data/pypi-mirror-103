#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['insnail_ai_tools',
 'insnail_ai_tools.elastic_search',
 'insnail_ai_tools.elastic_search.documents',
 'insnail_ai_tools.elastic_search.documents.ontology',
 'insnail_ai_tools.extractor',
 'insnail_ai_tools.mongodb',
 'insnail_ai_tools.mongodb.model',
 'insnail_ai_tools.mongodb.model.ontology',
 'insnail_ai_tools.mongodb.model.wecom',
 'insnail_ai_tools.web',
 'insnail_ai_tools.web.django',
 'insnail_ai_tools.web.fastapi',
 'insnail_ai_tools.wechatpy',
 'insnail_ai_tools.wechatpy.work']

package_data = \
{'': ['*']}

extras_require = \
{'dev': ['flit ==3.0.0',
         'ipython ==7.18.1',
         'jedi ==0.17.2',
         'pre-commit ==2.9.3',
         'black ==20.8b1',
         'isort ==5.6.4',
         'flake8 ==3.8.4',
         'pytest ==6.2.1',
         'pytest-cov ==2.10.1',
         'pytest-asyncio ==0.14.0'],
 'django': ['django ==3.1.4', 'gunicorn ==20.0.4'],
 'es': ['elasticsearch-dsl ==7.3.0'],
 'fastapi': ['fastapi[all] ==0.62.0',
             'starlette ==0.13.6',
             'pydantic ==1.6.1',
             'uvicorn ==0.11.8'],
 'flask': ['flask ==1.1.2', 'flask-cors ==3.0.9', 'gunicorn ==20.0.4'],
 'mongo': ['motor ==2.3.1', 'pymongo ==3.11.3', 'mongoengine ==0.22.1'],
 'mussy': ['asyncio ==3.4.3',
           'apollo-client ==0.9.2',
           'pyyaml ==5.3.1',
           'requests ==2.24.0',
           'fire ==0.3.1',
           'aiohttp ==3.7.3',
           'tqdm ==4.50.2'],
 'oss': ['oss2 ==2.13.0'],
 'sso': ['redis ==3.5.3', 'python-jose ==3.2.0'],
 'tx': ['tencentcloud-sdk-python ==3.0.341'],
 'wechat': ['wechatpy ==2.0.0a5']}

entry_points = \
{'console_scripts': ['snail = insnail_ai_tools.cli:main']}

setup(name='insnail_ai_tools',
      version='0.0.72',
      description='Insnail Ai Tools',
      author='Insnail Ai Team',
      author_email='libiao@ingbaobei.com',
      url='https://github.com/pypa/insnail_ai_tools',
      packages=packages,
      package_data=package_data,
      extras_require=extras_require,
      entry_points=entry_points,
      python_requires='>=3.6',
     )
