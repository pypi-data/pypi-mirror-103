"""mmm yes, docstring..."""

import re
import io
from .lib import binlol

__version__ = "2.1.0"


class ParsingError(Exception):
    """base exception for parsing error"""

    def __init__(self, message, text, line):
        self.message = message
        self.text = text
        self.line = line
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}, {self.text} [line {self.line}]"


class ParseDuplicateError(ParsingError):
    """dupe error raised while parsing"""


class PropertyError(Exception):
    pass


class DuplicateError(Exception):
    pass


class SectionError(Exception):
    pass


class ParsePropertyError(ParsingError):
    """raised when failed parsing property"""


class ParseSectionError(ParsingError):
    """raised when failed parsing section"""


class INI(object):
    """main class for parsing ini"""

    def __init__(self, delimiter=("=",), convert_property=False):
        self.ini = dict()
        self.delimiter = delimiter
        self.convert_property = convert_property
        self._sections = list()

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        return self

    def __str__(self):
        return f"{self.ini}"

    def __getitem__(self, key):
        return self.ini[key]

    def read(self, string):
        self.ini = parse(string, self.delimiter, self.convert_property)
        self._sections = []
        for prop in self.ini:
            if isinstance(self.ini[prop], dict):
                self._sections.append(prop)

    def sections(self):
        return self._sections

    def has_section(self, name):
        return name in self._sections

    def has_property(self, name, section=None):
        if section is None:
            return name in self.ini

        return name in self.ini[section]

    def read_file(self, filename):
        """read sections and properties"""
        self.ini = parse(
            open(filename, "r").read(), self.delimiter, self.convert_property
        )
        self._sections = []
        for prop in self.ini:
            if isinstance(self.ini[prop], dict):
                self._sections.append(prop)

    def read_binfile(self, filename):
        bin_data = binlol.load(filename)
        self.ini = parse(
            binlol.parse_bin_tree(bin_data), self.delimiter, self.convert_property
        )
        self._sections = []
        for prop in self.ini:
            if isinstance(self.ini[prop], dict):
                self._sections.append(prop)

    def remove_section(self, name):
        if not self.has_section(name):
            raise SectionError("section %s not found" % name)

        del self.ini[name]
        self._sections.remove(name)

    def remove_property(self, name, section=None):
        if section is None:
            if not self.has_property(name):
                raise PropertyError("property %s not found" % name)

            del self.ini[name]
            return None

        if not self.has_section(section):
            raise SectionError("section %s not found" % section)
        if not self.has_property(name, section):
            raise PropertyError(f"property {name} not found in section {section}")

        del self.ini[section][name]

    def set(self, name, value="", section=None):
        if section is None:
            self.ini.update({name: value})
            return None

        if not self.has_section(section):
            raise SectionError("section %s not found" % section)

        self.ini[section].update({name: value})

    def get(self, name, section=None):
        if section is None:
            if not self.has_property(name):
                raise PropertyError("property %s not found" % name)

            return self.ini[name]

        if not self.has_section(section):
            raise SectionError("section %s not found" % section)
        if not self.has_property(name, section):
            raise PropertyError(f"property {name} not found in section {section}")

        return self.ini[section][name]

    def set_section(self, name):
        if self.has_section(name):
            raise DuplicateError("section %s already exists" % name)

        self.ini.update({name: {}})
        self._sections.append(name)

    def write(self, filename):
        """write properties and sections to file"""
        dump(filename, self.ini)

    def write_bin(self, filename):
        """write properties and sections to file in binary format"""
        dump_bin(filename, self.ini)

    def write_string_bin(self, filename, string):
        """write properties and sections to file in binary format from string"""
        res = parse(string, self.delimiter, self.convert_property)
        dump_bin(filename, res)


def _parse(string):
    """parse ini format string returns parse tree"""
    lines = io.StringIO(string).readlines()
    parse_tree = []
    parse_tree.append([])

    parse_tree_point = 0

    for index, line in enumerate(lines):
        if is_section(line.strip()):
            parse_tree_point += 1
            parse_tree.append([])

        parse_tree[parse_tree_point].append((index + 1, line))

    return parse_tree


def parse(string, delimiter, convert_property):
    """parse "parse tree" returns ini dictionary"""
    result = {}

    parse_tree = _parse(string)

    prev_section = None
    prev_property = None
    prev_multiline_val = None

    for chunks in parse_tree:
        for line, chunk in chunks:
            if not chunk.strip() and prev_multiline_val is None:
                continue

            if is_section(chunk.strip()):
                prev_section = parse_section(chunk.strip())

                if prev_section in result:
                    raise ParseDuplicateError(
                        "section already exists", prev_section, line
                    )

                result.update({prev_section: {}})

            elif is_property(chunk.strip(), delimiter):
                key, val = parse_property(chunk.strip(), delimiter)

                prev_property = key

                if prev_section:
                    if prev_property in result[prev_section]:
                        raise ParseDuplicateError(
                            "property already exists", prev_property, line
                        )

                    result[prev_section].update({key: val})
                else:
                    if prev_property in result:
                        raise ParseDuplicateError(
                            "property already exists", prev_property, line
                        )

                    result.update({key: val})

            else:
                if re.match(r"^\s", chunk):
                    if prev_section:
                        if prev_property:
                            result[prev_section][prev_property] = result[prev_section][
                                prev_property
                            ] + ("\n" + chunk.strip())
                            continue
                    elif prev_section is None:
                        if prev_property:
                            result[prev_property] = result[prev_property] + (
                                "\n" + chunk.strip()
                            )
                            continue

                raise ParsePropertyError("error parsing property", chunk.strip(), line)

    if convert_property:
        return _convert_property(result)

    return result


def _convert_property(INI_dict):
    """converter"""
    eval_codes = [
        (r"^[-+]?(\d*[.])\d*$", float),
        (r"^[-+]?\d+$", int),
        (r"^\"(.*)\"$", eval),
    ]

    for sectf in INI_dict:
        if isinstance(INI_dict[sectf], dict):
            for prop in INI_dict[sectf]:
                for eval_code in eval_codes:
                    if type(INI_dict[sectf][prop]).__name__ != "str":
                        continue

                    if re.match(eval_code[0], INI_dict[sectf][prop]):
                        INI_dict[sectf][prop] = eval_code[1](INI_dict[sectf][prop])
                        break

                if type(INI_dict[sectf][prop]).__name__ != "str":
                    continue

                if INI_dict[sectf][prop].lower() == "true":
                    INI_dict[sectf][prop] = True
                elif INI_dict[sectf][prop].lower() == "false":
                    INI_dict[sectf][prop] = False
        else:
            for eval_code in eval_codes:
                if type(INI_dict[sectf]).__name__ != "str":
                    continue

                if re.match(eval_code[0], INI_dict[sectf]):
                    INI_dict[sectf] = eval_code[1](INI_dict[sectf])
                    break

            if type(INI_dict[sectf]).__name__ != "str":
                continue

            if INI_dict[sectf].lower() == "true":
                INI_dict[sectf] = True
            elif INI_dict[sectf].lower() == "false":
                INI_dict[sectf] = False

    return INI_dict


def dump(filename, ini_dict):
    """dump a dictionary or a set to INI file format"""
    with open(filename, "w+") as file:
        for sect in ini_dict:
            if isinstance(ini_dict[sect], dict):
                file.write(f"[{sect}]\n")
                for prop in ini_dict[sect]:
                    file.write(f"{prop} = {ini_dict[sect][prop]}\n")
            else:
                file.write(f"{sect} = {ini_dict[sect]}\n")


def dump_bin(filename, ini_dict):
    """dump a dictionary or a set to INI file format"""
    file = list()
    for sect in ini_dict:
        if isinstance(ini_dict[sect], dict):
            file.append(f"[{sect}]\n")
            for prop in ini_dict[sect]:
                file.append(f"{prop} = {ini_dict[sect][prop]}\n")
        else:
            file.append(f"{sect} = {ini_dict[sect]}\n")

    bin_file = binlol.parse_string("".join(file))
    binlol.dump(filename, bin_file, file_format="INI")


def parse_property(string, delimiter):
    """parse property returns property key and property value"""
    if check_comment(string):
        return None
    prop = re.findall(rf"^\s*(.+?)\s*[{r'|'.join(delimiter)}]\s*(.+?)\s*$", string)
    if not prop:
        return None
    if len(prop[0]) < 2:
        return None
    key, val = prop[0][0], prop[0][1]
    _key = re.match(r"^\s*(\#)|((.*)\s[#])", key)
    if _key:
        return None
    val = re.split(r"((.)^[#]$)|\s([#])", val)[0]

    return key, val


def parse_section(string):
    """parse section returns section name"""
    if check_comment(string):
        return None
    sec = re.findall(r"^\s*\[(.*)\]\s*?(.*)$", string)
    if not sec:
        return None
    if sec[0][1] and not re.match(r"^[#;]", sec[0][1].strip()):
        return None
    _sec = re.match(r"(.*)\s[#]", sec[0][0])
    if not _sec:
        return sec[0][0]


def check_comment(string):
    """check comment"""
    sec = re.match(r"^[#;]", string)
    if sec:
        return True
    return False


def is_property(string, delimiter):
    """check property"""
    if parse_property(string, delimiter) is not None:
        return True
    return False


def is_section(string):
    """check section"""
    if parse_section(string) is not None:
        return True
    return False


def is_ini(filename):
    """check file extension"""
    return filename.endswith(".ini")
