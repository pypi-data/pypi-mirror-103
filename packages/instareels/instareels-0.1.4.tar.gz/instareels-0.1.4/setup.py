from  setuptools import setup
setup(name="instareels",
version="0.1.4",description="This can download instagram reels",author="@tanay_mishra",packages=['download_reels'],
author_email="tanaymishra2204@gmail.com",install_requires=['requests-HTML','requests','wheel','libxml2','libxslt','libiconv'],
long_description="""This module can download Instagram reels video 
to download import download function from module and call with parameters 
like that download('link','videos/video.mp4')..
Just Visit : "https://github.com/tanaymishra/reels" to get the code..
and visit "https://github.com/tanaymishra/Reels-instruction For instruction
Instruction:-
pip3/pip install instareels

from download_reels import download

download("link","name.mp4")

That is it your module video will be downloaded in few seconds.
"
"""
)