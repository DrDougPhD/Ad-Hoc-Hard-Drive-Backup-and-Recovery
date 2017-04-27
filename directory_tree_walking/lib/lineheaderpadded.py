#!/usr/bin/env python3
#
#  Create pretty line headers, padded with dashes, equals, octothorpes, tildes,
#    and whatever else you want.
#
#  Examples:
#
#      ==========================: Hello, World! :==========================
#
#      ~~~~~~~~~~~~~~~: Error Messages:~~~~~~~~~~~~~~~
#
#      !!!!!!!!!!!!!!!!!!!! CRITICAL FAILURE !!!!!!!!!!!!!!!!!!!!
#
#
# LICENSE
#
#      Copyright 2017 Doug McGeehan
#      GPL GNUv3
#

def hr(title, line_char='=', bookend=':', width=80):
    # convert to string in case a non-str type is provided (e.g. ints)
    title = str(title)
    n = len(title)
    title_length_split = n/2

    if bookend: # is neither None or an empty space
        assert len(bookend) == 1, (\
          'Invalid bookend: must be one character, not "{}"').format(bookend)

        bookend_spaces = 4
    else:
        bookend = ''
        bookend_spaces = 2

    # -------------------------: <title> :-------------------------
    # the bookend_spaces comes from two colons ':' and two spaces surrounding
    #     the title
    # the linechars_count comes from subtracting the title length and the
    #     spaces occupied by the colons and spaces
    linechars_count = width - n - bookend_spaces
    half_linechars_count = linechars_count // 2

    hr_string = '{line_chars}{bookend} {title} {bookend}{line_chars}'.format(
        line_chars=line_char*half_linechars_count,
        bookend=bookend,
        title=title)
    # correct for the splitting not being exactly half
    if len(hr_string) != width:
        hr_string = hr_string + line_char

    return hr_string


if __name__ == '__main__':

    # Default line header
    # ===============================: Hello, World! :================================
    hello_world_short = hr('Hello, World!')
    print(hello_world_short)
    assert len(hello_world_short) == 80


    # Custom line characters and bookends
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# Mad Waves, Brah #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
    wavey = hr(title='Mad Waves, Brah', line_char='~', bookend='#')
    print(wavey)
    assert len(wavey) == 80


    # Custom header width
    # ====: Super Narrow :=====
    narrow_header_width = 25
    narrow_header = hr(title='Super Narrow', width=narrow_header_width)
    print(narrow_header)
    assert len(narrow_header) == narrow_header_width


    # Custom line characters, no bookends
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! CRITICAL ERROR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    critical_error_80_char_width = hr(title='CRITICAL ERROR', line_char='!',
                                      bookend=None)
    print(critical_error_80_char_width)
    assert len(critical_error_80_char_width) == 80
    print('(not really, just demoing)\n')


    # TODO: enforce a minimum length based on title
    # short_title = 'Short Title'
    # min_length_header = hr(title=short_title, width=short_title//2)
    # print(min_length_header)
    # assert len(min_length_header) > short_title//2

