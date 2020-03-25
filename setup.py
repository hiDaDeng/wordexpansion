from setuptools import setup, find_packages

setup(name='wordexpansion',
      version='0.0.6',
      author='大邓',
      author_email='thunderhit@qq.com',
      url='https://github.com/thunderhit/wordexpansion',
      packages=find_packages(),
      python_requires='>=3.5',
      license="MIT",
      keywords=['knowledge graph', 'text analysis', 'event extraction'],
      long_description=open('README.md').read(), # 读取的Readme文档内容
      long_description_content_type="text/markdown",  # 指定包文档格式为markdown
      )

