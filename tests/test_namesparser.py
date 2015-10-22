from unittest import TestCase
from namesparser import HumanNames, Token as T

COMMA = T("COMMA")
AND = T("AND")


class TestHumanNames(TestCase):
    def test_clean(self):
        self.assertEqual("Harris Tweed", HumanNames._clean("Harris Tweed"))
        self.assertEqual("Harris Tweed", HumanNames._clean("Harris Tweed*"))
        self.assertEqual("Harris Tweed", HumanNames._clean(" Harris Tweed "))
        self.assertEqual("Harris Tweed", HumanNames._clean("Harris   Tweed"))
        self.assertEqual("Tweed H. and Garters P.", HumanNames._clean("Tweed H.and Garters P."))
        self.assertEqual("Tweed, Harris", HumanNames._clean("Tweed,Harris"))

    def test_normalize(self):
        self.assertEqual("Biffalo Buff and Weepy Weed", HumanNames._normalize("Biffalo Buff and Weepy Weed"))
        self.assertEqual("Biffalo Buff and Weepy Weed", HumanNames._normalize("Biffalo Buff, and Weepy Weed"))
        self.assertEqual("Biffalo Buff and Weepy Weed", HumanNames._normalize("Biffalo Buff,and Weepy Weed"))
        self.assertEqual("Biffalo Buff and Weepy Weed", HumanNames._normalize("Biffalo Buff\nWeepy Weed"))
        self.assertEqual("Biffalo Buff and Weepy Weed", HumanNames._normalize("Biffalo Buff \n Weepy Weed"))
        self.assertEqual("Biffalo Buff and Weepy Weed", HumanNames._normalize("Biffalo Buff & Weepy Weed"))
        self.assertEqual("Biffalo Buff and Weepy Weed", HumanNames._normalize("Biffalo Buff &amp; Weepy Weed"))
        self.assertEqual("Biffalo Buff and Weepy Weed", HumanNames._normalize("Biffalo Buff with Weepy Weed"))


    def test_is_initials(self):
        #Michael Carmichael Zutt
        self.assertTrue(HumanNames._is_initials("M"))
        self.assertTrue(HumanNames._is_initials("M."))
        self.assertTrue(HumanNames._is_initials("MC"))
        self.assertTrue(HumanNames._is_initials("M.C."))
        self.assertFalse(HumanNames._is_initials("Michael"))
        self.assertFalse(HumanNames._is_initials("m"))

    def test_tokenize(self):
        moon, face = T("NAME", "Moon"), T("NAME", "Face")
        m = T("INITIAL", "M")
        hoos_foos = T("NAME", "Hoos-Foos")
        self.assertEqual([moon, face], HumanNames._tokenize("Moon Face"))
        self.assertEqual([m, face], HumanNames._tokenize("M Face"))
        self.assertEqual([m, face, AND, hoos_foos],
                         HumanNames._tokenize("M Face and Hoos-Foos"))
        self.assertEqual([m, face, COMMA, hoos_foos],
                         HumanNames._tokenize("M Face, Hoos-Foos"))

    def test_section_list(self):
        moon, face = T("NAME", "Moon"), T("NAME", "Face")
        m = T("INITIAL", "M")
        hoos_foos = T("NAME", "Hoos-Foos")

        self.assertSequenceEqual([[moon, face]],
                                 HumanNames._section_list([moon, face], "AND"))
        self.assertSequenceEqual([[moon, face], [hoos_foos]],
                                 HumanNames._section_list([moon, face, AND, hoos_foos], "AND"))

    def test_is_name(self):
        #Marvin O'Gravel Balloon Face
        marvin, ogravel, balloon, face = T("NAME", "Marvin"), T("NAME", "O'Gravel"), T("NAME", "Balloon"), \
                                         T("NAME", "Face")
        mobf = T("INITIAL", "M.O.B.F")

        self.assertTrue(HumanNames._is_name([marvin, ogravel, balloon, face]))
        self.assertTrue(HumanNames._is_name([mobf, face]))
        self.assertTrue(HumanNames._is_name([face, mobf]))
        self.assertFalse(HumanNames._is_name([face]))
        self.assertFalse(HumanNames._is_name([mobf]))

    def test_name_list(self):
        #Dave McCave, Sunny Jim, Bodkin Van Horn
        dave, mccave = T("NAME", "Dave"), T("NAME", "McCave")
        sunny, jim = T("NAME", "Sunny"), T("NAME", "Jim")
        bodkin, van, horn = T("NAME", "Bodkin"), T("NAME", "Van"), T("NAME", "Horn")

        # Just name
        self.assertSequenceEqual([[dave, mccave]],
                                 HumanNames._name_list([dave, mccave]))
        #Name and name
        self.assertSequenceEqual([[dave, mccave], [sunny, jim]],
                                 HumanNames._name_list([dave, mccave, AND, sunny, jim]))
        #Name, name
        self.assertSequenceEqual([[dave, mccave], [sunny, jim]],
                                 HumanNames._name_list([dave, mccave, COMMA, sunny, jim]))
        #Last, first
        self.assertSequenceEqual([[mccave, COMMA, dave]],
                                 HumanNames._name_list([mccave, COMMA, dave]))
        #Last, first and name
        self.assertSequenceEqual([[dave, mccave], [sunny, jim]],
                                 HumanNames._name_list([dave, mccave, COMMA, sunny, jim]))
        #Name, name and name
        self.assertSequenceEqual([[dave, mccave], [sunny, jim], [bodkin, van, horn]],
                                 HumanNames._name_list([dave, mccave, COMMA, sunny, jim, AND, bodkin, van, horn]))
        #Last, first, name and name
        self.assertSequenceEqual([[mccave, COMMA, dave], [sunny, jim], [bodkin, van, horn]],
                                 HumanNames._name_list(
                                     [mccave, COMMA, dave, COMMA, sunny, jim, AND, bodkin, van, horn]))
        #Double last, first
        self.assertSequenceEqual([[van, horn, COMMA, bodkin]],
                                 HumanNames._name_list([van, horn, COMMA, bodkin]))
        #Double last, first and name
        self.assertSequenceEqual([[van, horn, COMMA, bodkin], [sunny, jim]],
                                 HumanNames._name_list([van, horn, COMMA, bodkin, AND, sunny, jim]))

    def test_order_name(self):
        michael, carmichael, zutt = T("NAME", "Michael"), T("NAME", "Carmichael"), T("NAME", "Zutt")
        m, c = T("INITIAL", "M"), T("INITIAL", "C")

        self.assertSequenceEqual([michael, carmichael, zutt],
                                 HumanNames._order_name([zutt, COMMA, michael, carmichael]))
        self.assertSequenceEqual([michael, carmichael, zutt], HumanNames._order_name([michael, carmichael, zutt]))
        self.assertSequenceEqual([m, c, zutt], HumanNames._order_name([zutt, m, c]))

    def test_humannames(self):
        self.assertEqual("Oliver Boliver Butt", str(HumanNames("Oliver Boliver Butt")))
        self.assertEqual("O. Boliver Butt", str(HumanNames("O. Boliver Butt")))
        self.assertEqual("Oliver B. Butt", str(HumanNames("Oliver B. Butt")))
        self.assertEqual("OB Butt", str(HumanNames("OB Butt")))
        self.assertEqual("O B Butt", str(HumanNames("O B Butt")))
        self.assertEqual("Oliver Boliver Butt", str(HumanNames("Butt, Oliver Boliver")))
        self.assertEqual("OB Butt", str(HumanNames("Butt, OB")))
        self.assertEqual("OB Butt", str(HumanNames("Butt OB")))

        self.assertEqual("Oliver Boliver Butt and Zanzibar Buck-Buck McFate",
                         str(HumanNames("Oliver Boliver Butt and Zanzibar Buck-Buck McFate")))
        self.assertEqual("Oliver Boliver Butt and Zanzibar Buck-Buck McFate",
                         str(HumanNames("Butt, Oliver Boliver and Zanzibar Buck-Buck McFate")))
        self.assertEqual("Oliver Boliver Butt and Zanzibar Buck-Buck McFate",
                         str(HumanNames("Oliver Boliver Butt, Zanzibar Buck-Buck McFate")))
        self.assertEqual("OB Butt and ZBB McFate",
                         str(HumanNames("Butt, OB and McFate, ZBB")))
        self.assertEqual("OB Butt and ZBB McFate",
                         str(HumanNames("Butt OB and McFate ZBB")))

        self.assertEqual("Oliver Boliver Butt and Zanzibar Buck-Buck McFate and Buffalo Bill",
                         str(HumanNames("Oliver Boliver Butt and Zanzibar Buck-Buck McFate and Buffalo Bill")))
        self.assertEqual("Oliver Boliver Butt and Zanzibar Buck-Buck McFate and Buffalo Bill",
                         str(HumanNames("Oliver Boliver Butt, Zanzibar Buck-Buck McFate and Buffalo Bill")))
        self.assertEqual("Oliver Boliver Butt and Zanzibar Buck-Buck McFate and Buffalo Bill",
                         str(HumanNames("Oliver Boliver Butt, Zanzibar Buck-Buck McFate, and Buffalo Bill")))
        self.assertEqual("Oliver Boliver Butt and Zanzibar Buck-Buck McFate and Buffalo Bill",
                         str(HumanNames("Butt, Oliver Boliver, Zanzibar Buck-Buck McFate, and Buffalo Bill")))
