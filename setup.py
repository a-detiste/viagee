#!/usr/bin/python3

import os
import shutil
import subprocess
import sys

import setuptools.command.build_py
from setuptools import setup

podir = "./po"
pext = ".po"

langs = sorted([x[:-3] for x in os.listdir(podir) if x[-3:] == pext])


def modir(lang):
    return os.path.join("build/mo", lang)


def mkmo(lang):
    outpath = modir(lang)
    if os.path.exists(outpath):
        shutil.rmtree(outpath)
    os.makedirs(outpath)

    inpath = os.path.join(podir, lang + pext)
    cmd = "msgfmt %s -o %s/viagee.mo" % (inpath, outpath)

    subprocess.call(cmd, shell=True) and sys.exit(1)


def merge_i18n():

    cmd = "LC_ALL=C intltool-merge -u " +\
          "-c %s/.intltool-merge-cache " % podir +\
          podir
    for infile in (x[:-3] for x in os.listdir('.') if x[-3:] == '.in'):
        print("Processing %s.in to %s" % (infile, infile))

        if 'desktop' in infile:
            flag = '-d'
        elif 'schema' in infile:
            flag = '-s'
        elif 'xml' in infile:
            flag = '-x'
        else:
            flag = ''

        if flag:
            args = " %s %s.in %s" % (flag, infile, infile)
            subprocess.call(cmd + args, shell=True) and sys.exit(1)


class my_build(setuptools.command.build_py.build_py):
    def run(self):
        setuptools.command.build_py.build_py.run(self)

        for lang in langs:
            mkmo(lang)

        merge_i18n()


def polist():
    dst_tmpl = "share/locale/%s/LC_MESSAGES/"
    polist = [(dst_tmpl % x, ["%s/viagee.mo" % modir(x)]) for x in langs]

    return polist


setup(
    name='viagee',
    py_modules=['viagee'],
    version='3.7.1',
    description='support for Gmail as the preferred GNOME email application',
    author='David Steele',
    author_email='dsteele@gmail.com',
    url='https://davesteele.github.io/viagee/',
    scripts=['viagee'],
    requires=[],
    data_files=[
        ('share/icons/hicolor/16x16/apps', ['icons/16x16/viagee.png']),
#        ('share/icons/hicolor/24x24/apps', ['icons/24x24/viagee.png']),
        ('share/icons/hicolor/32x32/apps', ['icons/32x32/viagee.png']),
        ('share/icons/hicolor/48x48/apps', ['icons/48x48/viagee.png']),
        ('share/icons/hicolor/256x256/apps',
            ['icons/256x256/viagee.png']),
        ('share/applications', ['viagee.desktop']),
        ('share/viagee/autostart', ['viagee-startup.desktop']),
        ('share/viagee', ['viagee.glade', 'viagee.py']),
        ('share/metainfo', ['viagee.appdata.xml']),
               ] + polist(),
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Communications :: Email',
        'Topic :: Desktop Environment :: Gnome',
        'License :: OSI Approved :: " \
            "GNU General Public License v2 or later (GPLv2+)',
        'Intended Audience :: End Users/Desktop',
                ],
    cmdclass={
        'build_py': my_build,
             },
     )
