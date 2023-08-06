# standard imports
import logging

# external imports
from packaging import version

# local imports
from .error import (
        ExistsError,
        VersionError,
        )

logg = logging.getLogger().getChild(__name__)


class VersionAuditer:

    def __init__(self):
        self.versions = {}


    def add(self, k, s, fail_on_exist=False):
        if fail_on_exist:
            return self.update(k, s, on_exist='fail')
        else:
            return self.update(k, s, on_exist='skip')


    def update_if_lesser(self, k, s):
        pass


    def update_if_greater(self, k, s):
        pass


    def update(self, k, s, on_exist='overwrite'):
        k = k.lower()
        v = version.parse(s)
        if self.versions.get(k):
            if on_exist == 'fail':
                raise ExistsError('already exists')
            if on_exist == 'skip':
                logg.debug('skip {} => {} (skip existing)'.format(k, v))
                return False
            logg.debug('update {} => {}'.format(k, v))
        elif on_exist == 'update_if_exist':
            logg.debug('skip {} => {} (skip if not existing)'.format(k, v))
            return False
        else:
            logg.debug('add {} => {}'.format(k, v))
        self.versions[k] = str(v)
        return True


    def check(self, k, v, mod, fail_on_missing=False):
        #shouldhave = versions[modulename]
        shouldhave = self.versions.get(k)
        if shouldhave == None:
            if fail_on_missing:
                raise KeyError('master missing {}'.format(k))
            return True
        #have = version.parse(match[3])
        have = version.parse(v)

        logg.debug('check {} {} {}'.format(k, mod, v)) #l, match[1], match[2], match[3]))

        fault = None
        
        if mod == '~=':
            logg.debug('checking COMPATIBLE match for {} => {}'.format(k, v))
            if shouldhave.major > 0 and have.major < shouldhave.major:
                fault = 'COMPATIBLE WiTH'
            elif shouldhave.major == 0 and have.minor < shouldhave.minor:
                fault = 'COMPATIBLE WiTH'
            elif shouldhave.major == 0 and shouldhave.minor == 0:
                if have.is_prerelease and have < shouldhave:
                    fault = 'COMPATIBLE WITH'
                elif have.micro < shouldhave.micro:
                    fault = 'COMPATIBLE WiTH'

        elif mod == '==':
            logg.debug('checking EXACT match for {} => {}'.format(k, v))
            if not shouldhave == have:
                fault = 'EXACT MATCH OF'

        elif mod == '>':
            logg.debug('checking GREATED THAN match for {} => {}'.format(k, v))
            if not shouldhave < have:
                fault = 'GREATER THAN'

        elif mod == '>=':
            logg.debug('checking GREATED THAN OR EQUAL match for {} => {}'.format(k, v))
            if not shouldhave <= have:
                fault = 'GREATER OR EQUAL THAN'

        elif mod == '<':
            logg.debug('checking LESSER THAN match for {} => {}'.format(k, v))
            if not shouldhave < have:
                fault = 'LESSER THAN'

        elif mod == '<=':
            logg.debug('checking LESSER THAN OR EQUAL match for {} => {}'.format(k, v))
            if not shouldhave <= have:
                fault = 'LESSER OR EQUAL THAN'
        else:
            raise ValueError('caught comparison modifier {}, dunno what that is'.format(mod))

        if fault != None:
            raise VersionError('{}: {} not {} {}'.format(k, have, fault, shouldhave))


    def all(self):
        return list(self.versions.values())


    def __str__(self):
        s = ''
        for r in self.all():
            s += str(r) + '\n'
        return s
