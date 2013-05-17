The docs are definitely still "TODO", but here are a few notes to keep in mind as we're moving forward.

Import/Export Buttons
---------------------

We've included our own `admin/change_list.html`, which includes `nomnom/object_tools_links.html`. For use with Grappelli, we've also include `admin/grappelli_change_list.hmtl`. If you're using Grappelli for your backend:

 * copy `<env>/lib/pythonX.Y/site-packages/nomnom/templates/admin/grappelli_change_list.html` to a template directory in your project or app (i.e. `~/myproject/myapp/templates/admin/grappelli_change_list.html`)
 * rename `grappelli_change_list.html` to `change_list.html`

We'll eventually come up with a brilliant way to only swap out only `{% block object-tools-items %}`, but for now this lets us move forward.


Tested with
-----------

 * Django 1.4.5
 * Grappelli 2.4.4