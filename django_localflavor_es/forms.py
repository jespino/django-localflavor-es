# -*- coding: utf-8 -*-
"""
Spanish-specific Form helpers
"""

from __future__ import absolute_import, unicode_literals

from django.contrib.localflavor.es.es_provinces import PROVINCE_CHOICES
from django.contrib.localflavor.es.es_regions import REGION_CHOICES
from django.forms.fields import CharField, Select

from .validators import (ESPostalCodeValidator, ESPhoneNumberValidator,
                         ESIdentityCardNumberValidator, ESCCCValidator)


class ESPostalCodeField(CharField):
    """
    A form field that validates its input as a spanish postal code.

    Spanish postal code is a five digits string, with two first digits
    between 01 and 52, assigned to provinces code.
    """
    default_validators = [ESPostalCodeValidator()]


class ESPhoneNumberField(CharField):
    """
    A form field that validates its input as a Spanish phone number.
    Information numbers are ommited.

    Spanish phone numbers are nine digit numbers, where first digit is 6 (for
    cell phones), 8 (for special phones), or 9 (for landlines and special
    phones)

    TODO: accept and strip characters like dot, hyphen... in phone number
    """
    default_validators = [ESPhoneNumberValidator()]


class ESIdentityCardNumberField(CharField):
    """
    Spanish NIF/NIE/CIF (Fiscal Identification Number) code.

    Validates three diferent formats:

        NIF (individuals): 12345678A
        CIF (companies): A12345678
        NIE (foreigners): X12345678A

    according to a couple of simple checksum algorithms.

    Value can include a space or hyphen separator between number and letters.
    Number length is not checked for NIF (or NIE), old values start with a 1,
    and future values can contain digits greater than 8. The CIF control digit
    can be a number or a letter depending on company type. Algorithm is not
    public, and different authors have different opinions on which ones allows
    letters, so both validations are assumed true for all types.
    """
    default_validators = [ESIdentityCardNumberValidator()]


class ESCCCField(CharField):
    """
    A form field that validates its input as a Spanish bank account or CCC
    (Codigo Cuenta Cliente).

        Spanish CCC is in format EEEE-OOOO-CC-AAAAAAAAAA where:

            E = entity
            O = office
            C = checksum
            A = account

        It's also valid to use a space as delimiter, or to use no delimiter.

        First checksum digit validates entity and office, and last one
        validates account. Validation is done multiplying every digit of 10
        digit value (with leading 0 if necessary) by number in its position in
        string 1, 2, 4, 8, 5, 10, 9, 7, 3, 6. Sum resulting numbers and extract
        it from 11.  Result is checksum except when 10 then is 1, or when 11
        then is 0.

        TODO: allow IBAN validation too
    """
    default_validators = [ESCCCValidator()]


class ESRegionSelect(Select):
    """
    A Select widget that uses a list of spanish regions as its choices.
    """
    def __init__(self, attrs=None):
        super(ESRegionSelect, self).__init__(attrs, choices=REGION_CHOICES)


class ESProvinceSelect(Select):
    """
    A Select widget that uses a list of spanish provinces as its choices.
    """
    def __init__(self, attrs=None):
        super(ESProvinceSelect, self).__init__(attrs, choices=PROVINCE_CHOICES)
