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


def list_compact(arg):
    return [j for j in arg if j is not None]


def join_list_excerpt(lst, max_size, char=', '):
    sz = len(lst)
    if sz > max_size:
        lst = lst[0:max_size]
        lst.append('... and {c} more'.format(c=sz - max_size))
    return char.join(lst)
