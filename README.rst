=====================
django_localflavor_es
=====================

Country-specific Django helpers for Spain.

What's in the Spain localflavor?
================================

* forms.ESIdentityCardNumberField: A form field that validates input as a
  Spanish NIF/NIE/CIF (Fiscal Identification Number) code.

* forms.ESCCCField: A form field that validates input as a Spanish bank account
  number (Codigo Cuenta Cliente or CCC). A valid CCC number has the format
  EEEE-OOOO-CC-AAAAAAAAAA, where the E, O, C and A digits denote the entity,
  office, checksum and account, respectively. The first checksum digit
  validates the entity and office. The second checksum digit validates the
  account. It is also valid to use a space as a delimiter, or to use no
  delimiter.

* forms.ESPhoneNumberField: A form field that validates input as a Spanish
  phone number. Valid numbers have nine digits, the first of which is 6, 8 or
  9.

* forms.ESPostalCodeField: A form field that validates input as a Spanish
  postal code. Valid codes have five digits, the first two being in the range
  01 to 52, representing the province.

* forms.ESProvinceSelect: A ``Select`` widget that uses a list of Spanish
  provinces as its choices.

* forms.ESRegionSelect: A ``Select`` widget that uses a list of Spanish regions
  as its choices.

See the source code for full details.

About localflavors
==================

Django's "localflavor" packages offer additional functionality for particular
countries or cultures.

For example, these might include form fields for your country's postal codes,
phone number formats or government ID numbers.

This code used to live in Django proper -- in django.contrib.localflavor -- but
was separated into standalone packages in Django 1.5 to keep the framework's
core clean.

For a full list of available localflavors, see https://github.com/django/
