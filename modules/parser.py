syntax_colors = {
    "keyword": "#cba6f7",  
    "builtin": "#89dceb", 
    "variable": "#cdd6f4",  
    "string": "#f5c2e7",  
    "comment": "#bac2de",  
    "number": "#f9e2af",  
    "operator": "#94e2d5", 
    "function": "#89b4fa", 
    "class": "#fab387",  
    "exception": "#f38ba8",  
    "decorator": "#b4befe",  
    "parameter": "#f5c2e7",  
    "import": "#cba6f7", 
    "docstring": "#f2cdcd",  
    "brace": "#6c7086",  
    "line_number": "#7f849c",  
    "default": "#f5e0dc"  
}
keywords = ["def", "class", "return", "if", "else", "elif", "for", "while", "try", "except", "break", "continue","True","False"]
built_in = ["print", "range", "sum", "len", "int", "str", "list","lambda","global","f"]


def divide_tokens(divided_code):
    dividers = ['"', "'", "(", ")", "[", "]", "{", "}", "#", "+", "=", "*", "/", "-", ",", "" ,#replace \t
                 "", #replace \n
                 " ", ":",";"]
    result = [[]]
    text = ""
    for i in divided_code:
        if i in dividers:
                if text:
                    result[len(result) - 1].append(text)
                    text = ""
                result[len(result) - 1].append(i)
        else:
                text += i



    if not result[-1]:
        result.pop()

    return result


def parse(code_list,offset):

    to_devide = ""
    for i in code_list:
        to_devide += i + ""

    lines = to_devide.split("")
    trimmed = "".join(line[offset[1]:offset[1]+53] for line in lines[offset[0]:offset[0]+27])

    tokens = divide_tokens(trimmed)
    context = {
        "is_comment": False,
        "in_double_string": False,
        "in_single_string": False,
    }
    result = []

    for line in tokens:
        for token in line:

            token = token.replace("","\t")
            token = token.replace("","\n") #not the same, be careful


            context['is_comment'] = token == "#" or context['is_comment'] and token != "\n"
            if token == '"'  and not context["in_single_string"]:
                context["in_double_string"] = not context["in_double_string"]
            elif token == "'" and not context["in_double_string"]:
                context["in_single_string"] = not context["in_single_string"]

                        

            if context['is_comment']:
                color = syntax_colors["comment"]
            elif context["in_double_string"] or context["in_single_string"]:
                color = syntax_colors["string"]
            elif token == "'" or token == '"':
                color = syntax_colors["string"]
            elif token in keywords:
                color = syntax_colors["keyword"]
            elif token in built_in:
                color = syntax_colors["builtin"]
            elif token.isdigit():
                color = syntax_colors["number"]
            elif token in {'+', '=', '-', '*', '/', '>', '<', ':', '(', ')', '{', '}', '[', ']'}:
                color = syntax_colors["operator"]
            else:
                color = syntax_colors["default"]
            
            result.append([token, color])

    return result

def hex_to_rgb(h): return tuple(int(h.lstrip("#")[i:i+2], 16)/255 for i in (0, 2, 4))

def format(data):
    result = ""

    for i in data:
        color = hex_to_rgb(i[1])
        result += f"<rgb({color[0]},{color[1]},{color[2]},255)>{i[0]}"

    return result