Pswrd.py
========

Simple passwords management util. It doesn't store passwords anywhere, generating on the fly.

Usage:
------

Input master password, user name, domain name, service type (web/email/etc.) and press **get** button.

Screenshots:
------------

![Master password prompt](https://telegra.ph/file/67dd8e789a251e805c5fc.jpg "Master password prompt")
![Main screen](https://telegra.ph/file/724c3fcd60efea690f17f.jpg "Main screen")
![Result screen](https://telegra.ph/file/f290d776b0b4753e32d14.jpg "Result screen")
![Result screen](https://telegra.ph/file/80d2b6863a8f50bc6442a.jpg "Result screen")

Additional mode: generatig password using any input file as a key instead of filling info into the form.

![Using any file as a key](https://telegra.ph/file/9c6db926a948b1454ab33.jpg "Using any file as a key")

Notes:
------

There is a cli version of this util written as pure shell script: https://github.com/rekcuFniarB/pswrd#readme

Why this wheel was reinvented? Well, I needed a simple util which doesn't require syncing data between devices.

Requirements:
-------------

* Python
* [Kivy](https://kivy.org/)

Builds:
-------

Linux 64bit and Android unsigned builds: https://github.com/rekcuFniarB/pswrd.py/releases/tag/v0.5a
