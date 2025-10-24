#!/usr/bin/env python3

import tomli
import re
import shutil
import os
import glob


def parse_text(text, break_lines=False):
    text = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", text)
    text = re.sub(r"\[g\](.+?)\[g\]", r"\\textcolor{green}{\1}", text)
    text = re.sub(r"^ - ", r"\\\\ \\faAngleRight ", text, flags=re.M)
    text = re.sub(r"\n\n", r"%\n\\\\[1mm]%\n", text)
    text = re.sub(r"\n$", "", text)
    if break_lines:
        text = re.sub(r"([^%])\n", r"\1\\\\", text)
    return text


def print_card(title, p, output):
    output.write(r"\card[")

    # Attributes
    for attribute in ["type", "time", "cost", "components", "fontsize"]:
        value = p.get(attribute, "")
        if value:
            output.write(f"{attribute}={value}, ")

    output.write("]")

    # Image
    output.write("{" + get_image(p) + "}")

    # Title
    output.write("{" + title + "}")
    output.write("\n")

    # Description
    output.write("{" + parse_text(p.get("description", "")) + "}")
    output.write("\n")

    # Footer
    output.write("{" + parse_text(p.get("footer", ""), True) + "}")
    output.write("%\n")


def print_token(title, p, output):
    output.write(r"\token[")

    # Attributes
    for attribute in ["type", "time", "cost", "components", "fontsize"]:
        value = p.get(attribute, "")
        if value:
            output.write(f"{attribute}={value}, ")

    output.write("]")

    # Image
    image = p.get("image", "")
    if image:
        images.append(image)
    output.write("{" + image + "}")

    # Title
    output.write("{" + title + "}")
    output.write("\n")

    # Description
    output.write("{" + parse_text(p.get("description", "")) + "}%")
    output.write("\n")


def print_image(p, output):
    output.write(r"\imagecard")

    # Image
    image = p.get("image", "")
    if image:
        images.append(image)
    output.write("{" + image + "}")


def get_image(p):
    image = p.get("image", "")
    if image:
        if image not in images:
            images.append(image)
        return image
    return ""


def print_back_card(title, p, output):
    output.write(r"\backcard")

    # Image
    images.append("images/back.png")

    # Color
    output.write("{" + p.get("color", "") + "}")

    # Title
    output.write("{" + title + "}%")
    output.write("\n")


def print_sheet(id, p, output):

    # início da carta, imagem de fundo e título acima
    output.write(
        r"""%
\begin{tikzpicture}[x=1mm, y=1mm]

\tikzmath{\fs = \textsize + 0.5;}
    
% Parchment paper
\draw[fill=parchment] (0,0) rectangle (63,88);

% Imagem
\node[anchor=north west, inner sep=0,outer sep=0] (image) at (0, 88) {%
\includegraphics[width=63mm, height=88mm]{"""
        + get_image(p)
        + r"""}};
        
% Título
\node[title, anchor=north west, minimum width=59mm](title) at (2,86) {"""
        + parse_text(title)
        + r"};"
    )

    # ATTRIBUTES
    output.write(
        r"""

% Atributos
"""
    )
    attr_atual = 0
    attributes = p.get("attributes")
    pos_x = [2, 61]
    pos_y = [76.5, 68, 59.5]

    for attr, vl in attributes.items():
        if attr_atual < 3:
            output.write(r"\leftbox{" + str(pos_x[0]) + ",")
        else:
            output.write(r"\rightbox{" + str(pos_x[1]) + ",")
        output.write(str(pos_y[attr_atual % 3]))
        bonus = ("+" if vl[1] >= 0 else "") + str(vl[1])
        valor = str(vl[0])
        saving = ("+" if vl[2] >= 0 else "") + str(vl[2])

        output.write("}{" + attr + "}{" + bonus + "}{" + valor + "}{" + saving + "}")
        output.write("\n")
        attr_atual += 1

    # BOXES
    output.write(
        r"""
% Boxes
"""
    )
    box_atual = 0
    boxes = p.get("boxes")
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
            output.write(
                r"\centerboxsubs[anchor=north west]{"
                + str(x)
                + ","
                + str(y)
                + "}{"
                + name
                + "}{"
                + str(vl[0])
                + "}{"
                + str(vl[1])
                + "}"
            )
        else:
            output.write(
                r"\centerbox[anchor=north west]{"
                + str(x)
                + ","
                + str(y)
                + "}{"
                + name
                + "}{"
                + str(vl)
                + "}"
            )

        output.write("\n")
        box_atual += 1

    # SKILLS
    skills = p.get("skills")
    output.write(
        r"""
% Skills
\node[fill=parchment, opacity=0.7, text opacity=1, draw opacity=1, inner sep=0mm, anchor=north west, font=\sffamily\fontsize{8}{8.5}, draw=black, rounded corners=0.4mm, fit={(2,43) (20,2)}] (SKILLS) {};
\node[tag, anchor=east] at ([xshift=-0.5mm] SKILLS.north east) {"""
        + skills.get("title", "SKILLS")
        + r"""};
\node[anchor=west, align=left, text width=3mm, font=\sffamily\fontsize{5}{6}\selectfont] (skvalues) at (SKILLS.west) {%
"""
    )

    values = skills.get("skills")
    profs = skills.get("profic")
    names = skills.get(
        "names",
        [
            "Athletics",
            "Acrobatics",
            "Sleight of hand",
            "Stealth",
            "Arcana",
            "History",
            "Investigation",
            "Nature",
            "Religion",
            "Animal Handling",
            "Insight",
            "Medicine",
            "Perception",
            "Survival",
            "Deception",
            "Intimidation",
            "Performance",
            "Persuasion",
        ],
    )

    for i in range(18):
        value = ("+" if values[i] >= 0 else "−") + str(abs(values[i]))
        if profs[i]:
            value = "**" + value + "**"
        output.write(parse_text(value) + r"\\% " + names[i] + "\n")
    output.write("};\n")
    output.write(
        r"""
\node[anchor=west, align=left, text width=13mm,font=\sffamily\fontsize{5}{6}\selectfont] (sknames) at ([xshift=3mm] SKILLS.west) {%
"""
    )
    for i in range(18):
        name = names[i]
        if profs[i]:
            name = "**" + name + "**"
        output.write(parse_text(name) + "\\\\\n")
    output.write("};\n")

    # PROFICIENCIES
    proficiencies = p.get("proficiencies")
    output.write(
        r"""
% Proficiencies
\node[fill=parchment, opacity=0.7, text opacity=1, draw opacity=1, inner sep=0mm, anchor=north west, font=\sffamily\fontsize{8}{8.5}, draw=black, rounded corners=0.4mm, fit={(22,34) (61,22)}] (PROF) {};
\node[tag, anchor=east] at ([xshift=-0.5mm] PROF.north east) {"""
        + proficiencies.get("title", "PROFICIENCIES")
        + r"""};
\node[anchor=west, align=left, text width=37mm, font=\sffamily\fontsize{4.5}{4.5}\selectfont] (feats) at (PROF.west) {%
"""
    )

    lines = []
    for name, value in proficiencies.items():
        if name != "title":
            lines.append("**" + name + ":** " + value)
    output.write(parse_text((r"\\[0.7mm]" + "\n").join(lines)))
    output.write("};\n")

    # ATTACKS
    attacks = p.get("attacks")
    output.write(
        r"""
% Attacks
\node[fill=parchment, opacity=0.7, text opacity=1, draw opacity=1, inner sep=0mm, anchor=north west, font=\sffamily\fontsize{8}{8.5}, draw=black, rounded corners=0.4mm, fit={(22,20) (61,2)}] (ATTACKS) {};
\node[tag, anchor=east] at ([xshift=-0.5mm] ATTACKS.north east) {"""
        + attacks.get("title", "ATTACKS")
        + r"""};
\node[anchor=west, align=right, xshift=1mm, inner sep=0, font=\sffamily\fontsize{4.5}{6}\selectfont] (atts) at (ATTACKS.west) {%
"""
    )

    names = []
    values = []
    for name, value in attacks.items():
        if name != "title":
            names.append("**" + name + ":**")
            values.append(value)
    output.write(parse_text((r"\\" + "\n").join(names)))
    output.write("};\n")

    output.write(
        r"""
\node[anchor=west, align=left, text width=30mm, inner sep=0, xshift=0.5mm, font=\sffamily\fontsize{4.5}{6}\selectfont] (atts2) at (atts.east) {%
"""
    )
    output.write(parse_text((r"\\" + "\n").join(values)))
    output.write("};\n")

    output.write(
        r"""

% Borda
\draw[line width = 0.5mm, black] (0,0) rectangle (63,88);

\end{tikzpicture}%
"""
    )


def print_inventory(title, p, output):

    output.write(
        r"""%
\begin{tikzpicture}[x=1mm, y=1mm]
\tikzmath{\fs = \textsize + 0.5;}

% Parchment paper
\draw[fill=parchment] (0,0) rectangle (63,88);

% Imagem
\node[anchor=north west, inner sep=0,outer sep=0] (image) at (0, 88) {\includegraphics[width=63mm, height=88mm]{"""
        + get_image(p)
        + r"""}};

% Título
\node[title, anchor=north west, minimum width=59mm](title) at (2,86) {"""
        + parse_text(title)
        + r"""};
\node[fill=parchment, opacity=0.8, text opacity=1, draw opacity=1, inner sep=0mm, anchor=north west, font=\sffamily\fontsize{8}{8.5}, draw=black, rounded corners=0.4mm, fit={(2,80) (51,2)}] (ITEMS) {};

\centerbox[anchor=north east, minimum height=1.4cm, text depth=0.8cm]{61, 80}{XP}{"""
        + str(p.get("consumables").get("XP", ""))
        + r"""}
\centerbox[anchor=north east, minimum height=3.8cm, text depth=3.2cm]{61, 64}{GOLD}{"""
        + str(p.get("consumables").get("GP", ""))
        + r"""}
\centerbox[anchor=north east, minimum height=2.2cm, text depth=1.6cm]{61, 24}{GEMS}{}
%\centerbox[anchor=north east]{61, 24}{PLAT}{}
%\centerbox[anchor=north east]{61, 16}{RATION}{}
%\centerbox[anchor=north east]{61, 8}{HEAL PT}{} 

\node[anchor=north west, align=left, text width=46mm, inner sep=2mm, font=\sffamily\fontsize{5}{6}\selectfont] (skvalues) at (ITEMS.north west) {
"""
    )

    blocks = []
    for name, value in p.items():
        if name in ["inventory", "title", "image", "consumables"]:
            continue
        lines = []
        columns = 1
        if name.startswith("2c."):
            name = name[3:]
            columns = 2
        if name.startswith("3c."):
            name = name[3:]
            columns = 3
        i = 0
        lines.append(parse_text("**" + name + "**"))

        line = ""
        for value_line in value.splitlines():
            line += r"\faIcon[regular]{square}" + parse_text(value_line)
            i += 1

            if i == columns:
                i = 0
                lines.append(line)
                line = ""
            else:
                line += r"\tabto{" + str(46 * i / columns) + "mm}\n"
        if line != "":
            lines.append(line)
        blocks.append((r"\\" + "\n").join(lines))

    lines = []
    lines.append(parse_text("**Consumables**"))
    for name, value in p.get("consumables").items():
        if name in ["CP", "SP", "GP", "PP", "XP"]:
            continue
        lines.append(
            name
            + "\\tabto{2cm} "
            + (
                "".join(
                    [r"\faIcon[regular]{square}\hspace{-0.8mm}" for i in range(value)]
                )
            )
        )
    blocks.append((r"\\" + "\n").join(lines))

    output.write((r"\\[1mm]" + "\n").join(blocks))

    output.write("};")

    output.write(
        r"""

% Borda
\draw[line width = 0.5mm, black] (0,0) rectangle (63,88);

\end{tikzpicture}%
"""
    )


def include(include_file, output):
    output.write(f"%\n%\n% {include_file}\n")
    with open(include_file, "r") as lib1:
        for line in lib1:
            output.write(line)


def print_creature(title, p, output):
    # \pet[type=Tiny Beast, ac=11, hp=1, speed=60, speedm=180, prof=+2, perc=10, str=3, dex=13, con=8, int=2, wis=12, cha=7, strb=-4, dexb=+1,
    # conb=-1, intb=-4, wisb=+1, chab=-2]{images/card-buma}{Buma}
    # {Perception +3\\Stealth +3}
    # {%
    # \textbf{Senses}\\
    # Darkvision 120ft
    # \\[1mm]
    # \textbf{Flyby}\\
    # Buma doesn't provoke opportunity attacks when it flies out of an enemy's reach.
    # \\[1mm]
    # \textbf{Keen Hearing and Sight}\\
    # Buma has advantage on Wisdom (Perception) checks that rely on hearing or sight.
    # }%

    # início da carta, imagem de fundo e título acima
    output.write(r"\begin{tikzpicture}[x=1mm, y=1mm]")

    fontsize = p.get("fontsize", 6)
    type = p.get("type", "Wild Shape").upper()

    output.write(
        r"""
% Parchment paper
\draw[fill=parchment] (0,0) rectangle (\cardwidth,\cardheight);


% Imagem
\node[anchor=north west, inner sep=0,outer sep=0] (back) at (0, 63) {\includegraphics[width=41mm]{"""
        + get_image(p)
        + r"""}};

% Parchment paper
\draw[fill=parchment] (0, 0) rectangle (\cardwidth,20);

% Título
\node[title, anchor=north west](title) at (2,61) {\textbf{"""
        + parse_text(title)
        + "}};\n"
    )

    # Atributos
    pos_x = [2, 39.5]
    pos_y = [51.5, 43, 34.5]
    attrs = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
    for index, attr in enumerate(attrs):
        if p.get(attr, None) is not None:
            vl = p.get(attr)
            if index < 3:
                output.write(r"\leftbox{" + str(pos_x[0]) + ",")
            else:
                output.write(r"\rightbox{" + str(pos_x[1]) + ",")
            output.write(str(pos_y[index % 3]))

            bonus = ("+" if vl[1] >= 0 else "") + str(vl[1])
            valor = str(vl[0])
            saving = ("+" if vl[2] >= 0 else "") + str(vl[2])

            output.write(
                "}{" + attr + "}{" + bonus + "}{" + valor + "}{" + saving + "}"
            )
            output.write("\n")

    output.write(
        r"""

    % Texto
    \node[fill=parchment, inner sep=2mm, outer sep=0, font=\sffamily\fontsize{"""
        + str(fontsize)
        + """}{"""
        + str(fontsize * 0.5)
        + """}\selectfont, text width=37mm, anchor=north west, align=justify] (text) at (0, 29.5) {"""
        + parse_text(p.get("description", ""))
        + r"""};

    % Separador
    \draw [line width = 0.5mm] ([yshift=0.25mm] text.north west) -- ([yshift=0.25mm] text.north east);

    \coordinate (tagpos) at (39,3);

    % Type
    \node[tag](type) at (39, 29.5) {"""
        + type
        + """};

    % Borda
    \draw[line width = 0.5mm, black] (0,0) rectangle (\cardwidth,\cardheight);

    """
    )

    output.write("\end{tikzpicture}{}%\n")


#     # ATTRIBUTES
#     output.write(
#         r"""

# % Atributos
# """
#     )
#     attr_atual = 0
#     attributes = p.get("attributes")
#     pos_x = [2, 61]
#     pos_y = [76.5, 68, 59.5]

#     for attr, vl in attributes.items():
#         if attr_atual < 3:
#             output.write(r"\leftbox{" + str(pos_x[0]) + ",")
#         else:
#             output.write(r"\rightbox{" + str(pos_x[1]) + ",")
#         output.write(str(pos_y[attr_atual % 3]))
#         bonus = ("+" if vl[1] >= 0 else "") + str(vl[1])
#         valor = str(vl[0])
#         saving = ("+" if vl[2] >= 0 else "") + str(vl[2])

#         output.write("}{" + attr + "}{" + bonus + "}{" + valor + "}{" + saving + "}")
#         output.write("\n")
#         attr_atual += 1

#     # BOXES
#     output.write(
#         r"""
# % Boxes
# """
#     )
#     box_atual = 0
#     boxes = p.get("boxes")
#     pos_x = [2, 12, 22, 33, 43, 53]
#     pos_y = [52, 43]

#     for name, vl in boxes.items():

#         if box_atual < 6:
#             x = pos_x[box_atual % 6]
#             y = pos_y[0]
#         else:
#             x = pos_x[(box_atual % 6) + 2]
#             y = pos_y[1]

#         if isinstance(vl, list):
#             output.write(
#                 r"\centerboxsubs[anchor=north west]{"
#                 + str(x)
#                 + ","
#                 + str(y)
#                 + "}{"
#                 + name
#                 + "}{"
#                 + str(vl[0])
#                 + "}{"
#                 + str(vl[1])
#                 + "}"
#             )
#         else:
#             output.write(
#                 r"\centerbox[anchor=north west]{"
#                 + str(x)
#                 + ","
#                 + str(y)
#                 + "}{"
#                 + name
#                 + "}{"
#                 + str(vl)
#                 + "}"
#             )

#         output.write("\n")
#         box_atual += 1

#     # SKILLS
#     skills = p.get("skills")
#     output.write(
#         r"""

#     % Stats
#     \centerbox[anchor=north west, minimum height=6mm, minimum width=6mm]{1.5, 55}{AC}{\ac}
#     \centerbox[anchor=north west, minimum height=6mm, minimum width=6mm]{9.5, 55}{HP}{\hp}
#     \centerbox[anchor=north west, minimum height=6mm, minimum width=6mm]{17.5, 55}{SPEED}{\speed}
#     \centerbox[anchor=north west, minimum height=6mm, minimum width=6mm]{25.5, 55}{PROF}{\prof}
#     \centerbox[anchor=north west, minimum height=6mm, minimum width=6mm]{33.5, 55}{PERC}{\perc}

#     % Atributos
#     \node[fill=parchment, opacity=0.7, text opacity=1, draw opacity=1, inner sep=0mm, anchor=north west, font=\sffamily\fontsize{8}{8.5}, draw=black, rounded corners=0.4mm, fit={(1.5,28) (15.5,12)}] (ATTRS) {};

#     \node[tag, anchor=east] at ([xshift=-0.5mm] ATTRS.north east) {ATTRS};

#     \node[anchor=west, align=left, text width=3mm, font=\sffamily\fontsize{5}{6}\selectfont] (att) at (ATTRS.west) {%
#     \textbf{STR}\\
#     \textbf{DEX}\\
#     \textbf{CON}\\
#     \textbf{INT}\\
#     \textbf{WIS}\\
#     \textbf{CHA}
#     };
#     \node[anchor=west, align=right, minimum width=4mm, font=\sffamily\fontsize{5}{6}\selectfont] (att2) at (att.east) {%
#     \str\\
#     \dex\\
#     \con\\
#     \int\\
#     \wis\\
#     \cha
#     };
#     \node[anchor=west, align=center, font=\sffamily\fontsize{5}{6}\selectfont] (att3) at ([xshift=2.5mm] att.east) {%
#     (\strb)\\
#     (\dexb)\\
#     (\conb)\\
#     (\intb)\\
#     (\wisb)\\
#     (\chab)
#     };


#     % SKILLS
#     \node[fill=parchment, opacity=0.7, text opacity=1, draw opacity=1, inner sep=0mm, anchor=north west, font=\sffamily\fontsize{8}{8.5}, draw=black, rounded corners=0.4mm, fit={(1.5, 10) (15.5, 2)}] (SKILLS) {};

#     \node[tag, anchor=east] at ([xshift=-0.5mm] SKILLS.north east) {SKILLS};

#     \node[anchor=west, align=left, text width=14mm, font=\sffamily\fontsize{4}{4.5}\selectfont] (sk) at (SKILLS.west) {%
#     #4
#     };

#     % ABILITIES
#     \node[fill=parchment, opacity=0.7, text opacity=1, draw opacity=1, inner sep=0mm, anchor=north west, font=\sffamily\fontsize{8}{8.5}, draw=black, rounded corners=0.4mm, fit={(17.5, 28) (39.5, 2)}] (ABS) {};

#     \node[tag, anchor=east] at ([xshift=-0.5mm] ABS.north east) {ABILITIES AND ATTACKS};

#     \node[anchor=west, align=left, text width=18mm, font=\sffamily\fontsize{4.5}{4.5}\selectfont] (ab) at (ABS.west) {%
#     #5
#     };

#     % Borda
#     \draw[line width = 0.5mm, black] (0,0) rectangle (\cardwidth,\cardheight);

# \end{tikzpicture}\endgroup\allowbreak }


images = []

shutil.rmtree("output", ignore_errors=True)
os.makedirs("output/images")

for config_file in glob.glob("input/*.toml"):

    with open(config_file, mode="rb") as fp:
        cards = tomli.load(fp)

    outputfile = "output/" + os.path.splitext(os.path.basename(config_file))[0] + ".tex"
    with open(outputfile, mode="w") as output:

        output.write(r"\documentclass{article}")

        for include_file in sorted(glob.glob("includes/*.tex")):
            include(include_file, output)

        output.write(r"\begin{document}\begin{center}")

        for title, p in cards.items():

            title = p.get("title", title)

            output.write(
                f"""%
% {''.join(['=' for char in title])}
% {title}
% {''.join(['=' for char in title])}
"""
            )

            count = int(p.get("count", 1))
            if p.get("print", True):
                for i in range(0, count):

                    if p.get("token", False):
                        print_token(title, p, output)
                    elif p.get("back", False):
                        print_back_card(title, p, output)
                    elif p.get("sheet", False):
                        print_sheet(title, p, output)
                    elif p.get("inventory", False):
                        print_inventory(title, p, output)
                    elif p.get("creature", False):
                        print_creature(title, p, output)
                    elif p.get("include", None) is not None:
                        include(p.get("include"), output)
                    elif p.get("latex", None) is not None:
                        output.write(p.get("latex"))
                    elif p.get("description", None) is None:
                        print_image(p, output)
                    else:
                        print_card(title, p, output)
            else:
                output.write("% Not printed\n")

        output.write("\\end{center}\\end{document}")

    for image in images:
        if os.path.isfile(image):
            shutil.copy(image, f"output/{image}")
        for ext in [".png", ".jpeg", ".jpg"]:
            if os.path.isfile(image + ext):
                shutil.copy(image + ext, f"output/{image + ext}")

    # with zipfile.ZipFile('output.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
    #     for dirname, subdirs, files in os.walk("output"):
    #         zf.write(dirname)
    #         for filename in files:
    #             zf.write(os.path.join(dirname, filename))
