import os
import mapnik

valid_extensions = ['.ttf','.otf','.ttc','.pfa','.pfb','.ttc','.dfont']

class FontHandler(object):
    def __init__(self):
        self.added = []
        self.failed = []
        if hasattr(mapnik, 'fontscollectionpath'):
            self.fontdir = mapnik.fontscollectionpath
        else:
            self.fontdir = mapnik.paths.fontscollectionpath
    
    @property
    def available(self):
        return [f for f in mapnik.FontEngine.face_names()]

    def add_fonts(self,fonts):
        # Adding compatibility between old and new FontEngine API build
        try:
            engine = mapnik.FontEngine.instance()
        except AttributeError:
            engine = mapnik.FontEngine
        for font in fonts:
            if os.path.isdir(font):
                found = False;
                for dirpath, _, filenames in os.walk(font):
                    for filename in filenames:
                        if os.path.splitext(filename)[1] in valid_extensions:
                            font_name = os.path.join(dirpath, filename)
                            if engine.register_font(font_name):
                                self.added.append(font_name)
                            else:
                                self.failed.append(font_name)
            else:
                if engine.register_font(font):
                    self.added.append(font)
                else:
                    self.failed.append(font)

