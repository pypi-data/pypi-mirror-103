#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#    MusaMusa-TextRef Copyright (C) 2021 suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of MusaMusa-TextRef.
#    MusaMusa-TextRef is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MusaMusa-TextRef is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with MusaMusa-TextRef.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
   MusaMusa-TextRef project : musamusa_textref/textrefoeverses.py

   Text Reference for Old English Verses: TextRefOEVerses

   Unit testing: see tests/textrefoeverses.py

   ____________________________________________________________________________

   class:

   o TextRefOEVerses class
"""
# TextRefOEVerses DOES have public methods, inherited from TextRefBaseClass.
# pylint: disable=too-few-public-methods

import re
from musamusa_textref.textrefbaseclass import TextRefBaseClass
from musamusa_textref.subref import SubRef


class TextRefOEVerses(TextRefBaseClass):
    """
        TextRefOEVerses class
    """
    _refs_separator = ";"
    _ref2ref_separator = "-"
    _refsubpart_separator = "."

    _subrefs = {
              "a-z(1)": SubRef(re.compile(r"^[a-z]$"),
                               1,
                               2,
                               {"a": 1, "b": 2, }),
              "int": SubRef(re.compile(r"^\d+$"),
                            1, 9999, {}),
              "int+a-z(1)": SubRef(re.compile(r"^(?P<subref0>\d+)(?P<subref1>[a-z])$"),
                                   None, None, {}),
              }

    def _init_from_str__extract_def_from_src_mono(self,
                                                  src):
        """
            TextRefOEVerses._init_from_str__extract_def_from_src_mono()

            Apply several regexes to parse <src> and transform it into
            a list of (typevalue, value) like ('int', 43) or ('roman numbers', 12)
            ___________________________________________________________________

            ARGUMENT:
            o  (str)src: source string to be read

            RETURNED VALUE: (list)res
        """
        res = []
        # (pimydoc)TextRefBaseClass._subrefs structure
        # ⋅
        # ⋅ Beware ! If you modify _subrefs content, please rewrite
        # ⋅     o  _init_from_str__extract_def_from_src_mono()
        # ⋅     o  _monoref_definition2str()
        # ⋅ in the derived class.
        # ⋅
        # ⋅ TextRefBaseClass._subref is a tuple made of:
        # ⋅
        # ⋅     *  .regex     : (bytes)a compiled regex
        # ⋅     *  .min_value : None or (integer) minimal value
        # ⋅     *  .max_value : None or (integer) maximal value
        # ⋅     *  .char2int  : None or (a dict)  character to integer value
        # ⋅     *  .int2char  : inverse of .char2int, automatically generated
        # ⋅
        # ⋅     By example:
        # ⋅     * re.compile(r"^[a-z]$"),
        # ⋅     * 1,
        # ⋅     * 26,
        # ⋅     * {"a": 1,
        # ⋅        "b": 2,
        # ⋅        ...
        # ⋅        "z": 26}
        for _subpart in src.split(self._refsubpart_separator):
            subpart = _subpart.strip()
            if subpart:
                # ---- int ----------------------------------------------------
                _subrefs_res = re.search(self._subrefs["int"].regex,
                                         subpart)
                if _subrefs_res:
                    res.append(
                        ("int",
                         int(subpart)))
                    continue

                # ---- int+a-z(1) ---------------------------------------------
                _subrefs_res = re.search(self._subrefs["int+a-z(1)"].regex,
                                         subpart)
                if _subrefs_res:
                    res.append(
                        ("int",
                         int(_subrefs_res.group("subref0"))))
                    res.append(
                        ("a-z(1)",
                         self._subrefs["a-z(1)"].char2int[_subrefs_res.group("subref1")]))
                    continue

                # ---- a-z(1) -------------------------------------------------
                _subrefs_res = re.search(self._subrefs["a-z(1)"].regex,
                                         subpart)
                if _subrefs_res:
                    res.append(
                        ("a-z(1)",
                         self._subrefs["a-z(1)"].char2int[subpart]))
                    continue

                res.append(
                    (None,
                     subpart))

        return res
