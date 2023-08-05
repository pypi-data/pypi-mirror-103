from setuptools import setup, find_packages

setup(name='hawksoft.tools',
      version='1.0.1',
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # 多文件模块写法
      author="xingyongkang",
      author_email="xingyongkang@cqu.edu.cn",
      description="Provides many useful command lines in python",
      long_description=open('./README.md', encoding='utf-8').read(),
      long_description_content_type = "text/markdown",
      #long_description="http://gitee.comg/xingyongkang",
      license="MIT",
      url="https://github.com/xingyongkang",
      include_package_data=True,
      platforms="any",
      #install_requires=[],
      keywords='md2zhihu tree ',
      entry_points={
          'console_scripts': [
              'md2zhihu=hawksoft.md2zhihu:main',
              'tree=hawksoft.tree:main'
          ]
      },
)