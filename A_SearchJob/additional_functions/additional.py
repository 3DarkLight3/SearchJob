import datetime


def paginator_array(all_pages, current_page):
    lst = []

    if all_pages < 6:
        lst = [i+1 for i in range(0, all_pages)]
    else:
        if current_page < 4:
            lst.extend([i+1 for i in range(0, current_page+1)])
            lst.extend(['...', all_pages])

        elif all_pages - current_page < 4:
            lst.extend([1, '...'])
            lst.extend([i for i in range(current_page-1, all_pages+1)])

        else:
            lst.extend([1, '...'])
            lst.extend([i+1 for i in range(current_page-2, current_page+1)])
            lst.extend(['...', all_pages])

    return lst


def split_lines(line):

    line = line.split('. ')

    if len(line) != 1:

        for sentence in line:
            if isinstance(sentence[0], str):
                if sentence[0] == sentence[0].lower():
                    first_sentence = line[line.index(sentence) - 1]
                    second_sentence = sentence
                    line.remove(first_sentence)
                    line.remove(second_sentence)

                    full_sentence = f'{first_sentence} {second_sentence}'
                    line.insert(0, full_sentence)

        return line

    line = line[0].split('.\r\n')

    return line


def set_width_height_for_image(width, height):
    size = 100

    if width == height:
        return [size, size]

    elif width > height:
        width = int(round((size * (width / height)), 0))
        return [width, size]

    else:
        height = int(round((size * (height / width)), 0))
        return [size, height]


def get_current_year():

    current_date = datetime.datetime.now()
    return current_date.year
