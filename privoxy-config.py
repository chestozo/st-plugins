import sublime, sublime_plugin

# Opens privoxy config file and sets syntax to makefile
class PrivoxyConfigCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.window().open_file('~/configs/privoxy/my.action')
        self.view.set_syntax_file('Packages/Makefile/Makefile.tmLanguage')
