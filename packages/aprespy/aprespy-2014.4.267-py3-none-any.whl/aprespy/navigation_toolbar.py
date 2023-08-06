from os.path import join

import matplotlib as mpl
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.backends.qt_compat import QtCore, QtWidgets


class NavigationToolbar(NavigationToolbar2QT):
    """Inherating from NavigationToolbar2QT."""

    # def _init_toolbar(self):
    def __init__(self, canvas, parent):
        """Override NavigationToolbar2QT _init_toolbar method."""
        super(NavigationToolbar, self).__init__(canvas, parent)

        # self.basedir = os.path.join(matplotlib.rcParams['datapath'], 'images')
        join(mpl.get_data_path(), 'images')

        # Clear the toolbar buttons, start with clean bar
        for x in self.actions():
            self.removeAction(x)

        # only display the buttons we want
        self.toolitems = [t for t in NavigationToolbar2QT.toolitems if
                          t[0] in ('Home', 'Pan', 'Zoom', 'Save', None)]

        for text, tooltip_text, image_file, callback in self.toolitems:
            if text is None:
                self.addSeparator()
            else:
                a = self.addAction(self._icon(image_file + '.png'),
                                   text, getattr(self, callback))
                self._actions[callback] = a
                if callback in ['zoom', 'pan']:
                    a.setCheckable(True)
                if tooltip_text is not None:
                    a.setToolTip(tooltip_text)
                if text == 'Zoom':
                    a = self.addAction(self._icon("subplots.png"),
                                       'Customize', self.edit_parameters)
                    a.setToolTip('Edit axis, curve and image parameters')

        # # self.buttons = {}

        # Add the x,y location widget at the right side of the toolbar
        # The stretch factor is 1 which means any resizing of the toolbar
        # will resize this label instead of the buttons.
        if self.coordinates:
            self.locLabel = QtWidgets.QLabel("", self)
            self.locLabel.setAlignment(
                QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
            self.locLabel.setSizePolicy(
                QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                      QtWidgets.QSizePolicy.Ignored))
            labelAction = self.addWidget(self.locLabel)
            labelAction.setVisible(False)

        # # reference holder for subplots_adjust window
        # # self.adj_window = None

        # # Esthetic adjustments - we need to set these explicitly in PyQt5
        # # otherwise the layout looks different - but we don't want to set it if
        # # not using HiDPI icons otherwise they look worse than before.
        self.setIconSize(QtCore.QSize(24, 24))
        self.layout().setSpacing(12)
