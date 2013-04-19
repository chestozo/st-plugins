# run_multiple_commands.py

import sublime, sublime_plugin

# Takes an array of commands (same as those you'd provide to a key binding) with
# an optional context (defaults to view commands) & runs each command in order.
# Valid contexts are 'text', 'window', and 'app' for running a TextCommand,
# WindowCommands, or ApplicationCommand respectively.

class RunMultipleCommandsCommand(sublime_plugin.TextCommand):
  def exec_command(self, command):
    if not 'command' in command:
      raise Exception('No command name provided.')

    args = None
    if 'args' in command:
      args = command['args']

    # default context is the view since it's easiest to get the other contexts
    # from the view
    context = self.view
    if 'context' in command:
      context_name = command['context']
      if context_name == 'window':
        context = context.window()
      elif context_name == 'app':
        context = sublime
      elif context_name == 'text':
        pass
      else:
        raise Exception('Invalid command context "'+context_name+'".')

    # skip args if not needed
    if args is None:
      context.run_command(command['command'])
      # uncomment the next line, if you want to add a delay to the execution
      # sublime.set_timeout( lambda: context.run_command(command['command']), 2000 )
    else:
      context.run_command(command['command'], args)
      # uncomment the next line, if you want to add a delay to the execution
      # sublime.set_timeout( lambda: context.run_command(command['command'], args), 2000 )

  def run(self, edit, commands = None):
    if commands is None:
      return # not an error
    for command in commands:
      self.exec_command(command)
