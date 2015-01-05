import sublime, sublime_plugin

# Opens privoxy config file and sets syntax to makefile
class PrivoxyConfigCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view.window().open_file('~/configs/privoxy/my.action')

        # open_file is a async function so that we need to wait view to load
        def set_syntax():
            if view.is_loading():
                sublime.set_timeout(set_syntax, 100)
            else:
                view.set_syntax_file('Packages/Makefile/Makefile.tmLanguage')

        set_syntax()

class YaxyConfigCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view.window().open_file('~/configs/.yaxyrc')

        def set_syntax():
            if view.is_loading():
                sublime.set_timeout(set_syntax, 100)
            else:
                view.set_syntax_file('Packages/Makefile/Makefile.tmLanguage')

        set_syntax()
