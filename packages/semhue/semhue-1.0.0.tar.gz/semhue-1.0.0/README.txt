--------phue python package---------
------------@sempython--------------

Links for uploading code to PyPi:

=>  https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56
=>  https://realpython.com/pypi-publish-python-package/

Steps to upload package to PyPi:

(1) Create an account on https://pypi.org/
(2) Open setup.py, fill the empty strings (author, author_email, description, url)
(3) Open LICENSE.txt, write your name in place of "YOUR NAME"
(4) Once all this is done, open command prompt/terminal and write the following command:

If system is windows:

pip install twine
python setup.py sdist
twine upload dist/*

If any other system:

pip3 install twine
python3 setup.py sdist
twine upload dist/*

(5) Once you type the command `twine upload dist/*`, you'll be asked your PyPi username and password
Insert them, hit enter and your package is uploaded to PyPi!

----------------------------------------------------------------------------------------------------
If any problem arises, feel free to contact me :)
----------------------------------------------------------------------------------------------------

Regards
Devansh (@devansh3712)