import sys
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

class Screenshot(QWebView):
    def __init__(self):
        self.app = QApplication(sys.argv)
        QWebView.__init__(self)
        self._loaded = False
        self.loadFinished.connect(self._loadFinished)

    def capture(self, url, output_file):
        self.load(QUrl(url))
        self.wait_load()
        # set to webpage size
        frame = self.page().mainFrame()
        self.page().setViewportSize(frame.contentsSize())
        # render image
        image = QImage(self.page().viewportSize(), QImage.Format_ARGB32)
        painter = QPainter(image)
        frame.render(painter)
        painter.end()
        prin('saving', output_file)
        image.save(output_file)

    def wait_load(self, delay=0):
        # process app events until page loaded
        while not self._loaded:
            self.app.processEvents()
            time.sleep(delay)
        self._loaded = False

    def _loadFinished(self, result):
        self._loaded = True

s = Screenshot()
s.capture('https://dataanalytics.uc.edu/t/Provost/views/UCCOVIDCareful-External/CaseSummaryExternal?%3Aembed=y&%3AshowVizHome=no&%3Ahost_url=https%3A%2F%2Fdataanalytics.uc.edu%2F&%3Aembed_code_version=3&%3Atabs=no&%3Atoolbar=yes&%3Aiid=5&%3AisGuestRedirectFromVizportal=y&%3Adisplay_spinner=no&%3AloadOrderID=0', 'website.png')
