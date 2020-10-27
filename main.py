from PIL import Image, ImageDraw, ImageColor, ImageFont
import random


if __name__ == '__main__':
    shapes = ['circle', 'square', 'triangle', 'ellipse']
    colors = ['black', 'royalblue', 'brown', 'cyan', 'gray', 'red', 'purple', 'pink', 'gold', 'orange', 'teal',
              'green', 'darkcyan']

    im = Image.new('RGB', (800, 600), ImageColor.getrgb('white'))
    text_font = ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf', 22)
    head_font = ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf', 32)
    draw = ImageDraw.Draw(im)
    head_txt = 'Pattern Matching'
    # number of images generated
    n = 1
    for num in range(0, n):
        # each color and shape are randomly picked from colors and shapes list.
        color1 = colors[random.randint(0, (len(colors)-1))]
        color2 = colors[random.randint(0, (len(colors)-1))]
        color3 = colors[random.randint(0, (len(colors)-1))]
        color4 = colors[random.randint(0, (len(colors)-1))]
        shape1 = shapes[random.randint(0, (len(shapes)-1))]
        shape2 = shapes[random.randint(0, (len(shapes)-1))]

        example_text = 'Example Text: Consider the following sequence: {color1} {shape1}, {color1} {shape1},\n'\
                       '{color2} {shape2}, {color1} {shape1}, {color2} {shape2}, {color2} ' \
                       '{shape2}. '.format(color1=color1, color2=color2, shape1=shape1, shape2=shape2)
        example_question = 'Example Question: Based on the given diagram, what would the new sequence \nbe?'
        example_answer = 'Example Answer: \n{color3} {shape3}, {color3} {shape3}, \n{color4} {shape4}, '\
                         '{color3} {shape3}, \n{color4} {shape4}, {color4} ' \
                         '{shape4}. '.format(color3=color3, color4=color4, shape3=shape1, shape4=shape2)
        draw.text((5, 5), head_txt, fill='dimgrey', font=head_font)
        draw.text((5, 50), example_text, fill='dimgray', font=text_font)
        draw.text((5, 130), example_question, fill='dimgray', font=text_font)
        draw.text((5, 200), example_answer, fill='dimgray', font=text_font)

        # two arrows
        draw.line((510, 250, 630, 250), fill='black', width=5)
        draw.polygon([(620, 260), (620, 240), (640, 250)], fill='black')
        draw.line((510, 400, 630, 400), fill='black', width=5)
        draw.polygon([(620, 410), (620, 390), (640, 400)], fill='black')
        # 'circle', 'square', 'triangle', 'ellipse'
        if shape1 == 'circle':
            draw.ellipse((400, 200, 500, 300), fill=color1)
            draw.ellipse((650, 200, 750, 300), fill=color3)
        elif shape1 == 'square':
            draw.rectangle((400, 200, 500, 300), fill=color1)
            draw.rectangle((650, 200, 750, 300), fill=color3)
        elif shape1 == 'ellipse':
            draw.ellipse((425, 200, 475, 300), fill=color1)
            draw.ellipse((675, 200, 725, 300), fill=color3)
        else:
            draw.polygon([(400, 300), (500, 300), (450, 200)], fill=color1)
            draw.polygon([(650, 300), (750, 300), (700, 200)], fill=color3)

        if shape2 == 'square':
            draw.rectangle((400, 350, 500, 450), fill=color2)
            draw.rectangle((650, 350, 750, 450), fill=color4)
        elif shape2 == 'circle':
            draw.ellipse((400, 350, 500, 450), fill=color2)
            draw.ellipse((650, 350, 750, 450), fill=color4)
        elif shape2 == 'ellipse':
            draw.ellipse((425, 350, 475, 450), fill=color2)
            draw.ellipse((675, 350, 725, 450), fill=color4)
        else:
            draw.polygon([(400, 450), (500, 450), (450, 350)], fill=color2)
            draw.polygon([(650, 450), (750, 450), (700, 350)], fill=color4)
        file_path = 'C:/Users/galen/PycharmProjects/patternMatch/venv/images/pattern-match{number}.jpg'.format(number=num)
        im.save(file_path, quality=95)
    im.show()
