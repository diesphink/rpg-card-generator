#!/usr/bin/python3

import tomli
import re
import shutil
import os
import glob


def parse_text(text, break_lines=False):
    text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text)
    text = re.sub(r'^ - ', r'\\\\ \\faAngleRight ', text, flags=re.M)
    text = re.sub(r'\n\n', r'%\n\\\\[1mm]%\n', text)
    text = re.sub(r'\n$', '', text)
    if break_lines:
        text = re.sub(r'([^%])\n', r'\1\\\\', text)
    return text


def print_card(title, p, output):
    output.write(r"\card[")

    # Attributes
    for attribute in ["type", "time", "cost", "components", "fontsize"]:
        value = p.get(attribute, '')
        if value:
            output.write(f"{attribute}={value}, ")

    output.write("]")

    # Image
    output.write("{" + get_image(p) + "}")

    # Title
    output.write("{" + title + "}")
    output.write("\n")

    # Description
    output.write("{" + parse_text(p.get('description', '')) + "}")
    output.write("\n")

    # Footer
    output.write("{" + parse_text(p.get('footer', ''), True) + "}")
    output.write("%\n")


def print_token(title, p, output):
    output.write(r"\token[")

    # Attributes
    for attribute in ["type", "time", "cost", "components", "fontsize"]:
        value = p.get(attribute, '')
        if value:
            output.write(f"{attribute}={value}, ")

    output.write("]")

    # Image
    image = p.get('image', '')
    if image:
        images.append(image)
    output.write("{" + image + "}")

    # Title
    output.write("{" + title + "}")
    output.write("\n")

    # Description
    output.write("{" + parse_text(p.get('description', '')) + "}%")
    output.write("\n")


def print_image(p, output):
    output.write(r"\imagecard")

    # Image
    image = p.get('image', '')
    if image:
        images.append(image)
    output.write("{" + image + "}")

def get_image(p):
    image = p.get('image', '')
    if image:
        if image not in images:
            images.append(image)
        return image
    return ''


def print_back_card(title, p, output):
    output.write(r"\backcard")

    # Image
    images.append('images/back.png')

    # Color
    output.write("{" + p.get('color', '') + "}")

    # Title
    output.write("{" + title + "}%")
    output.write("\n")


def print_sheet(id, p, output):

    # início da carta, imagem de fundo e título acima
    output.write(r"""
\begin{tikzpicture}[x=1mm, y=1mm]

\tikzmath{\fs = \textsize + 0.5;}
    
% Parchment paper
\draw[fill=parchment] (0,0) rectangle (63,88);

% Imagem
\node[anchor=north west, inner sep=0,outer sep=0] (image) at (0, 88) {%
\includegraphics[width=63mm, height=88mm]{""" + get_image(p) + r"""}};
        
% Título
\node[title, anchor=north west, minimum width=59mm](title) at (2,86) {""" + parse_text(title) + r"};")

    # ATTRIBUTES
    output.write(r'''

% Atributos
''')
    attr_atual = 0
    attributes = p.get('attributes')
    pos_x = [2, 61]
    pos_y = [76.5, 68, 59.5]

    for attr, vl in attributes.items():
        if attr_atual < 3:
            output.write(r'\leftbox{' + str(pos_x[0]) + ',')
        else:
            output.write(r'\rightbox{' + str(pos_x[1]) + ',')
        output.write(str(pos_y[attr_atual % 3]))
        bonus = ("+" if vl[1] >= 0 else '') + str(vl[1])
        valor = str(vl[0])
        saving = ("+" if vl[2] >= 0 else '') + str(vl[2])

        output.write('}{' + attr + "}{" + bonus +
                     "}{" + valor + "}{" + saving + "}")
        output.write('\n')
        attr_atual += 1

    # BOXES
    output.write(r'''
% Boxes
''')
    box_atual = 0
    boxes = p.get('boxes')
    pos_x = [2, 12, 22, 33, 43, 53]
    pos_y = [52, 43]

    for name, vl in boxes.items():

        if box_atual < 6:
            x = pos_x[box_atual % 6]
            y = pos_y[0]
        else:
            x = pos_x[(box_atual % 6) + 2]
            y = pos_y[1]

        if isinstance(vl, list):
            output.write(r'\centerboxsubs[anchor=north west]{' + str(x) + ',' + str(
                y) + '}{' + name + '}{' + str(vl[0]) + '}{' + str(vl[1]) + '}')
        else:
            output.write(r'\centerbox[anchor=north west]{' + str(
                x) + ',' + str(y) + '}{' + name + '}{' + str(vl) + '}')

        output.write('\n')
        box_atual += 1

    # SKILLS
    skills = p.get('skills')
    output.write(r'''
% Skills
\node[fill=parchment, opacity=0.7, text opacity=1, draw opacity=1, inner sep=0mm, anchor=north west, font=\sffamily\fontsize{8}{8.5}, draw=black, rounded corners=0.4mm, fit={(2,43) (20,2)}] (SKILLS) {};
\node[tag, anchor=east] at ([xshift=-0.5mm] SKILLS.north east) {''' + skills.get('title', 'SKILLS') + r'''};
\node[anchor=west, align=left, text width=3mm, font=\sffamily\fontsize{5}{6}\selectfont] (skvalues) at (SKILLS.west) {%
''')

    values = skills.get('skills')
    profs = skills.get('profic')
    names = skills.get('names', ['Athletics', 'Acrobatics', 'Sleight of hand', 'Stealth', 'Arcana', 'History',
                                 'Investigation', 'Nature', 'Religion', 'Animal Handling', 'Insight', 'Medicine',
                                 'Perception', 'Survival', 'Deception', 'Intimidation', 'Performance', 'Persuasion'])

    for i in range(18):
        value = '+' + str(values[i])
        if profs[i]:
            value = '**' + value + '**'
        output.write(parse_text(value) + r'\\% ' + names[i] + '\n')
    output.write('};\n')
    output.write(r'''
\node[anchor=west, align=left, text width=13mm,font=\sffamily\fontsize{5}{6}\selectfont] (sknames) at ([xshift=3mm] SKILLS.west) {%
''')
    for i in range(18):
        name = names[i]
        if profs[i]:
            name = '**' + name + '**'
        output.write(parse_text(name) + '\\\\\n')
    output.write('};\n')

    # PROFICIENCIES
    proficiencies = p.get('proficiencies')
    output.write(r'''
% Proficiencies
\node[fill=parchment, opacity=0.7, text opacity=1, draw opacity=1, inner sep=0mm, anchor=north west, font=\sffamily\fontsize{8}{8.5}, draw=black, rounded corners=0.4mm, fit={(22,34) (61,22)}] (PROF) {};
\node[tag, anchor=east] at ([xshift=-0.5mm] PROF.north east) {''' + proficiencies.get('title', 'PROFICIENCIES') + r'''};
\node[anchor=west, align=left, text width=37mm, font=\sffamily\fontsize{4.5}{4.5}\selectfont] (feats) at (PROF.west) {%
''')

    lines = []
    for name, value in proficiencies.items():
        if name != 'title':
            lines.append('**' + name + ':** ' + value)
    output.write(parse_text((r'\\[0.7mm]' + '\n').join(lines)))
    output.write('};\n')

    # ATTACKS
    attacks = p.get('attacks')
    output.write(r'''
% Attacks
\node[fill=parchment, opacity=0.7, text opacity=1, draw opacity=1, inner sep=0mm, anchor=north west, font=\sffamily\fontsize{8}{8.5}, draw=black, rounded corners=0.4mm, fit={(22,20) (61,2)}] (ATTACKS) {};
\node[tag, anchor=east] at ([xshift=-0.5mm] ATTACKS.north east) {''' + attacks.get('title', 'ATTACKS') + r'''};
\node[anchor=west, align=right, xshift=1mm, inner sep=0, font=\sffamily\fontsize{4.5}{6}\selectfont] (atts) at (ATTACKS.west) {%
''')

    names = []
    values = []
    for name, value in attacks.items():
        if name != 'title':
            names.append('**' + name + ':**')
            values.append(value)
    output.write(parse_text((r'\\' + '\n').join(names)))
    output.write('};\n')

    output.write(r'''
\node[anchor=west, align=left, text width=30mm, inner sep=0, xshift=0.5mm, font=\sffamily\fontsize{4.5}{6}\selectfont] (atts2) at (atts.east) {%
''')
    output.write(parse_text((r'\\' + '\n').join(values)))
    output.write('};\n')

    output.write(r'''

% Borda
\draw[line width = 0.5mm, black] (0,0) rectangle (63,88);

\end{tikzpicture}%
''')

def print_inventory(title, p, output):

    output.write(r"""%
\begin{tikzpicture}[x=1mm, y=1mm]
\tikzmath{\fs = \textsize + 0.5;}

% Parchment paper
\draw[fill=parchment] (0,0) rectangle (63,88);

% Imagem
\node[anchor=north west, inner sep=0,outer sep=0] (image) at (0, 88) {\includegraphics[width=63mm, height=88mm]{""" + get_image(p) + r"""}};

% Título
\node[title, anchor=north west, minimum width=59mm](title) at (2,86) {""" + parse_text(title) + r"""};
\node[fill=parchment, opacity=0.8, text opacity=1, draw opacity=1, inner sep=0mm, anchor=north west, font=\sffamily\fontsize{8}{8.5}, draw=black, rounded corners=0.4mm, fit={(2,80) (51,2)}] (ITEMS) {};

\centerbox[anchor=north east]{61, 80}{COPP}{}
\centerbox[anchor=north east]{61, 72}{SILV}{}
\centerbox[anchor=north east, minimum height=3.8cm, text depth=3.2cm]{61, 64}{GOLD}{""" + str(p.get('consumables').get('GP', '')) + r"""}
\centerbox[anchor=north east, minimum height=2.2cm, text depth=1.6cm]{61, 24}{GEMS}{}
%\centerbox[anchor=north east]{61, 24}{PLAT}{}
%\centerbox[anchor=north east]{61, 16}{RATION}{}
%\centerbox[anchor=north east]{61, 8}{HEAL PT}{} 

\node[anchor=north west, align=left, text width=45mm, inner sep=2mm, font=\sffamily\fontsize{5}{6}\selectfont] (skvalues) at (ITEMS.north west) {
""")

    blocks = []
    for name, value in p.items():
        if name in ['inventory', 'title', 'image', 'consumables']:
            continue
        lines = []
        lines.append(parse_text('**' + name + '**'))
        for line in value.splitlines():
            lines.append(r'\faIcon[regular]{square}' + parse_text(line))
        blocks.append((r'\\' + '\n').join(lines))

    lines = []
    lines.append(parse_text('**Consumables**'))
    for name, value in p.get('consumables').items():
        if name in ['CP', 'SP', 'GP', 'PP']:
            continue
        lines.append(name + ' ' + (''.join([r'\faIcon[regular]{square}\hspace{-0.8mm}' for i in range(value)])))
    blocks.append((r'\\' + '\n').join(lines))


    output.write((r'\\[1mm]' + '\n').join(blocks))
     
    output.write('};')

    
    output.write(r"""

% Borda
\draw[line width = 0.5mm, black] (0,0) rectangle (63,88);

\end{tikzpicture}%
""")

def include(include_file, output):
    output.write(f"\n\n% {include_file}\n")
    with open(include_file, 'r') as lib1:
        for line in lib1:
            output.write(line)

images = []

shutil.rmtree('output', ignore_errors=True)
os.makedirs('output/images')

for config_file in glob.glob("input/*.toml"):

    with open(config_file, mode="rb") as fp:
        cards = tomli.load(fp)

    outputfile = "output/" + \
        os.path.splitext(os.path.basename(config_file))[0] + ".tex"
    with open(outputfile, mode="w") as output:

        output.write(r'\documentclass{article}')

        for include_file in sorted(glob.glob('includes/*.tex')):
            include(include_file, output)

        output.write(r'\begin{document}\begin{center}')

        for title, p in cards.items():

            title = p.get('title', title)

            output.write(f"""%
% {''.join(['=' for char in title])}
% {title}
% {''.join(['=' for char in title])}
""")

            count = int(p.get('count', 1))

            for i in range(0, count):

                if p.get('token', False):
                    print_token(title, p, output)
                elif p.get('back', False):
                    print_back_card(title, p, output)
                elif p.get('sheet', False):
                    print_sheet(title, p, output)
                elif p.get('inventory', False):
                    print_inventory(title, p, output)
                elif p.get('include', None) is not None:
                    include(p.get('include'), output)
                elif p.get('description', None) is None:
                    print_image(p, output)
                else:
                    print_card(title, p, output)

        output.write(r"\end{center}\end{document}")




    for image in images:
        if os.path.isfile(image):
            shutil.copy(image, f'output/{image}')
        for ext in [".png", ".jpeg", ".jpg"]:
            if os.path.isfile(image + ext):
                shutil.copy(image + ext, f'output/{image + ext}')

    # with zipfile.ZipFile('output.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
    #     for dirname, subdirs, files in os.walk("output"):
    #         zf.write(dirname)
    #         for filename in files:
    #             zf.write(os.path.join(dirname, filename))
