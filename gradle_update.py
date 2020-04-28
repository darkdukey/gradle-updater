#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
from common import *

def update_gradle_wrapper(path, gradle_version):
    print('== [✔] Update gradle wrapper')
    content = file_read(path)
    if content:
        content = re.sub(r'distributionUrl=.*', r'distributionUrl=https\\://services.gradle.org/distributions/gradle-' + gradle_version + '-all.zip', content)
        file_write(path, content)

def update_gradle_build(path, plugin_version):
    # Decide the type of build.gradle
    print('== Checking build.gradle file')
    content = file_read(path)
    match = re.search(r'build:gradle:', content)
    if match:
        print('== Found Root Gradle')
        update_root_gradle(path, plugin_version)
    else:
        print('== Found Child Gradle')
        update_child_gradle(path, plugin_version)

def update_root_gradle(path, plugin_version):
    # Add google() repo
    content = file_read(path)
    match = re.search(r'google\(\)', content)
    if match:
        print("build.gradle is ready for update")
    else:
        print("Fixing build.gradle")
        content = re.sub(r'jcenter\(\)', r'google()\n\t\tjcenter()', content)
        file_write(path, content)
    # update gradle plugin
    content = re.sub(r'build:gradle:\d.\d.\d', r'build:gradle:' + plugin_version, content)
    file_write(path, content)

def update_child_gradle(path, plugin_version):
    content = file_read(path)
    if content:
        # remove buildToolVersion
        content = re.sub(r'buildToolsVersion.*', r'', content)
        # change compile to implementation
        content = re.sub(r'  compile ', r'  implementation ', content)
        file_write(path, content)

def update_gradle(root_path, gradle_version, plugin_version):
    for root, dirs, files in os.walk(root_path, topdown=True):
        for f in files:
            if 'gradle-wrapper.properties' == f:
                update_gradle_wrapper(os.path.join(root, f), gradle_version)
            elif 'build.gradle' == f:
                update_gradle_build(os.path.join(root, f), plugin_version)

def main():
    # find all android studio projects under current path
    from optparse import OptionParser
    parser = OptionParser(usage='usage: %prog root_directory -v 5.6.4 -p 3.6.1')
    parser.add_option('-v', '--version',dest='version', help="Gradle version")
    parser.add_option('-p', '--plugin', dest='plugin', help="Gradle Plugin version")
    (opts, args) = parser.parse_args()

    if not opts.version:
        parser.error('please specify gradle version with -v')

    if not opts.plugin:
        parser.error('Please specify gradle plugin version with -p')

    if len(args) < 1:
        parser.error("Please specify root directory")
    else:
        update_gradle(args[0], opts.version, opts.plugin)

# ---------- main -------------
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
