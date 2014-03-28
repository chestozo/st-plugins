# Based on: http://www.bergspot.com/blog/2012/05/formatting-xml-in-sublime-text-2-xmllint/
# use shell in python: http://www.sublimetext.com/forum/viewtopic.php?f=2&p=12451
# shell quote: http://stackoverflow.com/a/35857/449345
import sublime, sublime_plugin, subprocess, os, commands


def shellquote(s):
    return "'" + s.replace("'", "'\\''") + "'"

def escape_quotes(s):
    return s.replace('"', '\\"').replace("'", "'\\''")


def beautify(self, edit, cmd, tmpfile):
    code = self.view.substr(self.view.sel()[0]).encode('utf-8')
    if code:
        tmpfile = open(tmpfile, 'w')
        tmpfile.write(code)
        tmpfile.close()

        result = commands.getoutput(cmd).decode('utf-8')
        if result:
            self.view.replace(edit, self.view.sel()[0], result)


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
        beautify(self, edit, "bash -c '. ~/.bashrc ; /usr/local/bin/js-beautify --type html -x ~/tmp/code-beautify.html'", os.environ['HOME'] + '/tmp/code-beautify.html')

class CodeBeautifyJsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        beautify(self, edit, "bash -c '. ~/.bashrc ; /usr/local/bin/js-beautify --type js ~/tmp/code-beautify.js'", os.environ['HOME'] + '/tmp/code-beautify.js')
