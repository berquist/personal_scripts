#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

##    This library is free software; you can redistribute it and/or
##    modify it under the terms of the GNU Lesser General Public
##    License as published by the Free Software Foundation; either
##    version 2.1 of the License, or (at your option) any later version.
##
##    This library is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
##    Lesser General Public License for more details.=
##
##    You should have received a copy of the GNU Lesser General Public
##    License along with this library; if not, write to the Free Software
##    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
##

"""Extracts an object from any pickled file and produces a text file.

This is a command-line tool for making sense of an otherwise abandoned Python
pickle file.

Target formats:
    DataTree
    JSON
    Python
    S-expressions (SXML)
    Plain text
    XML
    YAML

It's OK to specify more than one format. If no input files are given, the
script searches the current directory. If no options are given, the usage guide
is printed.

Authors: Eric Talevich & contributors (see code for credits)
License: GPL (http://www.gnu.org/copyleft/gpl.html)

"""


USAGE = """pickle2txt Usage
Command-line syntax:
    pickle2txt [--xml | --json | --datatree | --txt] inpath outpath
    pickle2txt [-h | --help]
"""

# TODO:
# It would be helpful to have a couple functions to navigate the object
# - One to flatten the tree/ return pairs
# - Another to navigate while keeping the structure (apply a mapping)
#
# Support the formats I claimed
#
# ENH: for formats that already have projects devoted to them, check to see if
# the popular (faster) modules are available (e.g. simplejson).
# If so, use them; if not, use this code.

import os
import os.path
import pickle
import sys

from pprint import pprint


ENCODING = "utf-8"

PRIMITIVES = (complex, float, int, str, bool, type(None), tuple, list)

def echo(msg):
    """Print a message to standard error."""
    sys.stderr.write("pickle2txt: %s\n" % msg)


class WriteError(Exception):
    """Our generic exception."""
    pass



# -----------------------------------------------------------------------------

class Format(object):
    """Base class for those that output specific formats."""

    def __init__(self):
        pass

    def write(self, obj):
        """Override this in the derived class."""
        pass


# -----------------------------------------------------------------------------
# DataTree

class Format_datatree(Format):
    """Ivan Vecerina's data storage format, similar to JSON.

    Quirks:
     - Arrays are written with commas at the start of the next line, rather than
        at the end of the line containing the statement.
     - The last comma in an array or dictionary listing is not necessary, but
        will not muck up this reader implementation. Will it muck up the C++
        and C implementations?
    """
    # ENH: Consider using repr() and replacement tricks as a shortcut

    def __init__(self):
        """Creates an instance at the top level."""
        Format.__init__(self)
        self.depth_ = 0

    def write(self, obj):
        """Serialize the given object and return as a string."""
        dstlist = ["# DataTree text file" + 2*os.linesep]
        dstlist.extend(self.set_value(obj.__dict__))
        dstlist.append("%s# EOF%s" % (2*os.linesep, os.linesep))
        return ''.join(dstlist)

    def set_value(self, val):
        """Calls the appropriate function to serialize the given value.

        Recurses with set_dict or set_array if the value is a dictionary or
        sequence.
        """
        valtype = type(val)
        if valtype in (type, dict):
            if valtype is type:
                val = val.__dict__
            self.depth_ += 1
            lines = self.set_dict(val)
        elif valtype in (list, tuple):
            self.depth_ += 1
            lines = self.set_array(val)
        else:
            lines = [self.serialize(val)]
        return lines


    def set_dict(self, dct):
        """Converts a dictionary to a list for eventual serialization."""
        lines = ['{' + os.linesep]
        for key in dct:
            lines.extend([key, ' : '] + self.set_value(dct[key]))
        lines.append('}'+ os.linesep)
        return lines


    def set_array(self, arr):
        """Prepares a sequence for serialization by inserting delimiters."""
        # TODO: Arrays should be all on one line
        lines = ["("]
        for val in arr:
            lines.extend(self.set_value(val))
            lines.append(', ') # Avoid double commas
        lines.append(")" + os.linesep)
        return lines


    def serialize(self, val):
        """Converts to a string when value isn't a dict or sequence."""
        #TODO: indentation. Prepend a "\t"*depth to each new line.
        if isinstance(val, type(NoneType)):
            val = "00"
        elif isinstance(val, bool):
            val = val and "1" or "0"
        elif isinstance(val, str) and ' ' in val:
            val = "'%s'" % val
        elif type(val) in (int, float, complex):
            val = str(val)
        else:
            try:
                val = repr(val)
            except:
                raise WriteError("Element '%s' cannot be serialized"
                                    % val.__name__)
        return val + os.linesep


# -----------------------------------------------------------------------------
# JSON

# Using minjson.py from the json-py project
# Copyright Jim Washington and Patrick D. Logan (LGPL license)
# http://sourceforge.net/projects/json-py/

##############################################################################
##
##    minjson.py implements JSON reading and writing in python.
##    Copyright (c) 2005 Jim Washington and Contributors.
##
##############################################################################

class Format_json(Format):
    """JavaScript Object Notation"""

    from re import compile, sub, search, DOTALL

    tfnTuple = (('True','true'), ('False','false'), ('None','null'),)

    # re for a double-quoted string that has a single-quote in it
    # but no double-quotes and python punctuation after:
    redoublequotedstring = compile(r'"[^"]*\'[^"]*"[,\]\}:\)]')
    escapedSingleQuote = r"\'"
    escapedDoubleQuote = r'\"'

    def __init__(self):
        Format.__init__(self)

    def write(self, obj):
        """Represent the object as a string.

        Do any necessary fix-ups with pyexpr2jsexpr.
        """
        try:
            #not really sure encode does anything here
            a_string = str(obj).encode(ENCODING)
        except UnicodeEncodeError:
            a_string = obj.encode(ENCODING)
        if isinstance(obj, str):
            if '"' in a_string:
                a_string = a_string.replace(self.escapedDoubleQuote, '"')
                result = '"%s"' % a_string.replace('"', self.escapedDoubleQuote)
            else:
                result = '"%s"' % a_string
        else:
            result = self.serialize(a_string).encode(ENCODING)
        return result

    def serialize(self, a_string):
        """Use python's formatting of string representations of objects.

        Python always uses "'" to delimit strings.  Except it doesn't when
        there is ' in the string.  Fix that, then, if we split on that
        delimiter, we have a list that alternates non-string text with string
        text.  Since string text is already properly escaped, we only need to
        replace True, False, and None in non-string text and remove any unicode
        'u's preceding string values.
        """
        # inSingleQuote = False
        # inDoubleQuote = False
        #python will quote with " when there is a ' in the string,
        #so fix that first
        if self.redoublequotedstring.search(a_string):
            a_string = self.swap_quotes(a_string)
        marker = None
        if self.escapedSingleQuote in a_string:
            #replace escaped single quotes with a marker
            marker = marker_base = '|'
            marker_count = 1
            while marker in a_string:
                #if the marker is already there, make it different
                marker_count += 1
                marker = marker_base * marker_count
            a_string = a_string.replace(self.escapedSingleQuote, marker)

        #escape double-quotes
        a_string = a_string.replace('"', self.escapedDoubleQuote)
        #split the string on the real single-quotes
        outlist = []
        alt = True
        for substr in a_string.split("'"):
            #if alt is True, non-string; do replacements
            if alt:
                substr = self.jsonify(substr)
            outlist.append(substr)
            alt = not alt
        result = '"'.join(outlist)
        if marker:
            #put the escaped single-quotes back as "'"
            result = result.replace(marker,"'")
        return result

    def swap_quotes(self, a_string):
        """Rewrite double-quoted strings with single quotes as single-quoted
        strings with escaped single quotes."""
        s = []
        foundlocs = self.redoublequotedstring.finditer(a_string)
        prevend = 0
        for loc in foundlocs:
            start, end = loc.span()
            s.append(a_string[prevend:start])
            tempstr = a_string[start:end]
            endchar = tempstr[-1]
            ts1 = tempstr[1:-2]
            ts1 = ts1.replace("'", self.escapedSingleQuote)
            ts1 = "'%s'%s" % (ts1, endchar)
            s.append(ts1)
            prevend = end
        s.append(a_string[prevend:])
        return ''.join(s)

    def replace_bool_none(self, a_string):
        """Replace True, False, and None with javascript counterparts"""
        for k in self.tfnTuple:
            if k[0] in a_string:
                a_string = a_string.replace(k[0], k[1])
        return a_string

    def jsonify(self, substr):
        """Replace True, False, and None with javascript counterparts if
        appropriate, remove unicode u's, fix long L's, make tuples lists, and
        strip white space if requested
        """
        if 'e' in substr:
            #True, False, and None have 'e' in them. :)
            substr = (self.replace_bool_none(substr))
        if substr[-1] in "uU":
            #remove unicode u's
            substr = substr[:-1]
        if "L" in substr:
            #remove Ls from long ints
            substr = substr.replace("L",'')
        #do tuples as lists
        if "(" in substr:
            substr = substr.replace("(",'[')
        if ")" in substr:
            substr = substr.replace(")",']')
        return substr


# -----------------------------------------------------------------------------
# Python code

class Format_py(Format):
    """Python code representation via the pprint module."""

    def __init__(self):
        Format.__init__(self)

    def write(self, obj):
        """Serialize."""
        from io import StringIO
        output = StringIO()
        pprint.pprint(obj, stream=output, indent=4)
        contents = output.getvalue()
        output.close()
        return contents


# -----------------------------------------------------------------------------
# S-Expressions (Lisp/SXML)

class Format_lisp(Format):
    """S-expressions, a.k.a. Lisp code. Specifically, SXML."""

    def dict2sexp(self, dct, root='Root', indent='\t'):
        """Convert a dictionary to an SXML-style sexpr.

        Rules:
            int, float -> as-is
            string -> "string"
            dict -> (key value)
            tuple, list -> repeat tag for each value
            bool -> int(bool)
            None, empty string -> empty node
            other object -> str(obj)

        """
        # from xml.sax.saxutils import escape

        def tagset(key, val, level):
            """Place a label and value in an s-expression."""
            if val in (None, ""):
                return "%s(%s \"\")\n" % (indent*level, key)

            if type(val) in (list, tuple):
                return "".join(tagset(key, v, level) for v in val)

            if type(val) is bool:
                val = int(val)

            return "%s(%s %s)\n" % (indent*level, key,
                                    format_value(key, val, level))

        def format_value(key, val, level):
            """Recurse with tagset to serialize a node."""
            if type(val) in (float, int):
                pass

            elif type(val) is dict:
                lines = [tagset(k, v, level+1) for k, v in val.items()]
                lines.sort()  # NB: Py dicts are unordered
                val = "\n%s%s" % (''.join(lines), indent*level)

            else:
                val = '"%s"' % val

            return val

        return tagset(root, dct, 0)

    def write(self, obj):
        """Serialize."""
        return '(*TOP* (*PI* xml "version=\"1.0\" encoding=\"UTF-8\"")\n' + \
                self.dict2sexp(obj.__dict__, root=__name__) + ')\n'


# -----------------------------------------------------------------------------
# Plain text

class Format_text(Format):
    """ Prints all attributes as simple "Attribute: Value" pairs """

    def __init__(self):
        Format.__init__(self)

    def flatten(self, node, indent=0):
        """Generate key-val pairs from a dictionary.

        If val is not a primitive, wing it.
        """
        #if '__dict__' in node:
            #node = node.__dict__
        #if 'iteritems' in node:
            #for key, val in node.items():
                #if type(val) in PRIMITIVES:
                    #yield (indent, key, str(val))
                #else:
                    #yield (indent, key, str(type(val)))
                    #self.flatten(val, indent+1)
        #else:
        yield (indent, repr(node))

    def write(self, obj):
        """Serialize."""
        return '\n'.join("%s%s\n" % (i*'  ', k)
                         for i, k in self.flatten(obj))


# -----------------------------------------------------------------------------
# XML

class Format_xml(Format):
    """Standard XML 1.0 using Python builtins."""

    def __init__(self):
        Format.__init__(self)

    def dict2xml(self, dct, root='Root', indent='\t'):
        """Convert a dictionary to an XML string.

        Rules:
            string -> escape(string)
            int, float -> as-is
            dict -> <key>value</key>
            tuple, list -> repeat tag for each value
            bool -> int(bool)
            None, empty string -> empty node
            other object -> escape(str(obj))

        """
        # from xml.sax.saxutils import escape

        def tagset(key, val, level):
            if val in (None, ""):
                return "%s<%s />\n" % (indent*level, key)

            if type(val) in (list, tuple):
                return "".join(tagset(key, v, level) for v in val)

            if type(val) is bool:
                val = int(val)

            return "%s<%s>%s</%s>\n" % (indent*level, key,
                                        format_value(key, val, level), key)

        def format_value(key, val, level):
            if type(val) in (float, int, str):
                pass

            elif type(val) is dict:
                lines = [tagset(k, v, level+1) for k, v in val.items()]
                lines.sort()  # NB: Py dicts are unordered
                val = "\n%s%s" % (''.join(lines), indent*level)

            elif type(val) is not str:
                val = str(val)

            return val

        return tagset(root, dct, 0)

    def write(self, obj):
        """Serialize."""
        return '<?xml version="1.0" encoding="UTF-8">\n' + \
                self.dict2xml(obj.__dict__, root=__name__)


# -----------------------------------------------------------------------------
# YAML

class Format_yaml(Format):
    """Yet Another Markup Language."""
    # TODO: Look for a spec or existing code

    def write(self, obj):
        """Serialize."""
        pass



# -----------------------------------------------------------------------------
# This is where the action happens

def test(obj):
    """Clunky test: Convert a sample pickle to every format."""
    path = 'example.pickle'
    for format in ("datatree", "json", "py", "text", "xml", "yaml"):
        if eval("options.to_" + format):
            outfile = open("%s.%s" % (path, format), 'w')
            outfile.write(to_format(obj, format, path))
            outfile.close()


def process_args(options, filepaths):
    """Command-line processing."""
    if not filepaths:
        echo("Warning: no input files given or found.")
        return

    for format in ("datatree", "json", "py", "text", "xml", "yaml"):
        if getattr(options, format):
          fmat = globals()["Format_{}".format(format)]()
          for path in filepaths:
              try:
                  infile = open(path, 'rb')
                  outfile = open("%s.%s" % (path, format), 'w')
                  while True:
                    obj = pickle.load(infile)
                    outfile.write(fmat.write(obj))
              except (IOError, pickle.UnpicklingError) as why:
                  echo("Couldn't load file: %s" % why)
              except EOFError:
                outfile.close()
                infile.close()



if __name__ == "__main__":
    from optparse import OptionParser

    OP = OptionParser(USAGE)
    OP.add_option("-d", "--datatree", dest="datatree",
                        action="store_true",
                        help="Output in Ivan Vecerina's DataTree format")
    OP.add_option("-j", "--json", dest="json",
                        action="store_true",
                        help="Output in JSON format")
    OP.add_option("-p", "--py", dest="py",
                        action="store_true",
                        help="Output as a formatted Python code representation")
    OP.add_option("-t", "--text", dest="text",
                        action="store_true",
                        help="Output as plain, unformatted text")
    OP.add_option("-x", "--xml", dest="xml",
                        action="store_true",
                        help="Output in XML 1.0 format")
    OP.add_option("-y", "--yaml", dest="yaml",
                        action="store_true",
                        help="Output in YAML format")

    process_args(*OP.parse_args())

