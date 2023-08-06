# -*- coding: utf-8 -*-

"""Main module of pylexique."""

from collections import OrderedDict
import pkg_resources
import json
from zipfile import ZipFile
import atexit
from dataclasses import dataclass
from typing import ClassVar

_RESOURCE_PACKAGE = __name__

PYLEXIQUE_DATABASE = '/'.join(('Lexique383', 'lexique383.xlsb'))
HOME_PATH = '/'.join(('Lexique', ''))

LEXIQUE383_FIELD_NAMES = ['ortho', 'phon', 'lemme', 'cgram', 'genre', 'nombre', 'freqlemfilms2', 'freqlemlivres',
                          'freqfilms2',
                          'freqlivres', 'infover', 'nbhomogr', 'nbhomoph', 'islem', 'nblettres', 'nbphons', 'cvcv',
                          'p_cvcv',
                          'voisorth', 'voisphon', 'puorth', 'puphon', 'syll', 'nbsyll', 'cv_cv', 'orthrenv', 'phonrenv',
                          'orthosyll', 'cgramortho', 'deflem', 'defobs', 'old20', 'pld20', 'morphoder', 'nbmorph']


LEXIQUE = OrderedDict()



class LexEntryTypes:
    """
    Hint type information.

    """
    ortho = str
    phon = str
    lemme = str
    cgram = str
    genre = str
    nombre = str
    freqlemfilms2 = float
    freqlemlivres = float
    freqfilms2 = float
    freqlivres = float
    infover = str
    nbhomogr = int
    nbhomoph = int
    islem = bool
    nblettres = int
    nbphons = int
    cvcv = str
    p_cvcv = str
    voisorth = int
    voisphon = int
    puorth = int
    puphon = int
    syll = str
    nbsyll = int
    cv_cv = str
    orthrenv = str
    phonrenv = str
    orthosyll = str
    cgramortho = str
    deflem = float
    defobs = int
    old20 = float
    pld20 = float
    morphoder = str
    nbmorph = int


class Lexique383:
    """
    This is the class handling the lexique database.
    It provides method for interacting with the Lexique DB
    and retrieve lexical items.
    All the lexical items are then stored in an Ordered Dict called

    :param lexique_path: string.
        Path to the lexique csv file.
    """

    file_name = pkg_resources.resource_filename(_RESOURCE_PACKAGE, PYLEXIQUE_DATABASE)

    def __init__(self, lexique_path=None):
        self.lexique_path = lexique_path
        self.lexique = OrderedDict()
        if lexique_path:
            print('parsing Lexique383')
            self.parse_lexique(self.lexique_path)
            # with ZipFile(pkg_resources.resource_stream(
            #         _RESOURCE_PACKAGE, PYLEXIQUE_DATABASE)) as content:
            #     with content.open('Lexique383.pickle', mode='w') as archive:
            #         joblib.dump(self.lexique , archive)
        else:
            # self.parse_lexique(self.lexique_path)
            # with ZipFile(pkg_resources.resource_stream(
            #         _RESOURCE_PACKAGE, PYLEXIQUE_DATABASE)) as content:
            #     with content.open('Lexique383.pickle', mode='r') as archive:
            #         joblib.load(archive)
            pass
        print('Lexique 383 loaded successfully')
        return

    def __repr__(self):
        return '{0}.{1}'.format(__name__, self.__class__.__name__)

    def __len__(self):
        return len(self.lexique)

    def parse_lexique(self, lexique_path):
        """
        | Parses the given lexique file and creates a hdf5 table to store the data.

        :param lexique_path: string.
            Path to the lexique csv file.
        :return: PyTables.Table
        """
        with open(lexique_path, 'r', encoding='utf-8', errors='ignore') as csv_file:
            content = csv_file.readlines()
            lexique383_db = (content[1:])
            self.create_db(lexique383_db)
        return

    def create_db(self, lexicon):
        """
        | Creates an hdf5 table populated with the entries in lexique if it does not exist yet.
        | It stores the hdf5 database for fast access.

        :param lexicon: Iterable.
            Iterable containing the lexique383 entries.
        :return: PyTables.Table
        """
        errors = {}
        for i, row in enumerate(lexicon):
            row_fields = row.strip().split('\t')
            formatted_row_fields = []
            for field, value in zip(LEXIQUE383_FIELD_NAMES, row_fields):
                if getattr(LexEntryTypes, field) == float:
                    value = value.replace(',', '.')
                try:
                    formatted_value = getattr(LexEntryTypes, field)(value)
                except ValueError:
                    errors[value] = field
                    formatted_value = value
                finally:
                    formatted_row_fields.append(formatted_value)
            if row_fields[0] in self.lexique and not isinstance(self.lexique[row_fields[0]], list):
                self.lexique[row_fields[0]]= [self.lexique[row_fields[0]]]
                self.lexique[row_fields[0]].append(formatted_row_fields)
            elif row_fields[0] in self.lexique and isinstance(self.lexique[row_fields[0]], list):
                self.lexique[row_fields[0]].append(LexItem(formatted_row_fields))
            else:
                self.lexique[row_fields[0]] = LexItem(formatted_row_fields)
        return


@dataclass(init=False, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False)
class LexItem:
    """
    | This class defines the lexical items in Lexique383.
    | It uses slots for memory efficiency.

    :param row_fields:
    """
    _s: ClassVar[list] = LEXIQUE383_FIELD_NAMES + ['_name_']
    __slots__ = _s
    _name_: str
    for attr in LEXIQUE383_FIELD_NAMES:
        attr: LexEntryTypes

    def __init__(self, row_fields):
        fields = row_fields
        setattr(self, '_name_', fields[0])
        for attr, value in zip(LEXIQUE383_FIELD_NAMES, fields):
            setattr(self, attr, value)
        return


if __name__ == "__main__":
    pass
