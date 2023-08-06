Script has a goal to capture and count tags from the site. You can either
use terminal version or UI. There is possibility to use aliases for
sites (you can edit it in file **synonims.yaml** (site-packages/tagscounteralexdoka/...))

1 step
~~~~~~~

First step is creating Db for tags. (optional, if it does not exist)

.. code:: bash

   tagcounter --createdb

2 step
~~~~~~

To use terminal version (to load tags info to DB), you can run commans
like:

.. code:: bash

   tagcounter --get google.com
   # or if use alias
   tagcounter --get tut

.. _step-1:

3 step
~~~~~~

To show info from DB use :

.. code:: bash

   tagcounter --show google.com
   # or if use alias
   tagcounter --show tut

If you run script without parameters, program will start with UI, with
the same functionality.
