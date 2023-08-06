from setuptools import setup

setup(
   name='discogslearner',
   version='0.1',
   license = "GPL-3.0",
   description='Machine Learning module for Discogs',
   author='Pascal Maas',
   author_email='p.maas92@gmail.com',
   packages=['discogslearner'],
   install_requires=['pandas', 'tqdm', 'numpy', "sklearn", "discogs_client"],
   url = "https://github.com/Pascallio",
   download_url = "https://github.com/Pascallio/DiscogsLearner/archive/refs/tags/v0.1.tar.gz",
   keywords = ["Discogs", "Machine Learning"]
)