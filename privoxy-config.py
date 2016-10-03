import sublime, sublime_plugin

# Opens privoxy config file and sets syntax to makefile
class PrivoxyConfigCommand(sublime_plugin.WindowCommand):
    def run(self, paths = [], name = ""):
        view = self.window.open_file('~/configs/privoxy/my.action')

        # open_file is a async function so that we need to wait view to load
        def set_syntax():
            if view.is_loading():
                sublime.set_timeout(set_syntax, 100)
            else:
                view.set_syntax_file('Packages/Makefile/Makefile.tmLanguage')

        set_syntax()

# Opens privoxy main config file and sets syntax to makefile
class PrivoxyMainConfigCommand(sublime_plugin.WindowCommand):
    def run(self, paths = [], name = ""):
        view = self.window.open_file('/usr/local/etc/privoxy/config')

        # open_file is a async function so that we need to wait view to load
        def set_syntax():
            if view.is_loading():
                sublime.set_timeout(set_syntax, 100)
            else:
                view.set_syntax_file('Packages/Makefile/Makefile.tmLanguage')

        set_syntax()

class YaxyConfigCommand(sublime_plugin.WindowCommand):
    def run(self, paths = [], name = ""):
        view = self.window.open_file('~/configs/.yaxyrc')

        def set_syntax():
            if view.is_loading():
                sublime.set_timeout(set_syntax, 100)
            else:
                view.set_syntax_file('Packages/Makefile/Makefile.tmLanguage')

        set_syntax()
