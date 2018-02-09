# -*- coding: utf-8 -*-
from __future__ import print_function
import os
from shutil import copyfile
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Installs the Bulma extra js and css"

    def add_arguments(self, parser):
        parser.add_argument('css',
                            default="css",
                            help='Css path',
                            )
        parser.add_argument('js',
                            default="js",
                            help='Js path',
                            )

    def handle(self, *args, **options):
        css = options["css"]
        js = options["js"]
        cmd = "git clone https://github.com/synw/bulma-extra"
        print("Cloning the assets repository")
        os.system(cmd)
        print("Installing files")
        copyfile("bulma-extra/bulma-extra.css", css + "/bulma-extra.css")
        copyfile("bulma-extra/bulma-extra.js", js + "/bulma-extra.js")
        print("Done")
        cssl = '<link rel="stylesheet" media="screen, projection" href="' + \
            css + '/bulma-extra.css" />'
        jsl = '<script type="text/javascript" src="' + js + '/bulma-extra.js"></script>'
        os.system("rm -rf bulma-extra")
        print("\n" + cssl)
        print(jsl + "\n")
