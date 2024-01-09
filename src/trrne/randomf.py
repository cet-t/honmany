from random import SystemRandom
from enum import Enum


class STRTYPE(Enum):
    MIX = 0
    ALPHABET = 1
    JP = 2
    NUM = 3


class Rnd:
    __ALPHABETS: str = 'abcdefghijklmnopqrstuvwxyz'
    __NUMBERS: str = '1234567890'
    __JAPANESES: str = 'あいうえおかきくけこがぎぐげごさしすせそざじずぜぞたちつてとだぢづでどなにぬねのはひふへほばびぶべぼぱぴぷぺぽまみむめもやゆよらりるれろわをん'

    @staticmethod
    def normal_char(n: int) -> list:
        chars = list(Rnd.__ALPHABETS)
        dst: list = []
        for _ in range(n := len(chars)-1 if n > len(chars) else n-1):
            dst.append(chars[Rnd.randint(0, n)])
        return dst

    @staticmethod
    def randstr(n: int, *, type=STRTYPE.MIX) -> str:
        if not isinstance(n, int) or not isinstance(type, STRTYPE):
            raise TypeError()

        def mixer(src: str) -> str:
            dst: str = ''
            for _ in range(n):
                dst += src[Rnd.randint(max=len(src)-1)]
            return dst

        if type == STRTYPE.ALPHABET:
            return mixer(Rnd.__ALPHABETS)
        elif type == STRTYPE.JP:
            return mixer(Rnd.__JAPANESES)
        elif type == STRTYPE.NUM:
            return mixer(Rnd.__NUMBERS)
        else:
            return mixer(Rnd.__ALPHABETS + Rnd.__NUMBERS)

    @staticmethod
    def randint(min: int = 0, max: int = 0) -> int:
        if not isinstance(min, int) or not isinstance(max, int):
            raise TypeError()
        return SystemRandom().randint(int(min), int(max))

    @staticmethod
    def randfloat(min: float = 0.0, max: float = 0.0) -> float:
        if not isinstance(min, (int, float)) or not isinstance(max, (int, float)):
            raise TypeError()
        return SystemRandom().uniform(min, max)


# https://qiita.com/mk668a/items/d53515817c41e22e77f0
# https://www.hanachiru-blog.com/entry/2019/02/01/190918
