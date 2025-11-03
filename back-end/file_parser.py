def parse_text(filename):
    with open(filename, 'r') as file:
        text = file.read()
    words = text.split()
    difficult_words = [word for word in words if len(word) > 7]
    return difficult_words
