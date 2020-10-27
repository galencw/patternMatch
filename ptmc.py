from PIL import Image, ImageDraw, ImageColor, ImageFont
from functools import reduce
import random


########################################################################################################################
# MATH
# converts the list to a function that generates a random element from the list each time it is called
def list_to_random_generator(list_arg):
    return lambda: list_arg[random.randrange(0, len(list_arg))]


# recursive version of generate_list
def generate_list_rec(generator, size, list_arg):
    return generate_list_rec(generator, size - 1, list_arg + [generator()]) if size > 0 else list_arg


# generates a list of the given size, populating it with the values returned by the given generator
def generate_list(generator, size):
    return generate_list_rec(generator, size, [])


########################################################################################################################
########################################################################################################################
# COLORS
def get_colors():
    return ["black", "royalblue", "brown", "cyan", "gray", "red", "purple",
            "pink", "gold", "orange", "teal", "green", "darkcyan"]


def get_random_color():
    return list_to_random_generator(get_colors())()


def get_random_colors(size):
    return generate_list(get_random_color, size)


def get_color_for_pretty_printing(color):
    try:
        return {"royalblue": "royal blue", "darkcyan": "dark cyan"}[color]
    except KeyError:
        return color


########################################################################################################################
########################################################################################################################
# SHAPES
# returns the list of shapes used for question generation
def get_shapes():
    return ['circle', 'square', 'triangle', 'ellipse']


def get_random_shape():
    return list_to_random_generator(get_shapes())()


def get_random_shapes(size):
    return generate_list(get_random_shape, size)


########################################################################################################################
########################################################################################################################
# DRAW
def draw_header(draw):
    draw.text((5, 5), "Pattern Matching", fill="dimgrey", font=get_header_font())


def draw_question(draw):
    draw.text((5, 130), "Based on the given diagram, what would the new sequence be?", fill="dimgrey",
              font=get_body_font())


def draw_line(draw, y):
    draw.line((510, y, 630, y), fill="black", width=5)


def draw_arrowhead(draw, y):
    draw.polygon([(620, y + 20), (620, y), (640, y + 10)], fill="black")


def draw_arrow(draw, y):
    draw_line(draw, y + 10)
    draw_arrowhead(draw, y)


def draw_arrows_rec(draw, amount, y):
    if amount > 0:
        draw_arrow(draw, y)
        draw_arrows_rec(draw, amount - 1, y + 150)


def draw_arrows(draw):
    draw_arrows_rec(draw, 2, 250)


def draw_circle(draw, color, x, y):
    draw.ellipse((x, y, x + 100, y + 100), fill=color)


def draw_square(draw, color, x, y):
    draw.rectangle((x, y, x + 100, y + 100), fill=color)


def draw_ellipse(draw, color, x, y):
    draw.ellipse((x + 25, y, x + 75, y + 100), fill=color)


def draw_triangle(draw, color, x, y):
    draw.polygon([(x, y + 100), (x + 100, y + 100), (x + 50, y)], fill=color)


# maps the name to the appropriate draw function
def draw_shape(draw, name, color, x, y):
    {"circle": draw_circle, "square": draw_square,
     "ellipse": draw_ellipse, "triangle": draw_triangle}[name](draw, color, x, y)


def draw_shapes(draw, shapes, x):
    if len(shapes) > 0:
        draw_shape(draw, shapes[0][2], shapes[0][1], x, 200 + shapes[0][0] * 150)
        draw_shapes(draw, shapes[1:], x)


def draw_text_and_answer(draw, input_sequence, output_shapes):
    draw.text((5, 50), get_text(input_sequence), fill='dimgray', font=get_body_font())
    draw.text((5, 200), get_answer(generate_output_sequence(input_sequence, output_shapes)), fill='dimgray',
              font=get_body_font())


def draw_shapes_text_and_answer(draw, input_shapes, output_shapes):
    draw_shapes(draw, input_shapes, 400)
    draw_shapes(draw, output_shapes, 650)
    draw_text_and_answer(draw, generate_input_sequence(input_shapes), output_shapes)


def draw_all(draw):
    draw_header(draw)
    draw_question(draw)
    draw_arrows(draw)
    draw_shapes_text_and_answer(draw, generate_shapes(), generate_shapes())


########################################################################################################################
########################################################################################################################
# STRINGS
def interject(string, interjection, index, gap=0):
    return string[:index] + interjection + string[index + gap:]


def truncate_at_last_comma(string):
    return string[:string.rindex(",")]


# finds the index of the nth occurrence of elem in string
def elem_index_to_string_index(string, elem, elem_index):
    def string_indexer_rec(string_index, elem_index_rec):
        return string_indexer_rec(string.index(elem, string_index + 1), elem_index_rec - 1) \
            if elem_index_rec >= 0 else string_index

    return string_indexer_rec(-1, elem_index)


def get_index_of_second_comma(string):
    return elem_index_to_string_index(string, ",", 1) + 1


def newline_after_second_comma(string):
    return interject(string, "\n", get_index_of_second_comma(string), gap=1)


def get_text(input_sequence):
    # reduces the input sequence to a comma-separated string
    # elem[1] -> color, elem[2] -> name
    def reducer(answer, elem):
        return answer + get_color_for_pretty_printing(elem[1]) + " " + elem[2] + ", "

    # applies the reducer
    def get_reduction():
        return reduce(reducer, input_sequence, "Consider the following sequence: ")

    return truncate_at_last_comma(newline_after_second_comma(get_reduction()))


def get_answer(output_sequence):
    # elem[0] -> index
    def space_when_index_is_even_else_newline(elem):
        return " " if elem[0] % 2 == 0 else "\n"

    # elem[1][1] -> color
    # elem[1][2] -> shape
    def elem_to_string(elem):
        return get_color_for_pretty_printing(elem[1][1]) + " " + elem[1][2] + "," + \
               space_when_index_is_even_else_newline(elem)

    return truncate_at_last_comma(reduce(lambda answer, elem: answer + elem_to_string(elem),
                                         enumerate(output_sequence), ""))


########################################################################################################################
# FONTS
def get_arial_font(size):
    return ImageFont.truetype("arial.ttf", size)


def get_header_font():
    return get_arial_font(32)


def get_body_font():
    return get_arial_font(22)


########################################################################################################################
########################################################################################################################
# SEQUENCES
# generates a list of three-tuples, where each tuple includes an index, color, and name
def generate_shapes():
    return list(zip(range(0, 2), get_random_colors(2), get_random_shapes(2)))


# generates a list of shapes, then creates a random sequence of these shapes
def generate_input_sequence(input_shapes):
    return generate_list(list_to_random_generator(input_shapes), 6)


# generates a list of shapes, then creates a sequence of these shapes based on the provided input sequence
# shapes are mapped by index (the index generated in generate_shape_list)
def generate_output_sequence(input_sequence, output_shapes):
    return reduce(lambda answer, elem: answer + [output_shapes[elem[0]]], input_sequence, [])


########################################################################################################################
########################################################################################################################
# IMAGE
def get_new_image():
    return Image.new('RGB', (800, 600), ImageColor.getrgb('white'))


def get_draw(image):
    return ImageDraw.Draw(image)


def draw_on_image(image):
    draw_all(get_draw(image))
    return image


def draw_images_rec(index, amount):
    if index < amount:
        draw_on_image(get_new_image()).save("Pattern_Matching_" + str(index) + ".jpg")
        draw_images_rec(index + 1, amount)


def draw_images(amount):
    draw_images_rec(0, amount)


########################################################################################################################
########################################################################################################################
# MAIN
# hey look, the whole program's a monad!
def main():
    draw_images(1)


########################################################################################################################
main()
