import re


class SimilarityTool:
    @staticmethod
    def compare_strings(str1, str2):
        pairs1 = SimilarityTool.word_letter_pairs(str1.upper())
        pairs2 = SimilarityTool.word_letter_pairs(str2.upper())

        intersection = 0
        union = len(pairs1) + len(pairs2)

        for i in range(len(pairs1)):
            for j in range(len(pairs2)):
                if pairs1[i] == pairs2[j]:
                    intersection += 1
                    pairs2.pop(j)
                    break

        return (2.0 * intersection) / union

    @staticmethod
    def word_letter_pairs(str1):
        all_pairs = []
        words = re.split(r'\s', str1)

        for w in words:
            if w:
                pairs_in_word = SimilarityTool.letter_pairs(w)
                all_pairs.extend(pairs_in_word)

        return all_pairs

    @staticmethod
    def letter_pairs(str1):
        num_pairs = len(str1) - 1
        return [str1[i:i + 2] for i in range(num_pairs)]
