#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytesser
import Image
#from validate_email import validate_email
def corrector_globalsources(email_text):
    repl_mass = [
        (' ',''),
        ('—', '-'),
        ('r‘f', 'rf'),
        ('\.*','y'),
        ('\»"','y'),
        ('\\\\r', 'v'),
        ('n-\'', 'rv'),
        ('\-v','w'),
        ('n/', 'ry'),
        ('\\r','v'),
        ('\/', 'y'),
        ('><','x'),
        ('|<','k'),
        ('m/', 'rry'),
        ('|', 'l'),
        ('0', 'o')
    ]
    for def_symb, new_symb in repl_mass:
        email_text = email_text.replace(def_symb, new_symb)
    return email_text


def tesser_engine(image_file_name, image_resize_procent = 250, corrector=corrector_globalsources):
    """
    Распознавание
    """
    email_image = Image.open(image_file_name)
    image_size_x, image_size_y = email_image.size
    image_size_x *= image_resize_procent/100
    image_size_y *= image_resize_procent/100
    email_image = email_image.resize((image_size_x, image_size_y))
    email_text = pytesser.image_to_string(email_image)
    email_text = email_text.strip()
    email_text = corrector(email_text)
    try:
        email_text_unicode = unicode(email_text)
    except UnicodeDecodeError:
        print 'can not convert:', email_text,
        email_text_unicode = ''
    return email_text_unicode