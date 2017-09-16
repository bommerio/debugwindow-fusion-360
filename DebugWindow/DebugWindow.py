import adsk.core, adsk.fusion, adsk.cam, traceback

# global set of event handlers to keep them referenced for the duration of the command
handlers = []
_app = adsk.core.Application.cast(None)
_ui = adsk.core.UserInterface.cast(None)

# Event handler for the commandCreated event.
class ShowTextCommandPaletteCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
        self.palette = _ui.palettes.itemById('TextCommands')
    def notify(self, args):
        try:
            self.palette.isVisible = not self.palette.isVisible
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))     
                
def run(context):
    try:
        global _ui, _app
        _app = adsk.core.Application.get()
        _ui  = _app.userInterface
        
        # Add a command that displays the panel.
        showPaletteCmdDef = _ui.commandDefinitions.itemById('showTextCommandPalette')
        if not showPaletteCmdDef:
            showPaletteCmdDef = _ui.commandDefinitions.addButtonDefinition('showTextCommandPalette', 'Show Debug Window', 'Show the debug window, using the built in Text Command palette', '')

            # Connect to Command Created event.
            onCommandCreated = ShowTextCommandPaletteCommandCreatedHandler()
            showPaletteCmdDef.commandCreated.add(onCommandCreated)
            handlers.append(onCommandCreated)

        # Add the command to the toolbar.
        panel = _ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
        cntrl = panel.controls.itemById('showTextCommandPalette')
        if not cntrl:
            panel.controls.addCommand(showPaletteCmdDef)

        #_ui.messageBox('Start addin')
    except:
        if _ui:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def stop(context):
    try:        
        # Delete controls and associated command definitions created by this add-ins
        panel = _ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
        cmd = panel.controls.itemById('showTextCommandPalette')
        if cmd:
            cmd.deleteMe()
        cmdDef = _ui.commandDefinitions.itemById('showTextCommandPalette')
        if cmdDef:
            cmdDef.deleteMe() 
            
        #_ui.messageBox('Stop addin')
    except:
        if _ui:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))