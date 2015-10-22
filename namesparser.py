import re
from collections import deque
from nameparser import HumanName


class HumanNames():
    def __init__(self, names_mess):
        self.names_mess = names_mess
        clean_names = HumanNames._clean(self.names_mess)
        norm_names = HumanNames._normalize(clean_names)
        name_tokens = HumanNames._tokenize(norm_names)
        name_list = HumanNames._name_list(name_tokens)
        self.name_strings = []
        self.human_names = []
        for name_tokens in name_list:
            name_str = " ".join([token.value for token in HumanNames._order_name(name_tokens)])
            self.name_strings.append(name_str)
            self.human_names.append(self.create_humanname(name_str))

    def create_humanname(self, name_str):
        """
        Override this to plug in your own HumanName.
        """
        return HumanName(name_str)

    def __repr__(self):
        return " and ".join(self.name_strings)

    @staticmethod
    def _clean(names_str):
        """
        Clean up some common errors in the name mess.
        """

        #Trim
        clean_names_str = names_str.strip()
        #Get rid of extra spaces
        clean_names_str = re.sub(" {2,}", " ", clean_names_str)
        #Remove *
        clean_names_str = clean_names_str.replace("*", "")
        #Fix missing space
        clean_names_str = clean_names_str.replace(".and", ". and")
        clean_names_str = re.sub(", ?", ", ", clean_names_str)
        return clean_names_str

    @staticmethod
    def _normalize(names_str):
        """
        Normalize some alternative forms of conjunctions.
        """
        norm_names_str = names_str
        #Replace " with " with " and "
        norm_names_str = norm_names_str.replace(" with ", " and ")
        #Replace " & " with " and "
        norm_names_str = norm_names_str.replace(" & ", " and ")
        norm_names_str = norm_names_str.replace(" &amp; ", " and ")
        #Replace ", and" with " and"
        norm_names_str = re.sub(", ?and ", " and ", norm_names_str)
        #Replace \n with " and"
        norm_names_str = re.sub(" *\n *", " and ", norm_names_str)
        return norm_names_str

    @staticmethod
    def _tokenize(names_str):
        """
        Split name mess into name tokens.
        """
        name_tokens = []
        split_names = re.split(" ?(and|,| ) ?", names_str)
        for s in split_names:
            if s == "and":
                name_tokens.append(Token("AND"))
            elif s == ",":
                name_tokens.append(Token("COMMA"))
            elif s == " ":
                pass
            elif HumanNames._is_initials(s):
                name_tokens.append(Token("INITIAL", s))
            else:
                name_tokens.append(Token("NAME", s))
        return name_tokens

    @staticmethod
    def _is_initials(part_str):
        """
        Returns True if initials.
        """
        for c in part_str:
            if c != "." and not c.isupper():
                return False
        return True

    @staticmethod
    def _section_list(tokens, token_type):
        """
        Groups into lists of tokens by splitting on a token type.
        """
        sections = deque()
        section = []
        for token in tokens:
            if token.type == token_type:
                sections.append(section)
                section = []
            else:
                section.append(token)
        if section:
            sections.append(section)
        return sections

    @staticmethod
    def _name_list(tokens):
        """
        Groups a list of name tokens into names.
        """
        name_sections = []
        and_sections = HumanNames._section_list(tokens, "AND")
        while and_sections:
            and_section = and_sections.popleft()
            comma_sections = HumanNames._section_list(and_section, "COMMA")
            while comma_sections:
                comma_section1 = comma_sections.popleft()
                if len(comma_sections) == 0:
                    name_sections.append(comma_section1)
                else:
                    comma_section2 = comma_sections.popleft()
                    if HumanNames._is_name(comma_section1) and HumanNames._is_name(comma_section2):
                        comma_sections.appendleft(comma_section2)
                    else:
                        comma_section1.append(Token("COMMA"))
                        comma_section1.extend(comma_section2)
                    name_sections.append(comma_section1)
        return name_sections

    @staticmethod
    def _is_name(tokens):
        """
        Returns True if provided tokens constitutes a complete name.

        A complete name has at least two name tokens or at least a name token
        and an initial token.
        """
        name_count = 0
        initial_count = 0
        for token in tokens:
            if token.type == "NAME":
                name_count += 1
            elif token.type == "INITIAL":
                initial_count += 1
        if name_count >= 2 or (name_count == 1 and initial_count >= 1):
            return True
        return False

    @staticmethod
    def _order_name(tokens):
        """
        Reorder name tokens into first last.
        """
        #Last, first
        comma_pos = 0
        for pos, token in enumerate(tokens):
            if token.type == "COMMA":
                comma_pos = pos
                break
        if comma_pos:
            new_tokens = tokens[comma_pos+1:]
            new_tokens.extend(tokens[:comma_pos])
            return new_tokens
        #Last initials
        new_tokens = deque(tokens)
        while new_tokens[-1].type == "INITIAL":
            token = new_tokens.pop()
            new_tokens.appendleft(token)
        return new_tokens


class Token():
    def __init__(self, token_type, value=None):
        self.type = token_type
        self.value = value

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        if self.value is not None:
            return "{} ({})".format(self.type, self.value)
        return self.type