def deduplicate_list(list_with_dups):
    return list(dict.fromkeys(list_with_dups))


def filter_list_by_set(original_list, filter_set):
    return [elem for elem in original_list if elem not in filter_set]


def write_to_file(filename, text, message):  # pragma: no cover
    with open(filename, 'w') as f:
        f.write(text)

    print(message)
