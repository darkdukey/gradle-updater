
import os
from common import *

def update_gradle(root_path, gradle_version):
    for root, dirs, files in os.walk(root_path, topdown=False):
        for f in files:
            if "gradlew" == f:
                print "root:" + root
                print "file:" + f
                os.system("gradle wrapper -d " + root + " --gradle-version=" + gradle_version + " --distribution-type=all")
        # for d in dirs:
        #     print(os.path.join(root, d))

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