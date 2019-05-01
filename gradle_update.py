
import os
import re
from common import *

def update_build_file(folder):
    # Check for build.gradle file
    build_file = os.path.join(folder, 'build.gradle')
    if not file_exists(build_file):
        return
    
    content = file_read(build_file)

    match = re.search(r'google\(\)', content)
    if match:
        print "build.gradle is ready for update"
        return
    else:
        print "Fixing build.gradle"
        content = re.sub(r'jcenter\(\)', r'google()\n\tjcenter()', content)
    
    file_write(build_file, content)

def update_gradle(root_path, gradle_version):
    for root, dirs, files in os.walk(root_path, topdown=True):
        for f in files:
            if "gradlew" == f:
                print "root:" + root
                print "file:" + f
                abs_path = os.path.abspath(os.path.join(root_path, root))
                os.chdir(abs_path)
                # Fix build.gradle for older versions
                update_build_file(abs_path)
                os.system("gradlew wrapper --gradle-version=" + gradle_version + " --distribution-type=all")

def main():
    # find all android studio projects under current path
    from optparse import OptionParser
    parser = OptionParser(usage='usage: %prog root_directory -v 5.4.1')
    parser.add_option('-v', '--version',dest='version', help="Version for gradle")
    (opts, args) = parser.parse_args()

    if not opts.version:
        parser.error('please specify gradle version with -v')

    if len(args) < 1:
        parser.error("Please specify root directory")
    else:
        update_gradle(args[0], opts.version)

# ---------- main -------------
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)