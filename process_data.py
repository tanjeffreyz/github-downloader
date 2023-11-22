import ast
from lm_dataformat import Reader
from datasets import Dataset


DATA_PATH = '/data/github_data'


def find_fn_defs(node):
    if not isinstance(node, ast.AST):
        return
    if isinstance(node, ast.FunctionDef):
        yield node
    if hasattr(node, 'body'):
        for n in node.body:
            yield from find_fn_defs(n)


def generator():
    reader = Reader(DATA_PATH)
    for example in reader.stream_data():
        # Try parsing Python code into an abstract syntax tree
        try:
            root = ast.parse(example)
        except:
            continue

        # Find all function definitions in the AST
        for fn_def in find_fn_defs(root):
            fn_string = ast.unparse(fn_def)
            signature, body = fn_string.split('\n', 1)
            yield {
                'signature': signature, 
                'body': body
            }


dataset = Dataset.from_generator(generator)
dataset.push_to_hub('LLM-PBE/github-python', private=True)


#####################
#   Sanity Check    #
#####################
# from datasets import load_dataset
# test = load_dataset('LLM-PBE/github-python')
# print(test)
# print(test['train'][0])
