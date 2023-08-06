README
######

Welcome to OLIB, an object library.

OLIB is an object library you can use to program with objects, uses a JSON
in file database with a versioned readonly storage and reconstructs objects
based on type information in the path. 

OLIB is placed in the Public Domain and has no COPYRIGHT and no LICENSE.

INSTALL
=======

OLIB can be found on pypi, see http://pypi.org/project/olib

installation is through pypi::

 $ sudo pip3 install olib --upgrade --force-reinstall

PROGRAMMING
===========

OLIB provides a library you can use to program objects under python3. It 
provides a basic Object, that mimics a dict while using attribute access
and provides a save/load to/from json files on disk. Objects can be
searched with a little database module, provides read-only files to
improve persistence and use a type in filename reconstruction.

basic usage is this:

 >>> from obj import Object
 >>> o = Object()
 >>> o.key = "value"
 >>> o.key
 'value'
 >>> o
 {"key": "value"}

objects can be saved and loaded to JSON files:

 >>> from obj import Object, cfg
 >>> cfg.wd = "data"
 >>> o = Object()
 >>> o.key = "value"
 >>> path = o.save()
 >>> path
 'obj.Object/4b58abe2-3757-48d4-986b-d0857208dd96/2021-04-12/21:15:33.734994
 >>> oo = Object().load(path)
 >>> oo.key
 'value'

an Object tries to mimic a dictionary while trying to be an object with normal
attribute access as well. Hidden methods are provided as are the basic
methods like get, items, keys, register, set, update, values.

great for giving objects peristence by having their state stored in files.

CONTACT
=======

have fun coding

| Bart Thate (bthate67@gmail.com)
| botfather on #dunkbots irc.freenode.net
