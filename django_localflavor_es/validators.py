# -*- coding: utf-8 -*-
"""
Spanish-specific Form helpers
"""

from __future__ import absolute_import, unicode_literals

import re

from django.core.validators import RegexValidator, EMPTY_VALUES
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class ESPostalCodeValidator(RegexValidator):
    """
    A validator for spanish postal code.

    Spanish postal code is a five digits string, with two first digits
    between 01 and 52, assigned to provinces code.
    """
    regex = r'^(0[1-9]|[1-4][0-9]|5[0-2])\d{3}$'
    message = _('Enter a valid postal code in the range and format 01XXX - 52XXX.')
    code = 'invalid'


class ESPhoneNumberValidator(RegexValidator):
    """
    A validator for Spanish phone number.
    Information numbers are ommited.

    Spanish phone numbers are nine digit numbers, where first digit is 6 (for
    cell phones), 8 (for special phones), or 9 (for landlines and special
    phones)

    TODO: accept and strip characters like dot, hyphen... in phone number
    """
    regex = r'^(6|7|8|9)\d{8}$'
    message = _('Enter a valid phone number in one of the formats 6XXXXXXXX, 8XXXXXXXX or 9XXXXXXXX.')
    code = 'invalid'


class ESIdentityCardNumberValidator(RegexValidator):
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
    default_error_messages = {
        'invalid': _('Please enter a valid NIF, NIE, or CIF.'),
        'invalid_only_nif': _('Please enter a valid NIF or NIE.'),
        'invalid_nif': _('Invalid checksum for NIF.'),
        'invalid_nie': _('Invalid checksum for NIE.'),
        'invalid_cif': _('Invalid checksum for CIF.'),
    }

    def __init__(self, only_nif=False, *args, **kwargs):
        self.only_nif = only_nif
        self.nif_control = 'TRWAGMYFPDXBNJZSQVHLCKE'
        self.cif_control = 'JABCDEFGHI'
        self.cif_types = 'ABCDEFGHKLMNPQS'
        self.nie_types = 'XT'
        self.regex = re.compile(r'^([%s]?)[ -]?(\d+)[ -]?([%s]?)$' % (self.cif_types + self.nie_types, self.nif_control + self.cif_control), re.IGNORECASE)
        self.message = self.default_error_messages['invalid%s' % (self.only_nif and '_only_nif' or '')]
        self.code = 'invalid%s' % (self.only_nif and '_only_nif' or '')

    def __call__(self, value):
        super(ESIdentityCardNumberValidator, self).__call__(value)

        if value in EMPTY_VALUES:
            return ''
        nif_get_checksum = lambda d: self.nif_control[int(d) % 23]

        value = value.upper().replace(' ', '').replace('-', '')
        m = re.match(r'^([%s]?)[ -]?(\d+)[ -]?([%s]?)$' % (self.cif_types + self.nie_types, self.nif_control + self.cif_control), value)
        letter1, number, letter2 = m.groups()

        if not letter1 and letter2:
            # NIF
            if letter2 == nif_get_checksum(number):
                return value
            else:
                raise ValidationError(self.error_messages['invalid_nif'], code="invalid_nif")
        elif letter1 in self.nie_types and letter2:
            # NIE
            if letter2 == nif_get_checksum(number):
                return value
            else:
                raise ValidationError(self.error_messages['invalid_nie'], code="invalid_nie")
        elif not self.only_nif and letter1 in self.cif_types and len(number) in [7, 8]:
            # CIF
            if not letter2:
                number, letter2 = number[:-1], int(number[-1])
            checksum = cif_get_checksum(number)
            if letter2 in (checksum, self.cif_control[checksum]):
                return value
            else:
                raise ValidationError(self.error_messages['invalid_cif'], code="invalid_cif")
        else:
            raise ValidationError(self.error_messages['invalid'], code="invalid")


class ESCCCValidator(RegexValidator):
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
    default_error_messages = {
        'invalid': _('Please enter a valid bank account number in format XXXX-XXXX-XX-XXXXXXXXXX.'),
        'checksum': _('Invalid checksum for bank account number.'),
    }
    regex = r'^\d{4}[ -]?\d{4}[ -]?\d{2}[ -]?\d{10}$'

    def __call__(self, value):
        super(ESCCCValidator, self).__call__(value)
        if value in EMPTY_VALUES:
            return ''
        control_str = [1, 2, 4, 8, 5, 10, 9, 7, 3, 6]
        m = re.match(r'^(\d{4})[ -]?(\d{4})[ -]?(\d{2})[ -]?(\d{10})$', value)
        entity, office, checksum, account = m.groups()
        get_checksum = lambda d: str(11 - sum([int(digit) * int(control) for digit, control in zip(d, control_str)]) % 11).replace('10', '1').replace('11', '0')
        if get_checksum('00' + entity + office) + get_checksum(account) == checksum:
            return value
        else:
            raise ValidationError(self.error_messages['checksum'])


def cif_get_checksum(number):
    s1 = sum([int(digit) for pos, digit in enumerate(number) if int(pos) % 2])
    s2 = sum([sum([int(unit) for unit in str(int(digit) * 2)]) for pos, digit in enumerate(number) if not int(pos) % 2])
    return (10 - ((s1 + s2) % 10)) % 10
