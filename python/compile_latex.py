#!/usr/bin/python

__author__ = "Tiago Oliveira & Debora Antunes"
__copyright__ = ""
__credits__ = ["Tiago Oliveira", "Debora Antunes"]
__license__ = "GPL-3.0"
__version__ = "compile_latex"
__maintainer__ = "Tiago Oliveira"
__email__ = "tiagomanuel28@gmail.com"
__status__ = "Done"

###############################################################################

## Imports
import subprocess, sys, datetime, os
try:
    filename = sys.argv[1]
except:
    filename = input("Name of the file to compile:")

## Objects
exclude = [".tex", ".pdf", ".csv", ".sty", "temp"]
dir = filename + "_temp"

## Manage temp files and temp folder
if os.path.exists(dir):
    for file in os.listdir(dir):
        if not file.startswith("."):
            os.replace(str(dir+"/"+file), str(file))
else:
    os.makedirs(dir)

## Run latex compile commands
commands = [
    ['pdflatex', filename + '.tex'],
    ['makeglossaries', filename],
    ['bibtex', filename],
    ['pdflatex', filename + '.tex'],
    ['pdflatex', filename + '.tex'],
    ['texcount', '-inc', '-total', '-0', filename + '.tex', '-out=word_count.txt']
]

for c in commands:
    subprocess.call(c)

## Make word count stats
with open("word_count.txt", "r") as wc_file, open(filename + '.csv', "a+") as wc_csv:
    wc = str(wc_file.readlines()[1].split("+")[0])
    date = str(datetime.datetime.now()).replace(" ", "_")[:-10]
    wc_csv.write(date + "," + wc + "\n")


## Clean up main folder
os.remove("word_count.txt") 
for file in os.listdir():
    if file.startswith(filename) and file[-4:] not in exclude:
        os.replace(str(file), str(dir+"/"+file))