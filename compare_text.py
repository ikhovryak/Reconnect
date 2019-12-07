
def clean(text):
    symbol = """`~!@#$%^&*()_-+={[}]|\:;'<",>.?/'"""
    clean = ""
    for i in text:
        if i in symbol:
            add = ""
        else:
            add = i
        clean = clean + add
    return clean

def list_of_words(text):
    return text.split(" ")

def remove_words(list_words, text_list):
    for i in text_list:
        if i in list_words:
            text_list.remove(i)
    return text_list


def compare(expected_list, got_list):
    not_matched = {}
    # Key = Expected, Value = Got
    if len(got_list) < len(expected_list):                      # expected text is longer than the got text
        min_list, max_list = got_list, expected_list
        for i in range(len(min_list)):
            if min_list[i] != max_list[i]:
                not_matched[expected_list[i]] = got_list[i]
        list_difference = len(max_list) - len(min_list)
        remaining = max_list[len(min_list):len(max_list)]
        for k in remaining:
            not_matched[k] = ""
    else:
        max_list, min_list = got_list, expected_list
        for i in range(len(min_list)):
            if min_list[i] != max_list[i]:
                not_matched[expected_list[i]] = got_list[i]
        list_difference = len(max_list) - len(min_list)
        remaining = max_list[len(min_list):len(max_list)]
        for k in range(len(remaining)):
            not_matched[k] = remaining[k]

    return not_matched

if __name__ == '__main__':
    remove_these_words = ["a", "um", "uh", "ah", "umm", "o"]
    got_text = "ENTER YOUR GOT TEXT HERE"
    expected_text = "ENTER YOUR EXPECTED TEXT HERE"
    expected_list = list_of_words(clean(expected_text))
    got_list = list_of_words(clean(got_text))
    refined_expected_list = remove_words(remove_these_words, expected_list)
    refined_got_list = remove_words(remove_these_words, got_list)
    print(compare(refined_expected_list, refined_got_list))







