# author: https://github.com/pySTE

from typing import Tuple, Optional, List


class WordComparator:
    """
    Класс для сравнения слов и вычисления их схожести.
    Использует расстояние Левенштейна для определения различий между словами.
    """

    def __init__(self, case_sensitive: bool = False):
        """
        Инициализация компаратора слов.

        :param case_sensitive: учитывать ли регистр букв при сравнении (по умолчанию False)
        """
        self.case_sensitive = case_sensitive

    def _prepare_words(self, word1: str, word2: str) -> Tuple[str, str]:
        """
        Подготавливает слова для сравнения: приводит к одному регистру, если необходимо.

        :param word1: первое слово
        :param word2: второе слово
        :return: кортеж подготовленных слов
        """
        if not self.case_sensitive:
            return word1.lower(), word2.lower()
        return word1, word2

    def calculate_distance(self, word1: str, word2: str) -> int:
        """
        Вычисляет расстояние Левенштейна между двумя словами.

        Расстояние Левенштейна - это минимальное количество операций вставки,
        удаления или замены символа, необходимых для превращения одного слова в другое.

        :param word1: первое слово
        :param word2: второе слово
        :return: расстояние Левенштейна
        """
        word1, word2 = self._prepare_words(word1, word2)
        size_x = len(word1) + 1
        size_y = len(word2) + 1

        matrix: List[List[int]] = [[0] * size_y for _ in range(size_x)]

        for x in range(size_x):
            matrix[x][0] = x
        for y in range(size_y):
            matrix[0][y] = y

        for x in range(1, size_x):
            for y in range(1, size_y):
                if word1[x - 1] == word2[y - 1]:
                    substitution_cost = 0
                else:
                    substitution_cost = 1

                matrix[x][y] = min(
                    matrix[x - 1][y] + 1,  # удаление
                    matrix[x][y - 1] + 1,  # вставка
                    matrix[x - 1][y - 1] + substitution_cost  # замена
                )

        return matrix[size_x - 1][size_y - 1]

    def calculate_similarity(self, word1: str, word2: str) -> float:
        """
        Вычисляет процент схожести между двумя словами.

        :param word1: первое слово
        :param word2: второе слово
        :return: процент схожести (0.0 - 1.0)
        """
        if not word1 and not word2:
            return 1.0

        distance = self.calculate_distance(word1, word2)
        max_len = max(len(word1), len(word2))

        if max_len == 0:
            return 1.0

        return 1.0 - (distance / max_len)

    def is_similar(self, word1: str, word2: str, threshold: float = 0.6) -> bool:
        """
        Проверяет, являются ли слова похожими на основе заданного порога.

        :param word1: первое слово
        :param word2: второе слово
        :param threshold: порог схожести (по умолчанию 0.6)
        :return: True если процент схожести выше порога, иначе False
        """
        similarity = self.calculate_similarity(word1, word2)
        return similarity >= threshold


def compare_words(word1: str, word2: str, threshold: Optional[float] = None) -> Tuple[float, Optional[bool]]:
    """
    Функция для быстрого сравнения слов без создания экземпляра класса.

    :param word1: первое слово
    :param word2: второе слово
    :param threshold: опциональный порог для бинарного результата
    :return: кортеж (процент схожести, результат сравнения с порогом если threshold указан)
    """
    comparator = WordComparator()
    similarity = comparator.calculate_similarity(word1, word2)

    if threshold is not None:
        return similarity, similarity >= threshold
    return similarity, None
