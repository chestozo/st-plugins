# Based on: http://www.bergspot.com/blog/2012/05/formatting-xml-in-sublime-text-2-xmllint/
# use shell in python: http://www.sublimetext.com/forum/viewtopic.php?f=2&p=12451
# shell quote: http://stackoverflow.com/a/35857/449345
import sublime, sublime_plugin, subprocess, os, codecs


def shellquote(s):
    return "'" + s.replace("'", "'\\''") + "'"

def escape_quotes(s):
    return s.replace('"', '\\"').replace("'", "'\\''")

syntax_dict = {
    'js': 'Packages/Naomi/syntaxes/naomi.fjsx15.sublime-syntax',
    'html': 'Packages/HTML/HTML.sublime-syntax'
}

# open_file is a async function so that we need to wait view to load
def set_syntax(view, file_type):
    if view.is_loading():
        sublime.set_timeout(lambda: set_syntax(file_type), 100)
    else:
        view.set_syntax_file(syntax_dict[file_type])


def beautify(self, edit, cmd, tmpfile):
    code = self.view.substr(self.view.sel()[0]) #.encode('utf-8')
    if code:
        # tmpfile is used by some of the beautifiers
        tmpfile = codecs.open(tmpfile, 'w', 'utf-8')
        tmpfile.write(code)
        tmpfile.close()

        p = subprocess.Popen(
            cmd,
            shell=True,
            bufsize=-1,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE
        )
        output, error = p.communicate(code.encode('utf-8')) # not sure if we need this
        if error:
            sublime.error_message(error.decode('utf-8'))
        else:
            result = output.decode('utf-8')
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
        beautify(self, edit, "bash -c '. ~/.bashrc 2&> /dev/null ; /usr/local/bin/js-beautify --type html -x -r ~/tmp/code-beautify.html > /dev/null ; cat ~/tmp/code-beautify.html'", os.environ['HOME'] + '/tmp/code-beautify.html')
        set_syntax(self.view, 'html')

class CodeBeautifyJsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        beautify(self, edit, "bash -c '. ~/.bashrc 2&> /dev/null ; /usr/local/bin/js-beautify --type js -r ~/tmp/code-beautify.js > /dev/null ; cat ~/tmp/code-beautify.js'", os.environ['HOME'] + '/tmp/code-beautify.js')
        set_syntax(self.view, 'js')
