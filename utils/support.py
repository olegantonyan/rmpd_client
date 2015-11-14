# -*- coding: utf-8 -*-


def underscore_to_camelcase(s):
    def camelcase_words(words):
        for word in words:
            if not word:
                yield "_"
                continue
            yield word.capitalize()
    return ''.join(camelcase_words(s.split('_')))
