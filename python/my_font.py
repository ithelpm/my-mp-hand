import matplotlib.font_manager
# Get the list of font names
font_names = [f.name for f in matplotlib.font_manager.fontManager.ttflist]
font_names = str(font_names)
table = str.maketrans({
    '[':'',
    ']':'',
    '\'':'',
    ',':'\n',
})
font_names = font_names.translate(table)
b = lambda :'cod' in font_names
print(font_names)
print(b())
