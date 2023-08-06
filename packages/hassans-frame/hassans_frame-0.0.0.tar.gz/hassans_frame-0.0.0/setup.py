from setuptools import setup,Extension,find_packages
classifiers=[
'Development Status :: 5 - Production/Stable',
'Intended Audience :: Developers',
'Operating System :: Microsoft :: Windows :: Windows 10',
'License :: OSI Approved :: MIT License',
'Programming Language :: Python :: 3.7'
]
with open("README.txt","r") as fh:
     long_discription=fh.read()

setup(name="hassans_frame",
     # version="1.0.0",
     discription="It count the frequency of words",
     long_description=long_discription,
     long_description_content_type="text/markdown",
     url="",
     author="Syed M Ahmed Hassan Shah",
     author_email="ahmedhassan.11012@gmail.com",
     classifiers=classifiers,
     keywords=['text processing','data analysis','data science'],
     packages=find_packages(),
     install_requires=["Pandas"]
     )