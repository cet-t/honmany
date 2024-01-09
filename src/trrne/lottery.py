from typing import Generic, TypeVar
from random import uniform

T = TypeVar('T')


class LotteryPair(Generic[T]):
    def __init__(self, pairs: list[tuple[T, float]]) -> None:
        super().__init__()
        self.__pairs: list[tuple[T, float]] = pairs
        self.__subjects: list[T] = [pairs[i][0] for i in range(self.length)]
        self.__weights: list[float] = [pairs[i][1] for i in range(self.length)]

    @property
    def length(self) -> int:
        return len(self.__pairs)

    @property
    def pairs(self) -> list[tuple[T, float]]:
        return self.__pairs

    @property
    def subjects(self) -> list[T]:
        return self.__subjects

    @property
    def weights(self) -> list[float]:
        return self.__weights

    @property
    def total_weight(self) -> float:
        dst = .0
        for weight in self.__weights:
            dst += weight
        return dst


class Lottery(Generic[T]):
    @staticmethod
    def bst(weights: list[float]) -> int:
        '''二分探索木'''
        if len(weights) <= 0:
            # raise Exception('からっぽやんけ')
            return -1

        totals: list[float] = []
        total: float = 0.0
        for i in range(len(weights)):
            total += weights[i]
            totals.append(total)
        # for i in totals:
        #     print(f'totals: {i}')

        r: float = uniform(0, total)
        bottom: int = 0
        top: int = len(totals)-1
        while bottom < top:
            center: int = int((bottom+top)/2)
            if r > totals[center]:
                bottom = center+1
            else:
                if r >= totals[center-1] if center > 0 else 0.0:
                    return center
                top = center
        return top

    @staticmethod
    def weighted(pairs: LotteryPair[T]) -> T:
        if pairs.length() <= 0:
            raise Exception()
        return pairs.subjects()[Lottery.bst(pairs.weights())] if pairs.length() != 1 else pairs.subjects()[0]
