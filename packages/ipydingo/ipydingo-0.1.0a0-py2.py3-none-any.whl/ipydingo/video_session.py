import ipywidgets as widgets
from traitlets import Unicode, Int

# See js/lib/example.js for the frontend counterpart to this file.

@widgets.register
class VideoSession(widgets.DOMWidget):
    """An example widget."""

    # Name of the widget view class in front-end
    _view_name = Unicode('VideoSessionView').tag(sync=True)

    # Name of the widget model class in front-end
    _model_name = Unicode('VideoSessionModel').tag(sync=True)

    # Name of the front-end module containing widget view
    _view_module = Unicode('ipydingo').tag(sync=True)

    # Name of the front-end module containing widget model
    _model_module = Unicode('ipydingo').tag(sync=True)

    # Version of the front-end module containing widget view
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    # Version of the front-end module containing widget model
    _model_module_version = Unicode('^0.1.0').tag(sync=True)

    hostname = Unicode('localhost').tag(sync=True)
    port = Int(8080).tag(sync=True)

    def video(self):
        return self

def ipy_video(hostname, port):
    vid_session = VideoSession(hostname = hostname, port = port)
    return vid_session, vid_session
