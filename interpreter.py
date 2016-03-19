import tokenizer

def run_file(filename):
    with open(filename, 'r') as f:
        code = f.read()
    return run_code(code)

def run_code(code):
    tokens = tokenizer.tokenize(code)
    for token in tokens:
        print(token)
