
import os
import re
from common import *

def update_build_file(folder, gradle_version, plugin_version):
    # Check for build.gradle file
    build_file = os.path.join(folder, 'build.gradle')
    if not file_exists(build_file):
        return
    # Add google() repo
    content = file_read(build_file)
    match = re.search(r'google\(\)', content)
    if match:
        print "build.gradle is ready for update"
    else:
        print "Fixing build.gradle"
        content = re.sub(r'jcenter\(\)', r'google()\n\tjcenter()', content)
        file_write(build_file, content)
    # update gradle plugin
    content = re.sub(r'build:gradle:\d.\d.\d', r'build:gradle:' + plugin_version, content)
    file_write(build_file, content)
    # update wrapper file
    wrapper_file = os.path.join(folder, 'gradle', 'wrapper', 'gradle-wrapper.properties')
    print "Modify wrapper file: " + wrapper_file
    content = file_read(wrapper_file)
    if content:
        content = re.sub(r'distributionUrl=.*', r'distributionUrl=https\\://services.gradle.org/distributions/gradle-' + gradle_version + '-all.zip', content)
        file_write(wrapper_file, content)
    # Update app/build.gradle
    app_build_file = os.path.join(folder, 'app', 'build.gradle')
    content = file_read(app_build_file)
    if content:
        # remove buildToolVersion
        content = re.sub(r'buildToolsVersion.*', r'', content)
        # change compile to implementation
        content = re.sub(r'  compile ', r'  implementation ', content)
        file_write(app_build_file, content)

def update_gradle(root_path, gradle_version, plugin_version):
    for root, dirs, files in os.walk(root_path, topdown=True):
        for f in files:
            if "gradlew" == f:
                print '== Update Gradlew =='
                print "root:" + root
                print "file:" + f
                abs_path = os.path.abspath(os.path.join(root_path, root))
                os.chdir(abs_path)
                # Fix build.gradle for older versions
                update_build_file(abs_path, gradle_version, plugin_version)
                os.system("gradlew wrapper --gradle-version=" + gradle_version + " --distribution-type=all")
            elif "build.gradle" == f:
                print '== update build.gradle file =='
                print "root:" + root
                print "file:" + f
                abs_path = os.path.abspath(os.path.join(root_path, root))
                os.chdir(abs_path)
                update_build_file(abs_path, gradle_version, plugin_version)

def main():
    # find all android studio projects under current path
    from optparse import OptionParser
    parser = OptionParser(usage='usage: %prog root_directory -v 5.4.1 -p 3.4.0')
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