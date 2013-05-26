import sublime, sublime_plugin, subprocess

def beautify_code(self, edit, command):
    # help from http://www.sublimetext.com/forum/viewtopic.php?f=2&p=12451
    xmlRegion = sublime.Region(0, self.view.size())
    p = subprocess.Popen(command, bufsize=-1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    result, err = p.communicate(self.view.substr(self.view.sel()[0]).encode('utf-8'))

    if err != "":
        self.view.set_status('xmllint', "xmllint: "+err)
        sublime.set_timeout(self.clear,10000)
    else:
        self.view.replace(edit, self.view.sel()[0], result.decode('utf-8'))
        sublime.set_timeout(self.clear,0)

# via http://www.bergspot.com/blog/2012/05/formatting-xml-in-sublime-text-2-xmllint/
class CodeBeautifyXmlCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        beautify_code(self, edit, "XMLLINT_INDENT=$'\t' xmllint --format --encode utf-8 -")

    def clear(self):
        self.view.erase_status('xmllint')

class CodeBeautifyHtmlCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('select_all')
        beautify_code(self, edit, "node ~/configs/tools/tabifier.js " + self.view.file_name())

    def clear(self):
        self.view.erase_status('xmllint')

class CodeBeautifyJsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('select_all')
        beautify_code(self, edit, "python ~/configs/tools/jsbeautifier.py -d " + self.view.file_name())

    def clear(self):
        self.view.erase_status('xmllint')





