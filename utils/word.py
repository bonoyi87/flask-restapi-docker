# 초성 리스트. 00 ~ 18
import re

CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
# 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']


def seperate_word(word, only_chosung=False):
    r_lst = []
    for w in list(word.strip()):
        if '가' <= w <= '힣':
            ch1 = (ord(w) - ord('가')) // 588
            ch2 = ((ord(w) - ord('가')) - (588 * ch1)) // 28
            ch3 = (ord(w) - ord('가')) - (588 * ch1) - 28 * ch2
            if only_chosung:
                r_lst.append(CHOSUNG_LIST[ch1])
            else:
                r_lst.append(CHOSUNG_LIST[ch1])
                r_lst.append(JUNGSUNG_LIST[ch2])
                r_lst.append(JONGSUNG_LIST[ch3])
        else:
            r_lst.append(w)
    return ''.join(r_lst) if r_lst else ''


def get_hangul(val: str) -> str:
    """
    한글만 가져오기
    :param val:
    :return: str
    """
    regex_only_hangul = re.compile('[ㄱ-ㅎㅏ-ㅣ가-힣]')
    return "".join(regex_only_hangul.findall(val))


def has_chosung(val: str) -> bool:
    """
    초성만 포함되었는지 여부
    :param val:
    :return: bool
    """
    regex = re.compile(r"[ㄱ-ㅎ]")
    if regex.match(val):
        return True
    return False
