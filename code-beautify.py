# Based on: http://www.bergspot.com/blog/2012/05/formatting-xml-in-sublime-text-2-xmllint/
# use shell in python: http://www.sublimetext.com/forum/viewtopic.php?f=2&p=12451
# shell quote: http://stackoverflow.com/a/35857/449345
import sublime, sublime_plugin, subprocess

def shellquote(s):
    return "'" + s.replace("'", "'\\''") + "'"

def beautify_code(self, edit, command, command_name):
    xmlRegion = sublime.Region(0, self.view.size())
    p = subprocess.Popen(command, bufsize=-1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    result, err = p.communicate(self.view.substr(self.view.sel()[0]).encode('utf-8'))

    if err != "":
        self.view.set_status(command_name, command_name + ": " + err)
        sublime.set_timeout(self.clear,10000)
    else:
        self.view.replace(edit, self.view.sel()[0], result.decode('utf-8'))
        sublime.set_timeout(self.clear,0)


class CodeBeautifyXmlCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        beautify_code(self, edit, "XMLLINT_INDENT=$'\t' xmllint --format --encode utf-8 -", 'xmllint')

    def clear(self):
        self.view.erase_status('xmllint')

class CodeBeautifyHtmlCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('select_all')
        beautify_code(self, edit, "~/local/bin/node ~/configs/tools/tabifier.js " + shellquote(self.view.file_name()), 'tabifier')

    def clear(self):
        self.view.erase_status('tabifier')

class CodeBeautifyJsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('select_all')
        beautify_code(self, edit, "python ~/configs/tools/jsbeautifier.py -d " + shellquote(self.view.file_name()), 'jsbeautifier')

    def clear(self):
        self.view.erase_status('jsbeautifier')





