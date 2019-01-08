from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import argparse
import signal
import sys, os

from testvector import TestVector

__version__ = "1.0.0"


# -----------------------------------------------------------------------------
#  Exceptions.
# -----------------------------------------------------------------------------

class FileReadError(RuntimeError): pass
class NoSuchFileError(RuntimeError): pass
class UnknownFileTypeError(RuntimeError): pass

def exceptionHandler(f):
    """Function decorator returning a exception handler function."""
    def _critical(title, *args):
        QtWidgets.QMessageBox.critical(None, title, " ".join((str(arg) for arg in args)))
    def _exceptionHandler(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except FileReadError as exception:
            _critical("Read error", "<strong>Failed to read from file:</strong><br/>", exception)
        except NoSuchFileError as exception:
            _critical("No such file", "<strong>No such file to open:</strong><br/>", exception)
        except UnknownFileTypeError as exception:
            _critical("Unknown filetype", "<strong>Unknown file type:</strong><br/>", exception)
        except:
            raise
    return _exceptionHandler

# -----------------------------------------------------------------------------
#  Main window class.
# -----------------------------------------------------------------------------

class MainWindow(QtWidgets.QMainWindow):

    AppTitle = "Testvector Viewer"
    AppVersion = __version__

    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        # Setup main window.
        self.setWindowTitle(self.AppTitle)
        self.setWindowIcon(QtGui.QIcon.fromTheme('utilities-system-monitor'))
        self.resize(1000, 700)

        # Create menus, toolbars and status bar.
        self.createActions()
        self.createToolbars()
        self.createMenubar()
        self.createStatusbar()

        # Setup central MDI area.
        self.mdiArea = MdiArea(self)
        self.setCentralWidget(self.mdiArea)

    def createActions(self):
        """Create actions used in menu bar and tool bars."""

        # Action for opening a new connections file.
        self.openAct = QtWidgets.QAction("&Open...", self)
        self.openAct.setShortcut(QtGui.QKeySequence.Open)
        self.openAct.setStatusTip("Open an existing file")
        self.openAct.setIcon(QtGui.QIcon.fromTheme('document-open'))
        self.openAct.triggered.connect(self.onOpen)

        self.closeAct = QtWidgets.QAction(self.tr("&Close"), self)
        self.closeAct.setShortcuts(QtGui.QKeySequence.Close)
        self.closeAct.setStatusTip("Close the current file")
        self.closeAct.setEnabled(False)
        self.closeAct.triggered.connect(self.onClose)

        # Action to quit the application.
        self.quitAct = QtWidgets.QAction( "&Quit", self)
        self.quitAct.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Q))
        self.quitAct.setStatusTip("Exit")
        self.quitAct.triggered.connect(self.onQuit)

        # Action for toggling status bar.
        self.statusbarAct = QtWidgets.QAction("&Statusbar", self)
        self.statusbarAct.setCheckable(True)
        self.statusbarAct.setChecked(True)
        self.statusbarAct.setStatusTip("Show or hide the statusbar in the current window")
        self.statusbarAct.toggled.connect(self.onToggleStatusBar)

        # Actions to show online contents help.
        self.contentsAct = QtWidgets.QAction("&Contents", self)
        self.contentsAct.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F1))
        self.contentsAct.triggered.connect(self.onContents)

        # Actions to show about dialog.
        self.aboutAct = QtWidgets.QAction("&About", self)
        self.aboutAct.triggered.connect(self.onAbout)

    def createToolbars(self):
        """Create tool bars and setup their behaviors (floating or static)."""

        self.toolbar = self.addToolBar("Toolbar")
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)
        self.toolbar.addAction(self.openAct)

        # Create action for toggling the tool bar here.
        self.toolbarAct = self.toolbar.toggleViewAction() # Get predefined action from toolbar.
        self.toolbarAct.setStatusTip("Show or hide the toolbar in the current window")

    def createMenubar(self):
        """Create menu bar with entries."""

        # Menu entry for file actions.
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.closeAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAct)

        # Menu entry for view actions.
        self.viewMenu = self.menuBar().addMenu("&View")
        self.viewMenu.addAction(self.toolbar.toggleViewAction())
        self.viewMenu.addAction(self.statusbarAct)

        # Menu entry for help actions.
        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.contentsAct)
        self.helpMenu.addSeparator()
        self.helpMenu.addAction(self.aboutAct)

    def createStatusbar(self):
        """Create status bar and content."""
        self.statusBar()
        self.statusBar().showMessage("Ready.")

    def onOpen(self):
        """Select a test vector file using a file open dialog."""
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,
            "Open test vector file",
            os.getcwd(),
            "TestVector (*.txt);;All files (*)"
        )
        # Return if user did not select a file.
        if not filename:
            return
        self.loadDocument(filename)
        self.closeAct.setEnabled(self.mdiArea.count())

    def onClose(self):
        self.mdiArea.closeDocument()
        self.closeAct.setEnabled(self.mdiArea.count())

    def onQuit(self):
        self.close()

    def onToggleStatusBar(self):
        """Toggles the visibility of the status bar."""
        self.statusBar().setVisible(self.statusbarAct.isChecked())

    def onContents(self):
        url = 'http://gtmtca2.hephy.oeaw.ac.at/redmine/projects/tdf/wiki'
        QtWidgets.QMessageBox.information(self, "Contents", "<p>Please refer to: <a href=\"{0}\">{0}</a></p>".format(url))

    def onAbout(self):
        QtWidgets.QMessageBox.information(self, "About",
            "<p><strong>{}</strong></p><p>Graphical tool for viewing memory "
            "images. This software is written in Python3 using "
            "the PyQt5 toolkit.</p>"
            "<p>Version {}</p>"
            "<p>Authors: Bernhard Arnold <a href=\"mailto:bernhard.arnold"
            "@cern.ch\">&lt;bernhard.arnold@cern.ch&gt;</a></p>".format(self.AppTitle, self.AppVersion)
        )

    def loadDocument(self, filename):
        """Load document from filename."""
        filename = os.path.abspath(filename)
        if not os.path.isfile(filename):
            raise NoSuchFileError(filename)
        # Do not open files twice, just reload them.
        for index in range(self.mdiArea.count()):
            document = self.mdiArea.widget(index)
            if document:
                if filename == document.filename:
                    self.mdiArea.setCurrentIndex(index)
                    document.reload()
                    return
        # Else load from file and create new document tab.
        self.statusBar().showMessage("Loading...", 2500)
        document = Document(filename, self)
        index = self.mdiArea.addTab(document, QtGui.QIcon.fromTheme('ascii'), os.path.basename(filename))
        self.mdiArea.setCurrentIndex(index)
        self.statusBar().showMessage("Successfully loaded file", 2500)

        # Enable close action
        self.closeAct.setEnabled(self.mdiArea.count())

# -----------------------------------------------------------------------------
#  MDI Area class.
# -----------------------------------------------------------------------------

class MdiArea(QtWidgets.QTabWidget):

    def __init__(self, parent = None):
        super(MdiArea, self).__init__(parent)
        self.setDocumentMode(True)
        self.setTabsClosable(True)
        self.setMovable(True)

        # Close document by clicking on the tab close button.
        self.tabCloseRequested.connect(self.closeDocument)

    def currentDocument(self):
        return self.widget(self.currentIndex())

    def documents(self):
        for index in range(self.count()):
            yield self.widget(index)

    def closeDocument(self):
        """Close an document by index or current active document.
        Provided for convenience.
        """
        index = self.currentIndex()
        # Finally remove tab by index.
        self.removeTab(index)
        return True

# -----------------------------------------------------------------------------
#  Document class.
# -----------------------------------------------------------------------------

class Document(QtWidgets.QWidget):
    """Document widget displaying a data table view and a object preview box."""

    def __init__(self, filename, parent = None):
        super(Document, self).__init__(parent)
        self.filename = os.path.abspath(filename)
        self.tableView = self.createTableView()
        self.previewWidget = self.createPreviewWidget()
        self.warningLabel = self.createWarningLabel()
        self.reloadCount = 0
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(self.tableView)
        splitter.addWidget(self.previewWidget)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.warningLabel, 0)
        layout.addWidget(splitter, 1)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        # Load the file.
        QtCore.QCoreApplication.instance().processEvents()
        self.reload()

    def createTableView(self):
        """Create the data table view."""
        tableView = QtWidgets.QTableView(self)
        # Make only single cells selectable.
        tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        # Hide the default grid.
        tableView.setShowGrid(False)
        # Disable sorting.
        tableView.setSortingEnabled(False)
        # Set a monospace font for cell content (as hex values are displayed).
        tableView.setFont(QtGui.QFont("Monospace", 10))
        # Prevent resizing of the horizontal and vertical headers.
        horizontalHeader = tableView.horizontalHeader()
        horizontalHeader.setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        horizontalHeader.setStretchLastSection(True)
        verticalHeader = tableView.verticalHeader()
        verticalHeader.setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        verticalHeader.setDefaultSectionSize(20)
        return tableView

    def createPreviewWidget(self):
        textEdit = QtWidgets.QTextEdit(self)
        textEdit.setReadOnly(True)
        textEdit.setAutoFillBackground(True)
        return textEdit

    def createWarningLabel(self):
        label = QtWidgets.QLabel(self)
        label.setStyleSheet(
            "padding: 16px;"
            "border: 1px solid #ce8720;"
            "background-color: #f9ac3a;"
        )
        label.setWordWrap(True)
        label.hide()
        return label

    def reload(self):
        """Reload data from file."""
        image = self.loadFile(self.filename)
        model = DataTableModel(image, self)
        self.tableView.setModel(model)
        # <hack>
        # Make sure to not resize for 3564 lines but only for the first, the
        # row-count must be overwritten.
        # Replacing the class method by a temporary fake function.
        if not self.reloadCount:
            rowCount = model.rowCount
            def fakeRowCount(parent): return 1
            model.rowCount = fakeRowCount # replace
            self.tableView.resizeColumnsToContents()
            model.rowCount = rowCount # restore
        # </hack>
        self.tableView.update()
        # Attach signals to new assigned model instance.
        self.tableView.selectionModel().currentChanged.connect(self.updatePreview)
        self.clearWarning()
        self.reloadCount += 1

    def loadFile(self, filename):
        """Load image from different file types."""
        image = TestVector()
        # Set of read functions to try
        try:
            with open(self.filename) as f:
                image.read(f)
                return image
        except IOError:
            raise FileReadError(filename)
        # If no read attempt succeeded then bil out with an exception.
        raise UnknownFileTypeError(filename)

    def updatePreview(self, current, previous):
        """Update the object preview."""
        # Get the objects raw value.
        value = current.data(QtCore.Qt.UserRole)
        if value is None: return
        bx, column, fmt, value = value
        text = [
            "<p><strong>Object: {}</strong></p>".format(fmt.label()),
            "<p><strong>BX: {}</strong></p>".format(bx),
            "<p><strong>Value:</strong> 0x{}</p>".format(fmt.format(value)),
            "<hr/>",
        ]
        table = []
        for attr in fmt.attributes:
            table.append("".join([
                "<tr>",
                "<td><strong>{0}</strong></td>",
                "<td>{1}</td>",
                "<td>0x{1:x}</td>",
                "</tr>",
            ]).format(attr.name, attr.get(value)))
        if table:
            text.append("<table width=\"100%\">")
            text.extend([
                "<tr style=\"background-color: #eee;\">",
                "<th>Attribute</th>",
                "<th>Dec</th>",
                "<th>Hex</th>",
                "</tr>",
            ])
            text.extend(table)
            text.append("</table>")
        self.previewWidget.setHtml('\n'.join(text))

    def clearWarning(self):
        """Clear the warning badge located at the top of the document."""
        self.warningLabel.clear()
        self.warningLabel.hide()

    def showWarning(self, message):
        """Show a warning badge displaying a message located at the top of the document."""
        self.warningLabel.setText(message)
        self.warningLabel.show()

# -----------------------------------------------------------------------------
#  Data model
# -----------------------------------------------------------------------------

class DataTableModel(QtCore.QAbstractTableModel):

    def __init__(self, testvector, parent=None, *args):
        super(DataTableModel, self).__init__(parent, *args)
        self.testvector = testvector

    def rowCount(self, parent):
        return len(self.testvector.events)

    def columnCount(self, parent):
        return len(self.testvector.formats)

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        event = self.testvector.events[index.row()]
        fmt = self.testvector.formats[index.column()]
        value = event[index.column()]
        if role == QtCore.Qt.UserRole:
            return (index.row(), index.column(), fmt, value)
        if role == QtCore.Qt.DisplayRole:
            return fmt.format(value)
        return QtCore.QVariant()

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.testvector.formats[col].label())
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(col)
        return QtCore.QVariant()

# -----------------------------------------------------------------------------
#  Parsing command line arguments
# -----------------------------------------------------------------------------

def parse_args():
    """Parse command line arguments."""
    argp = argparse.ArgumentParser(prog="tdf-analyze", description="")
    argp.add_argument('filename', nargs="*", metavar='<file>', help="test vector file")
    argp.add_argument('-V, --version', action='version', version='%(prog)s {}'.format(__version__))
    return argp.parse_args()

# -----------------------------------------------------------------------------
#  Main routine
# -----------------------------------------------------------------------------

def main():
    """Main routine."""
    args = parse_args()

    # Create application and main window.
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # Open connections file using command line argument.
    for filename in args.filename:
        window.loadDocument(filename)

    # Workaround for CTRL+C termination

    # Terminate application on SIG_INT signal.
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Run timer once to catch SIG_INT signals.
    timer = QtCore.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    # Run execution loop.
    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())
