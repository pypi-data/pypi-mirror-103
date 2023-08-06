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
   MusaMusa-TextRef project : musamusa_textref/semisortedtextrefsdict.py

   Use SemiSortedTextRefsDict to store (textref, data) where textref is
   a TextRef* like object.

   "semi sorted" means that the internal storage (.textref2data) isn't sorted
   but that you may iterate over a SemiSortedTextRefsDict and get sorted output
   thanks to the .sorted_textrefs attribute.
   ____________________________________________________________________________

   o  SemiSortedTextRefsDict class
"""
from musamusa_errors.error_messages import ListOfErrorMessages, MusaMusaError
from musamusa_textref.textrefdefault import TextRefDefault


class SemiSortedTextRefsDict:
    """
        SemiSortedTextRefsDict class

        ATTRIBUTES:
        o  (ListOfErrorMessages) .errors
        o  (dict: textref>data)  .textref2data
        o  (TextRef* object)     .sorted_textrefs

        METHODS:
        o  __init__(self, textrefclass=TextRefDefault)
        o  add(self, textref, data)
        o  improved_str(self)
    """
    def __init__(self,
                 textrefclass=TextRefDefault):
        """
            SemiSortedTextRefsDict.__init__()
            ___________________________________________________________________

            ARGUMENT:
            o  (type)textrefclass: TextRef* type to be used.
        """
        self.errors = ListOfErrorMessages()
        self.textref2data = dict()
        self.sorted_textrefs = textrefclass(force_validity=True)

    def add(self,
            textref,
            data):
        """
            SemiSortedTextRefsDict.add()

            Add a pair of (textref: data) to self.

            NO ERROR IS ADDED to .errors if textref is already (partially or not)
            in <self>.
            ___________________________________________________________________

            ARGUMENTS:
            o  (TextRef*) textref used as a key.
            o  (any type) data used as a value.

            RETURNED VALUE: (bool)success
        """
        if not self.errors.zero_error_or_warning():
            # (pimydoc)error::TEXTREF-ERRORID002
            # ⋅ You can't use SemiSortedTextRefsDict.add() with SemiSortedTextRefsDict object
            # ⋅ that already contains an error.
            error = MusaMusaError()
            error.msgid = "TEXTREF-ERRORID002"
            error.msg = f"[{error.msgid}] " \
                "You can't add anything to a SemiSortedTextRefsDict that already " \
                f"contains an error; current errors are {self.errors}"
            self.errors.append(error)
            return False

        if not textref.errors.zero_error_or_warning():
            # (pimydoc)error::TEXTREF-ERRORID003
            # ⋅ You can't add a TextRef* object to a SemiSortedTextRefsDict
            # ⋅ if the TextRef* already contains an error.
            error = MusaMusaError()
            error.msgid = "TEXTREF-ERRORID003"
            error.msg = f"[{error.msgid}] " \
                "You can't add a TextRef* object to a SemiSortedTextRefsDict " \
                "if the TextRef* contains an error; " \
                f"errors in the TextRef* object are {textref.errors}"
            self.errors.append(error)
            return False

        if not self.sorted_textrefs.add_and_sort(textref2=textref,
                                                 keep_iter_infos=True):
            return False

        self.textref2data[textref] = data

        return True

    def improved_str(self):
        """
            SemiSortedTextRefsDict.improved_str()
            ___________________________________________________________________

            RETURNED VALUE: (str) a string describing the object.
        """
        res = []

        if self.errors:
            res.append("ERROR/WARNINGS:")
            for error in self.errors:
                res.append("* "+str(error.improved_str()))

        res.append(
            f"textrefs={self.sorted_textrefs.definition2str()} "
            f"(reduced={self.sorted_textrefs.definition2str(reduced=True, keep_iter_infos=False)})")

        for textref in self.sorted_textrefs:
            res.append(f"*  {textref.definition2str()} : {self.textref2data[textref]}")
        return "\n".join(res)
