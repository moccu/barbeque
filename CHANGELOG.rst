Changelog
=========

1.4.2 - 2017-02-10
------------------

* Fix broken release.


1.4.1 - 2017-02-10
------------------

* Fix various bugs in floppyforms templates


1.4.0 - 2017-01-23
------------------

* Add default floppyforms templates
* Fix compatibility bug with OpenPyXL (for exporter module)


1.3.0 - 2016-12-08
------------------

* WARNING: create_error_pages is deprectated. Use render_static_templates instead.


1.3.1 - 2016-12-14
------------------

* Add python-dateutil to intall dependencies, required by barbeque.validators


1.3.0 - 2016-12-08
------------------

* WARNING: create_error_pages is deprectated. Use render_static_templates instead.
* Add render_static_templates command to render templates as static files


1.2.0 - 2016-11-30
------------------

* WARNING: barbeque.forms was moved to barbeque.forms.mixins - update your imports!
* Refactor UploadToPath to be deconstructable for Django migrations
* Add new mixin for floppyforms.Form to have another render helper (as_div)
* Add FieldsetRenderer to allow rendering of partial forms
* Add cms toolbar baseclass to easily insert title extensions to page menu
* Add template tag to fetch a title extension instance for a cms page
* FilerFileField now sets blank=True if null=True and other way around
* Speed up tests


1.1.1 - 2016-11-22
------------------

* Fix bug when compressor is not installed and Django tries to import buildcompress.


1.1.0 - 2016-11-07
------------------

* Add module for handling staticfiles when working with docker


1.0.1 - 2016-07-15
------------------

* Fix bug when using django-compressor 2.0


1.0.0 - 2016-05-04
------------------

* Dropped support for Django < 1.8 and Django-CMS < 3.2


0.4.0 - 2016-02-10
------------------

* Added buildcompress tag


0.3.0 - 2015-10-09
------------------

* Added django 1.8 and python 3.5 support
* Dropped django 1.5 support


0.2.1 - 2015-03-13
------------------

* Added management command to create static errorpages
* Added "set" template tag to allow context updates in without using the "with" tag.


0.2 - 2015-03-13
----------------

* Refactored library structure
* Added many new features


0.1 - 2014-06-15
----------------

* Initial release.
