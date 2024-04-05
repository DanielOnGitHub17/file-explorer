import json
"""Does not have support for style comments
"""

class CSS:
    def __init__(self, src=None, /, text=''):
        self.src = src
        self.css_text = text
        self.style_dict = {}
        self.style_list = []
        if src:
            self.parse_css(src)
        elif text:
            self.parse_csstext(text)
    def parse_css(self, src):
        with open(src) as stylefile:
            self.css_text = stylefile.read()
        return self.parse_csstext(self.css_text)
    def parse_csstext(self, text):
        #remove the spaces around and the last }
        text = text.strip().strip('}')
        splitted_text = text.split('}')
        raw_styles = [raw.split('{') for raw in splitted_text]
        
        #polish the styles by first splitting stripping the selectors ([0])
        for raw in raw_styles:
            raw[0] = raw[0].strip()
            
            #and doublestrip their styles (for spaces, newlines and ';')
            raw[1] = raw[1].strip().strip(';')
            
            #split their styles
            raw[1] = raw[1].split(';')
            
            #then strip, split, and finally strip
            for i in range(len(raw[1])):
                raw[1][i] = raw[1][i]
                raw[1][i] = [fine.strip() for fine in raw[1][i].strip().split(':')]
        self.style_list = raw_styles
        
        for selector, values in raw_styles:
            self.style_dict[selector] = dict(values)

        return self.style_dict

if __name__ == "__main__":
    from pprint import pprint
    import os
    print(os.getcwd())
    g = CSS(input("Enter the CSS file source: "))
    pprint(g.style_dict)
    input("Press enter to continue")
