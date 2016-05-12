'''Модуль справки'''

license_of_software = '''\

    \rThe MIT License (MIT)
    \rCopyright (c) 2016 Tuzhilkin Ivan

    \rPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    \rThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    \rTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

    '''
version = '1.0'

software_help = '''\

Optinal arguments:
\r-tar\tCreate tar archive.
\r\tSuppopt values:
\r\t\tbz2\tUse bzip2 compression.
\r\t\tgz\tUse gzip compression.
\r\t\txz\tUse lzma compression.
\r-zip\tCreate zip archive.
\r\tSuppopt values:
\r\t\tbz2\tUse bzip2 compression.
\r\t\tgz\tUse gzip compression.
\r\t\txz\tUse lzma compression.
\r-a\tAdd data to archive.
\r-f\tEnter path to files and dirs, what you need add to archive.
\r-e\tExtract data of archive.
\r-n\tCreate name of archive.
\r-l\tShow License.
\r-v\tShow version.
\r-h\tShow help.
'''
def help_processing(user_dict):
    for key in user_dict:
        if key == '-v':
            print(version)
        elif key == '-h':
            print(software_help)
        elif key == '-l':
            print(license_of_software)
