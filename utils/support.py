# -*- coding: utf-8 -*-


def underscore_to_camelcase(s):
    def camelcase_words(words):
        for word in words:
            if not word:
                yield "_"
                continue
            yield word.capitalize()
    return ''.join(camelcase_words(s.split('_')))


def camelcase_to_underscore(s):
    words = []
    from_char_position = 0
    for current_char_position, char in enumerate(s):
        if char.isupper() and from_char_position < current_char_position:
            words.append(s[from_char_position:current_char_position].lower())
            from_char_position = current_char_position
    words.append(s[from_char_position:].lower())
    return '_'.join(words)
