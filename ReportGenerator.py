"""report generator:

Got tired of cutting and pasting images into pages so created this report generator to save images and make latex
reports. Probably could be done using notebook exports but this I know how to do for sure.
Has a slightly lazy limit of a million images coming from image save code
"""

import os
from pathlib import Path
import matplotlib.pyplot as plt
import glob
import pandas as pd

class LatexReport(object):
    save_folder = '../reports/latex_reports'
    image_folder_append = '_images'

    def __init__(self,report_name):
        self.name = report_name
        # make file and directory to make images
        self.main_dir = os.path.join(self.save_folder,self.name)
        self.tex_file = os.path.join(self.main_dir,self.name + '.tex')
        self.image_dir = os.path.join(self.main_dir,self.name+self.image_folder_append)
        if not os.path.isdir(self.main_dir):
            os.mkdir(self.main_dir)
        if not os.path.isdir(self.image_dir):
            os.mkdir(self.image_dir)
        self.instantiate_tex_file()
        self.instantiate_image_dir()


    def instantiate_tex_file(self):
        open(self.tex_file, 'a')

    def instantiate_image_dir(self):
        if not os.path.isdir(self.image_dir):
            os.mkdir(self.image_dir)

    def reset_tex_file(self,file_title = None):
        with open(self.tex_file, 'w') as tex_file:
            tex_file.write(tex_start_string)
        if file_title:
            # double brackets are needed in the string below due to format operation
            self.add_tex(r"""\subsection*{{{:}}}""".format(file_title))
            self.add_tex('\n')

    def reset_folder(self):
        """
        delete all the .png images in self.image_dir
        :return:
        """
        to_remove = glob.glob(os.path.join(self.image_dir,'*.png'))
        for f in to_remove:
            os.remove(f)


    def finish_tex_file(self):
        with open(self.tex_file, 'a') as tex_file:
            tex_file.write(tex_end_string)

    def add_tex(self, tex_to_add):
        with open(self.tex_file, 'a') as tex_file:
            tex_file.write(tex_to_add)

    def add_image(self, image_fig, caption=None):
        """
        saves figure as a png to the image folder and then adds the latex to add it to the document. Uses the 'H'
        float flag, so they should stay in the prescribed order.
        :param image_fig:
        :param caption:
        :return:
        """
        image_files = glob.glob(os.path.join(self.image_dir,'*.png'))
        #image_files = [x for x in os.listdir(self.image_dir) if ((x[0]!='.') and (x[-4:] == '.png'))]
        image_files.sort()
        # images are saved simply as numbers with .png get the highest current number to add a new one.
        if len(image_files) == 0:
            image_number = 1
        else:
            image_number = int(os.path.basename(image_files[-1])[:-4]) +1

        image_name = '{:06d}.png'.format(image_number)
        print('image number : ', image_name)


        image_fig.savefig(os.path.join(self.image_dir,image_name), format='png')
        # when compiled as latex it will read '.' as the latex_reports and doesn't want a file extension
        self.add_tex(figure_string_1.format(os.path.join(self.name + self.image_folder_append,image_name[:-4])))
        if caption:
            self.add_tex(figure_string_2.format(caption))
        self.add_tex(figure_string_3.format()) #format command is just to make strng conisistently double {{
        self.add_tex('\n')

    def add_table(self, table, format_strings=None):
        """
        add a pandas table as a latex table
        :param table:
        :return:
        """

        table_string = r"""\begin{center}
\begin{tabular}
{ | """ + r'c |'*table.shape[1] + r"""}
"""
        table_string += "\\hline \n".format()
        table_string += r" & ".join([r"{:}".format(row_val) for row_val in table.columns]) + ' \\\\ \n'.format()

        vals = table.values
        for val_row in vals:
            table_string+= "\\hline \n".format()
            if format_strings:
                table_string += r" & ".join([format_strings[i].format(row_val) for i,row_val in enumerate(val_row)])
            else:
                table_string += r" & ".join([r"{:}".format(row_val) for row_val in val_row])
            table_string+= " \\\\ \n".format()
        table_string += "\\hline \n".format()

        table_string += r"""
\end{tabular}
\end{center}

"""
        self.add_tex(table_string)
        #print(table_string)

tex_start_string = r"""
\documentclass[a4paper,10pt]{book}

\usepackage[utf8x]{inputenc}
\usepackage{fullpage}
\usepackage[final]{pdfpages}
\usepackage{wrapfig}
\usepackage{amssymb}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amsbsy}
\usepackage{hyperref}
\usepackage{cite}
\usepackage{subfigure}
\usepackage{graphicx}
\usepackage[rightcaption]{sidecap}

% from peter - red and blue text.
\newcommand{\red}[1]{{\textcolor{red}{#1}}}
\newcommand{\blue}[1]{{\textcolor{blue}{#1}}}

\usepackage[toc,page]{appendix}
\usepackage{floatrow} % for figures with captions on the left.
\setlength{\parindent}{0pt} % no paragraph indent

\begin{document}

"""

tex_end_string = """


\end{document}
"""

figure_string_1 = r"""
\begin{{figure}}[H]
\centering
\includegraphics[width=\linewidth]{{{:}}}
"""

figure_string_2 = r"""
\caption{{{:}}}
"""

figure_string_3 = r"""
\end{{figure}}

"""