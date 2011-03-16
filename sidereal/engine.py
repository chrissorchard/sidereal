"""
Ah, graphics.

"""

# let's totally steal stuff from CrystalSpace
# by that, I mean, use it.
import cspace
from cspace import csInitializer

class Engine(object):
    def __init__(self):
        self.plugin_requests = [
        cspace.CS_REQUEST_VFS, cspace.CS_REQUEST_OPENGL3D,
        cspace.CS_REQUEST_ENGINE, cspace.CS_REQUEST_FONTSERVER,
        cspace.CS_REQUEST_IMAGELOADER, cspace.CS_REQUEST_LEVELLOADER,
        ]
    def init(self):
        # set up the object register
        self._object_reg = csInitializer.CreateEnvironment(['PROGRAM'])
        if self._object_reg is None:
            raise CSEngineException("Couldn't create environment!")
        
        if not csInitializer.SetupConfigManager(self._object_reg):
            raise CSEngineException("Couldn't initalise application.")

        if not csInitializer.RequestPlugins(self._object_reg,
                                                self.plugin_requests):
            raise CSEngineException("Plugin requsts failed.")

        if not csInitializer.SetupEventHandler(self._object_reg,self._event_handler):
            raise CSEngineException("Could not initalize event handler!")

        # get used event IDs
        self._keyboard_down_id = cspace.csevKeyboardDown(self._object_reg)

        if not csInitializer.OpenApplication(self._object_reg):
            raise CSEngineException("Could not open the application!")

    def destroy(self):
        csInitializer.DestroyApplication(self._object_reg)

    def run(self):
        cspace.csDefaultRunLoop(self._object_reg)

    @staticmethod
    def _event_handler(event):
        global _inst
        if ((event.Name  == _inst._keyboard_down_id) and
            (cspace.csKeyEventHelper.GetCookedCode(event) == cspace.CSKEY_ESC)):
            q  = _inst._object_reg.Get(cspace.iEventQueue)
            if q:
                q.GetEventOutlet().Broadcast(cspace.csevQuit(_inst._object_reg))
                return 1
        return 0




class CSEngineException(Exception):
    """
    Thrown when something in the setup or running of the Crystal Space
    Engine dies, or fails horribly.
    """
    pass

_inst = Engine()
init = _inst.init
run = _inst.run
destroy = _inst.destroy
