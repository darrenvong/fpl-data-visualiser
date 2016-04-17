# -*- coding: utf-8 -*-

"""
This module contains group of related auxiliary (helper) functions which aids the
generation of the front-end web application's pages.
@author: Darren Vong
"""
import os

from pymongo import MongoClient
from bson import SON

import profiles

###############################################################################
# Extracted from Carlos Buenos (2009-2010) code on accent folding.
# The accent map with the original code may be found
# at https://github.com/aristus/accent-folding/blob/master/accent-fold.py

accent_map = {u'ẚ':u'a',u'Á':u'a',u'á':u'a',u'À':u'a',u'à':u'a',u'Ă':u'a',u'ă':u'a',u'Ắ':u'a',u'ắ':u'a',u'Ằ':u'a',u'ằ':u'a',u'Ẵ':u'a',u'ẵ':u'a',u'Ẳ':u'a',u'ẳ':u'a',u'Â':u'a',u'â':u'a',u'Ấ':u'a',u'ấ':u'a',u'Ầ':u'a',u'ầ':u'a',u'Ẫ':u'a',u'ẫ':u'a',u'Ẩ':u'a',u'ẩ':u'a',u'Ǎ':u'a',u'ǎ':u'a',u'Å':u'a',u'å':u'a',u'Ǻ':u'a',u'ǻ':u'a',u'Ä':u'a',u'ä':u'a',u'Ǟ':u'a',u'ǟ':u'a',u'Ã':u'a',u'ã':u'a',u'Ȧ':u'a',u'ȧ':u'a',u'Ǡ':u'a',u'ǡ':u'a',u'Ą':u'a',u'ą':u'a',u'Ā':u'a',u'ā':u'a',u'Ả':u'a',u'ả':u'a',u'Ȁ':u'a',u'ȁ':u'a',u'Ȃ':u'a',u'ȃ':u'a',u'Ạ':u'a',u'ạ':u'a',u'Ặ':u'a',u'ặ':u'a',u'Ậ':u'a',u'ậ':u'a',u'Ḁ':u'a',u'ḁ':u'a',u'Ⱥ':u'a',u'ⱥ':u'a',u'Ǽ':u'a',u'ǽ':u'a',u'Ǣ':u'a',u'ǣ':u'a',u'Ḃ':u'b',u'ḃ':u'b',u'Ḅ':u'b',u'ḅ':u'b',u'Ḇ':u'b',u'ḇ':u'b',u'Ƀ':u'b',u'ƀ':u'b',u'ᵬ':u'b',u'Ɓ':u'b',u'ɓ':u'b',u'Ƃ':u'b',u'ƃ':u'b',u'Ć':u'c',u'ć':u'c',u'Ĉ':u'c',u'ĉ':u'c',u'Č':u'c',u'č':u'c',u'Ċ':u'c',u'ċ':u'c',u'Ç':u'c',u'ç':u'c',u'Ḉ':u'c',u'ḉ':u'c',u'Ȼ':u'c',u'ȼ':u'c',u'Ƈ':u'c',u'ƈ':u'c',u'ɕ':u'c',u'Ď':u'd',u'ď':u'd',u'Ḋ':u'd',u'ḋ':u'd',u'Ḑ':u'd',u'ḑ':u'd',u'Ḍ':u'd',u'ḍ':u'd',u'Ḓ':u'd',u'ḓ':u'd',u'Ḏ':u'd',u'ḏ':u'd',u'Đ':u'd',u'đ':u'd',u'ᵭ':u'd',u'Ɖ':u'd',u'ɖ':u'd',u'Ɗ':u'd',u'ɗ':u'd',u'Ƌ':u'd',u'ƌ':u'd',u'ȡ':u'd',u'ð':u'd',u'É':u'e',u'Ə':u'e',u'Ǝ':u'e',u'ǝ':u'e',u'é':u'e',u'È':u'e',u'è':u'e',u'Ĕ':u'e',u'ĕ':u'e',u'Ê':u'e',u'ê':u'e',u'Ế':u'e',u'ế':u'e',u'Ề':u'e',u'ề':u'e',u'Ễ':u'e',u'ễ':u'e',u'Ể':u'e',u'ể':u'e',u'Ě':u'e',u'ě':u'e',u'Ë':u'e',u'ë':u'e',u'Ẽ':u'e',u'ẽ':u'e',u'Ė':u'e',u'ė':u'e',u'Ȩ':u'e',u'ȩ':u'e',u'Ḝ':u'e',u'ḝ':u'e',u'Ę':u'e',u'ę':u'e',u'Ē':u'e',u'ē':u'e',u'Ḗ':u'e',u'ḗ':u'e',u'Ḕ':u'e',u'ḕ':u'e',u'Ẻ':u'e',u'ẻ':u'e',u'Ȅ':u'e',u'ȅ':u'e',u'Ȇ':u'e',u'ȇ':u'e',u'Ẹ':u'e',u'ẹ':u'e',u'Ệ':u'e',u'ệ':u'e',u'Ḙ':u'e',u'ḙ':u'e',u'Ḛ':u'e',u'ḛ':u'e',u'Ɇ':u'e',u'ɇ':u'e',u'ɚ':u'e',u'ɝ':u'e',u'Ḟ':u'f',u'ḟ':u'f',u'ᵮ':u'f',u'Ƒ':u'f',u'ƒ':u'f',u'Ǵ':u'g',u'ǵ':u'g',u'Ğ':u'g',u'ğ':u'g',u'Ĝ':u'g',u'ĝ':u'g',u'Ǧ':u'g',u'ǧ':u'g',u'Ġ':u'g',u'ġ':u'g',u'Ģ':u'g',u'ģ':u'g',u'Ḡ':u'g',u'ḡ':u'g',u'Ǥ':u'g',u'ǥ':u'g',u'Ɠ':u'g',u'ɠ':u'g',u'Ĥ':u'h',u'ĥ':u'h',u'Ȟ':u'h',u'ȟ':u'h',u'Ḧ':u'h',u'ḧ':u'h',u'Ḣ':u'h',u'ḣ':u'h',u'Ḩ':u'h',u'ḩ':u'h',u'Ḥ':u'h',u'ḥ':u'h',u'Ḫ':u'h',u'ḫ':u'h',u'H':u'h',u'̱':u'h',u'ẖ':u'h',u'Ħ':u'h',u'ħ':u'h',u'Ⱨ':u'h',u'ⱨ':u'h',u'Í':u'i',u'í':u'i',u'Ì':u'i',u'ì':u'i',u'Ĭ':u'i',u'ĭ':u'i',u'Î':u'i',u'î':u'i',u'Ǐ':u'i',u'ǐ':u'i',u'Ï':u'i',u'ï':u'i',u'Ḯ':u'i',u'ḯ':u'i',u'Ĩ':u'i',u'ĩ':u'i',u'İ':u'i',u'i':u'i',u'Į':u'i',u'į':u'i',u'Ī':u'i',u'ī':u'i',u'Ỉ':u'i',u'ỉ':u'i',u'Ȉ':u'i',u'ȉ':u'i',u'Ȋ':u'i',u'ȋ':u'i',u'Ị':u'i',u'ị':u'i',u'Ḭ':u'i',u'ḭ':u'i',u'I':u'i',u'ı':u'i',u'Ɨ':u'i',u'ɨ':u'i',u'Ĵ':u'j',u'ĵ':u'j',u'J':u'j',u'̌':u'j',u'ǰ':u'j',u'ȷ':u'j',u'Ɉ':u'j',u'ɉ':u'j',u'ʝ':u'j',u'ɟ':u'j',u'ʄ':u'j',u'Ḱ':u'k',u'ḱ':u'k',u'Ǩ':u'k',u'ǩ':u'k',u'Ķ':u'k',u'ķ':u'k',u'Ḳ':u'k',u'ḳ':u'k',u'Ḵ':u'k',u'ḵ':u'k',u'Ƙ':u'k',u'ƙ':u'k',u'Ⱪ':u'k',u'ⱪ':u'k',u'Ĺ':u'a',u'ĺ':u'l',u'Ľ':u'l',u'ľ':u'l',u'Ļ':u'l',u'ļ':u'l',u'Ḷ':u'l',u'ḷ':u'l',u'Ḹ':u'l',u'ḹ':u'l',u'Ḽ':u'l',u'ḽ':u'l',u'Ḻ':u'l',u'ḻ':u'l',u'Ł':u'l',u'ł':u'l',u'Ł':u'l',u'̣':u'l',u'ł':u'l',u'̣':u'l',u'Ŀ':u'l',u'ŀ':u'l',u'Ƚ':u'l',u'ƚ':u'l',u'Ⱡ':u'l',u'ⱡ':u'l',u'Ɫ':u'l',u'ɫ':u'l',u'ɬ':u'l',u'ɭ':u'l',u'ȴ':u'l',u'Ḿ':u'm',u'ḿ':u'm',u'Ṁ':u'm',u'ṁ':u'm',u'Ṃ':u'm',u'ṃ':u'm',u'ɱ':u'm',u'Ń':u'n',u'ń':u'n',u'Ǹ':u'n',u'ǹ':u'n',u'Ň':u'n',u'ň':u'n',u'Ñ':u'n',u'ñ':u'n',u'Ṅ':u'n',u'ṅ':u'n',u'Ņ':u'n',u'ņ':u'n',u'Ṇ':u'n',u'ṇ':u'n',u'Ṋ':u'n',u'ṋ':u'n',u'Ṉ':u'n',u'ṉ':u'n',u'Ɲ':u'n',u'ɲ':u'n',u'Ƞ':u'n',u'ƞ':u'n',u'ɳ':u'n',u'ȵ':u'n',u'N':u'n',u'̈':u'n',u'n':u'n',u'̈':u'n',u'Ó':u'o',u'ó':u'o',u'Ò':u'o',u'ò':u'o',u'Ŏ':u'o',u'ŏ':u'o',u'Ô':u'o',u'ô':u'o',u'Ố':u'o',u'ố':u'o',u'Ồ':u'o',u'ồ':u'o',u'Ỗ':u'o',u'ỗ':u'o',u'Ổ':u'o',u'ổ':u'o',u'Ǒ':u'o',u'ǒ':u'o',u'Ö':u'o',u'ö':u'o',u'Ȫ':u'o',u'ȫ':u'o',u'Ő':u'o',u'ő':u'o',u'Õ':u'o',u'õ':u'o',u'Ṍ':u'o',u'ṍ':u'o',u'Ṏ':u'o',u'ṏ':u'o',u'Ȭ':u'o',u'ȭ':u'o',u'Ȯ':u'o',u'ȯ':u'o',u'Ȱ':u'o',u'ȱ':u'o',u'Ø':u'o',u'ø':u'o',u'Ǿ':u'o',u'ǿ':u'o',u'Ǫ':u'o',u'ǫ':u'o',u'Ǭ':u'o',u'ǭ':u'o',u'Ō':u'o',u'ō':u'o',u'Ṓ':u'o',u'ṓ':u'o',u'Ṑ':u'o',u'ṑ':u'o',u'Ỏ':u'o',u'ỏ':u'o',u'Ȍ':u'o',u'ȍ':u'o',u'Ȏ':u'o',u'ȏ':u'o',u'Ơ':u'o',u'ơ':u'o',u'Ớ':u'o',u'ớ':u'o',u'Ờ':u'o',u'ờ':u'o',u'Ỡ':u'o',u'ỡ':u'o',u'Ở':u'o',u'ở':u'o',u'Ợ':u'o',u'ợ':u'o',u'Ọ':u'o',u'ọ':u'o',u'Ộ':u'o',u'ộ':u'o',u'Ɵ':u'o',u'ɵ':u'o',u'Ṕ':u'p',u'ṕ':u'p',u'Ṗ':u'p',u'ṗ':u'p',u'Ᵽ':u'p',u'Ƥ':u'p',u'ƥ':u'p',u'P':u'p',u'̃':u'p',u'p':u'p',u'̃':u'p',u'ʠ':u'q',u'Ɋ':u'q',u'ɋ':u'q',u'Ŕ':u'r',u'ŕ':u'r',u'Ř':u'r',u'ř':u'r',u'Ṙ':u'r',u'ṙ':u'r',u'Ŗ':u'r',u'ŗ':u'r',u'Ȑ':u'r',u'ȑ':u'r',u'Ȓ':u'r',u'ȓ':u'r',u'Ṛ':u'r',u'ṛ':u'r',u'Ṝ':u'r',u'ṝ':u'r',u'Ṟ':u'r',u'ṟ':u'r',u'Ɍ':u'r',u'ɍ':u'r',u'ᵲ':u'r',u'ɼ':u'r',u'Ɽ':u'r',u'ɽ':u'r',u'ɾ':u'r',u'ᵳ':u'r',u'ß':u's',u'Ś':u's',u'ś':u's',u'Ṥ':u's',u'ṥ':u's',u'Ŝ':u's',u'ŝ':u's',u'Š':u's',u'š':u's',u'Ṧ':u's',u'ṧ':u's',u'Ṡ':u's',u'ṡ':u's',u'ẛ':u's',u'Ş':u's',u'ş':u's',u'Ṣ':u's',u'ṣ':u's',u'Ṩ':u's',u'ṩ':u's',u'Ș':u's',u'ș':u's',u'ʂ':u's',u'S':u's',u'̩':u's',u's':u's',u'̩':u's',u'Þ':u't',u'þ':u't',u'Ť':u't',u'ť':u't',u'T':u't',u'̈':u't',u'ẗ':u't',u'Ṫ':u't',u'ṫ':u't',u'Ţ':u't',u'ţ':u't',u'Ṭ':u't',u'ṭ':u't',u'Ț':u't',u'ț':u't',u'Ṱ':u't',u'ṱ':u't',u'Ṯ':u't',u'ṯ':u't',u'Ŧ':u't',u'ŧ':u't',u'Ⱦ':u't',u'ⱦ':u't',u'ᵵ':u't',u'ƫ':u't',u'Ƭ':u't',u'ƭ':u't',u'Ʈ':u't',u'ʈ':u't',u'ȶ':u't',u'Ú':u'u',u'ú':u'u',u'Ù':u'u',u'ù':u'u',u'Ŭ':u'u',u'ŭ':u'u',u'Û':u'u',u'û':u'u',u'Ǔ':u'u',u'ǔ':u'u',u'Ů':u'u',u'ů':u'u',u'Ü':u'u',u'ü':u'u',u'Ǘ':u'u',u'ǘ':u'u',u'Ǜ':u'u',u'ǜ':u'u',u'Ǚ':u'u',u'ǚ':u'u',u'Ǖ':u'u',u'ǖ':u'u',u'Ű':u'u',u'ű':u'u',u'Ũ':u'u',u'ũ':u'u',u'Ṹ':u'u',u'ṹ':u'u',u'Ų':u'u',u'ų':u'u',u'Ū':u'u',u'ū':u'u',u'Ṻ':u'u',u'ṻ':u'u',u'Ủ':u'u',u'ủ':u'u',u'Ȕ':u'u',u'ȕ':u'u',u'Ȗ':u'u',u'ȗ':u'u',u'Ư':u'u',u'ư':u'u',u'Ứ':u'u',u'ứ':u'u',u'Ừ':u'u',u'ừ':u'u',u'Ữ':u'u',u'ữ':u'u',u'Ử':u'u',u'ử':u'u',u'Ự':u'u',u'ự':u'u',u'Ụ':u'u',u'ụ':u'u',u'Ṳ':u'u',u'ṳ':u'u',u'Ṷ':u'u',u'ṷ':u'u',u'Ṵ':u'u',u'ṵ':u'u',u'Ʉ':u'u',u'ʉ':u'u',u'Ṽ':u'v',u'ṽ':u'v',u'Ṿ':u'v',u'ṿ':u'v',u'Ʋ':u'v',u'ʋ':u'v',u'Ẃ':u'w',u'ẃ':u'w',u'Ẁ':u'w',u'ẁ':u'w',u'Ŵ':u'w',u'ŵ':u'w',u'W':u'w',u'̊':u'w',u'ẘ':u'w',u'Ẅ':u'w',u'ẅ':u'w',u'Ẇ':u'w',u'ẇ':u'w',u'Ẉ':u'w',u'ẉ':u'w',u'Ẍ':u'x',u'ẍ':u'x',u'Ẋ':u'x',u'ẋ':u'x',u'Ý':u'y',u'ý':u'y',u'Ỳ':u'y',u'ỳ':u'y',u'Ŷ':u'y',u'ŷ':u'y',u'Y':u'y',u'̊':u'y',u'ẙ':u'y',u'Ÿ':u'y',u'ÿ':u'y',u'Ỹ':u'y',u'ỹ':u'y',u'Ẏ':u'y',u'ẏ':u'y',u'Ȳ':u'y',u'ȳ':u'y',u'Ỷ':u'y',u'ỷ':u'y',u'Ỵ':u'y',u'ỵ':u'y',u'ʏ':u'y',u'Ɏ':u'y',u'ɏ':u'y',u'Ƴ':u'y',u'ƴ':u'y',u'Ź':u'z',u'ź':u'z',u'Ẑ':u'z',u'ẑ':u'z',u'Ž':u'z',u'ž':u'z',u'Ż':u'z',u'ż':u'z',u'Ẓ':u'z',u'ẓ':u'z',u'Ẕ':u'z',u'ẕ':u'z',u'Ƶ':u'z',u'ƶ':u'z',u'Ȥ':u'z',u'ȥ':u'z',u'ʐ':u'z',u'ʑ':u'z',u'Ⱬ':u'z',u'ⱬ':u'z',u'Ǯ':u'z',u'ǯ':u'z',u'ƺ':u'z',u'２':u'2',u'６':u'6',u'Ｂ':u'B',u'Ｆ':u'F',u'Ｊ':u'J',u'Ｎ':u'N',u'Ｒ':u'R',u'Ｖ':u'V',u'Ｚ':u'Z',u'ｂ':u'b',u'ｆ':u'f',u'ｊ':u'j',u'ｎ':u'n',u'ｒ':u'r',u'ｖ':u'v',u'ｚ':u'z',u'１':u'1',u'５':u'5',u'９':u'9',u'Ａ':u'A',u'Ｅ':u'E',u'Ｉ':u'I',u'Ｍ':u'M',u'Ｑ':u'Q',u'Ｕ':u'U',u'Ｙ':u'Y',u'ａ':u'a',u'ｅ':u'e',u'ｉ':u'i',u'ｍ':u'm',u'ｑ':u'q',u'ｕ':u'u',u'ｙ':u'y',u'０':u'0',u'４':u'4',u'８':u'8',u'Ｄ':u'D',u'Ｈ':u'H',u'Ｌ':u'L',u'Ｐ':u'P',u'Ｔ':u'T',u'Ｘ':u'X',u'ｄ':u'd',u'ｈ':u'h',u'ｌ':u'l',u'ｐ':u'p',u'ｔ':u't',u'ｘ':u'x',u'３':u'3',u'７':u'7',u'Ｃ':u'C',u'Ｇ':u'G',u'Ｋ':u'K',u'Ｏ':u'O',u'Ｓ':u'S',u'Ｗ':u'W',u'ｃ':u'c',u'ｇ':u'g',u'ｋ':u'k',u'ｏ':u'o',u'ｓ':u's',u'ｗ':u'w'};

accent_map = dict((ord(k),v) for k,v in accent_map.iteritems())

def accent_fold(s):
    if not s: return ''
    return unicode(s).translate(accent_map)
###############################################################################

AGENT_NAME = "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0"
headers = {"User-Agent": AGENT_NAME}

def connect(on_heroku=False):
    if not on_heroku:
        client = MongoClient(document_class=SON)
        players = client.players.current_gw
    else:
        client = MongoClient(os.environ["MONGODB_URI"])
        players = client.get_default_database().current_gw
    return client, players

def get_current_gameweek(col):
    # Using Vardy here as he's started since gameweek 1 and has had no blank gameweeks
    return profiles.get_profile_contents("Vardy", col)["current_gw"]

def capitalise_camel_case_words(s):
    """Capitalises a camel case string and separate the resultant words with spaces"""
    result = ""
    for char in s:
        result = result+char if char.islower() else result+" "+char
    
    return result.capitalize()

if __name__ == '__main__':
    print capitalise_camel_case_words("thisIsAReallyLongFuckingString")