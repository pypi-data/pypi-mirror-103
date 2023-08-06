import os
import sys
import threading
from datetime import datetime
from multiprocessing import Process
from pathlib import Path

import click
import matplotlib
import numpy as np
from matplotlib import container
from matplotlib.backends.backend_qt5agg import FigureCanvas
# from matplotlib.backends.qt_compat import QtCore, QtGui, QtWidgets
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtGui, QtWidgets

matplotlib.use('Qt5Agg')

try:
    from aprespy.input import read
    from aprespy.navigation_toolbar import NavigationToolbar
except ModuleNotFoundError:
    from input import read
    from navigation_toolbar import NavigationToolbar


__title__ = 'Aprespy'
__version__ = '2021.4.1'


os.environ['QT_MAC_WANTS_LAYER'] = '1'


class Aprespy(QtWidgets.QWidget):
    """Summary."""

    XX = 0
    XY = 1
    YX = 2
    YY = 3
    TX = 0
    TY = 1
    MARK = ['o', 'o', 'x', 'x']
    COLOR = ['#009900', '#0000B3', '#B30000', '#CECE00']
    # COLOR = ['#5AB300', '#00B3B3', '#B30000', '#5A00B3']
    # COLOR = ['g', 'b', 'r', 'y']
    FACE_COLOR = '#EDEDED'

    def __init__(self, file_name, data):
        super(Aprespy, self).__init__()
        self.title = file_name
        self.data = data
        self.cur_rot = data.data[data.rotations.index(data.theta)]
        self.rotations = data.rotations
        self.theta = data.theta
        self.standard_axis = False
        self.error_guide = False
        self.diagonals = False
        self.error_guide_plots = []

        # Get the path to the img directory, need when bundling with pyinstaller
        if getattr(sys, 'frozen', False):
            # we are running in a bundle
            img_pth = os.path.join(sys._MEIPASS, 'img')
        elif os.path.exists('img'):
            img_pth = 'img'
        else:
            img_pth = os.path.join(os.path.dirname(__file__), 'img')

        self._init_ui(img_pth)
        self._init_layout()
        self._plot()
        self._legend()
        self._tipper_legend()

        # Initialize standard y axis
        self.standard_yaxis.click()

    def _init_ui(self, img_pth: str):
        self.setWindowTitle(f'{__title__} v{__version__}')
        self.setMinimumSize(800, 700)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.canvas = FigureCanvas(Figure(facecolor=self.FACE_COLOR))
        self.canvas.figure.set_size_inches(18, 12)
        self.toolbar = self._init_toolbar(img_pth)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)

    def _init_toolbar(self, img_pth: str):
        # Initialize buttons
        self.standard_yaxis = self._init_standard_yaxis(img_pth)
        self.diagonal = self._init_diagonal(img_pth)
        self.error_guide_button = self._init_error_guide(img_pth)
        self.rotation_ang = self._init_rotation_ang_label()
        self.rotation_slider = self._init_rotation_slider(self.rotations)

        # Add buttons to toolbar
        toolbar = NavigationToolbar(self.canvas, self)
        toolbar.addWidget(self.standard_yaxis)
        toolbar.addWidget(self.diagonal)
        toolbar.addWidget(self.error_guide_button)
        toolbar.addSeparator()
        toolbar.addWidget(self.rotation_ang)
        toolbar.addWidget(self.rotation_slider)

        # Connect the widgets
        self.standard_yaxis.toggled.connect(self._standard_yaxis_toggled)
        self.diagonal.toggled.connect(self._diagonal_toggled)
        self.error_guide_button.toggled.connect(self._error_guide_toggled)
        # self._rotation_slider.valueChanged.connect(self._slider_changed)
        self.rotation_slider.valueChanged.connect(self._rotation_angle_changed)
        # self._rotation_slider.sliderReleased.connect(self._rotation_angle_changed)

        return toolbar

    def _init_standard_yaxis(self, img_pth: str):
        # add default axis
        default_yaxis = QtWidgets.QToolButton()
        default_yaxis.setToolTip('Set standard rho yaxis')
        default_yaxis.setIcon(QtGui.QIcon(os.path.join(img_pth,
                                                       'default_axis.png')))
        default_yaxis.setCheckable(True)

        return default_yaxis

    def _init_rotation_ang_label(self):
        d = u"\u00b0"
        label = QtWidgets.QLabel(self)
        label.setText(f'{self.theta}{d}')
        label.setFixedWidth(45)
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        return label

    def _init_diagonal(self, img_pth: str):
        # add default axis
        diagonal = QtWidgets.QToolButton()
        diagonal.setToolTip('Toggle diagonal components')
        diagonal.setIcon(QtGui.QIcon(os.path.join(img_pth,
                                                  'diagonal.png')))
        diagonal.setCheckable(True)

        return diagonal

    def _init_error_guide(self, img_pth: str):
        # add default axis
        error_guide = QtWidgets.QToolButton()
        error_guide.setToolTip('Display error bar guide')
        error_guide.setIcon(QtGui.QIcon(os.path.join(img_pth,
                                                     'guide.png')))

        error_guide.setCheckable(True)

        return error_guide

    def _init_rotation_slider(self, rot: list = []):
        sl = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        sl.setFocusPolicy(QtCore.Qt.StrongFocus)
        sl.TickPosition(QtWidgets.QSlider.TicksBelow)
        sl.setRange(0, len(rot) - 1)
        # TODO: set initial slider value
        for i, ang in enumerate(self.rotations):
            # if d.measured_coor:
            if ang == self.theta:
                sl.setValue(i)
        return sl

    def _init_layout(self):
        d = u"\u00B7"
        gs = self.canvas.figure.add_gridspec(3, 5)
        self.axr = self.canvas.figure.add_subplot(gs[0:2, 0:3])
        self.axr.set_title(f'{self.title}', fontweight='bold')
        self.axr.set_ylabel('Resistivity (Ω m)', fontweight='bold')
        self.axr.tick_params(labelbottom=False)
        self._set_rotation_angle_labels()

        self.axr.set_xscale('log')
        self.axr.set_yscale('log')

        self.axp = self.canvas.figure.add_subplot(gs[2, 0:3], sharex=self.axr)
        self.axr.grid(True, which='major', linestyle='solid')
        self.axr.grid(True, which='minor', linestyle='dotted')
        self.axp.set_ylabel('Phase (°)', fontweight='bold')
        self.axp.set_xlabel('Period (s)', fontweight='bold')

        self.axp.yaxis.set_ticks(np.arange(-90, 91, 15))
        self.axp.set_ylim(ymin=-5, ymax=95)

        self.axp.grid(True, which='major', linestyle='solid')
        self.axp.grid(True, which='minor', linestyle='dotted')

        # TODO: Adjust base on the tipper values
        tlim = [-0.25, 0.25]
        ttik = [tlim[0] / 2, 0, tlim[1] / 2]
        self.atx = self.canvas.figure.add_subplot(gs[:, 3])
        self.atx.set_yscale('log')
        self.atx.set_xlim(xmin=tlim[0], xmax=tlim[1])
        self.atx.xaxis.set_ticks(ttik)
        self.atx.set_xticklabels(ttik, fontsize=8)
        self.atx.set_ylim(ymin=40_000, ymax=4)
        self.atx.tick_params(labelleft=False)
        self.atx.set_xlabel('|Tzx|', fontweight='bold')
        self.atx.grid(True, which='major', linestyle='dashed')

        self.aty = self.canvas.figure.add_subplot(gs[:, 4], sharey=self.atx)
        self.aty.set_xlabel('|Tzy|', fontweight='bold')
        self.aty.grid(True, which='major', linestyle='dashed')
        self.aty.set_xlim(xmin=tlim[0], xmax=tlim[1])
        self.aty.xaxis.set_ticks(ttik)
        self.aty.set_xticklabels(ttik, fontsize=8)
        self.aty.yaxis.tick_right()
        self.aty.yaxis.set_label_position('right')
        self.aty.set_ylabel('Period (s)', fontweight='bold')

    def _plot(self):
        if self.error_guide:
            self._plot_error_guide(self.XY)
        if self.diagonals:
            self.rxx, self.pxx = self._plot_curves('Zxx', self.XX)
            self.ryy, self.pyy = self._plot_curves('Zyy', self.YY)
        self.rxy, self.pxy = self._plot_curves('Zxy', self.XY)
        self.ryx, self.pyx = self._plot_curves('Zyx', self.YX)
        self.zxr, self.zxi = self._plot_tipper(self.atx, self.TX)
        self.zyr, self.zyi = self._plot_tipper(self.aty, self.TY)

    def _plot_curves(self, label, position):
        rho = self._plot_line(self.axr,
                              self.data.periods,
                              self.cur_rot.rho[:, position],
                              None,
                              self.cur_rot.rho_se[:, position],
                              self.MARK[position],
                              self.COLOR[position],
                              label)
        phi = self._plot_line(self.axp,
                              self.data.periods,
                              self.cur_rot.phi[:, position],
                              None,
                              self.cur_rot.phi_se[:, position],
                              self.MARK[position],
                              self.COLOR[position],
                              label)

        return rho, phi

    def _plot_tipper(self, plot, position):
        real = self._plot_line(plot,
                               self.cur_rot.tz[:, position].real,
                               self.data.periods,
                               self.cur_rot.tz_se[:, position].real,
                               None,
                               self.MARK[self.XY],
                               'm',
                               'Re(Tz)')
        imag = self._plot_line(plot,
                               self.cur_rot.tz[:, position].imag,
                               self.data.periods,
                               self.cur_rot.tz_se[:, position].real,
                               None,
                               self.MARK[self.YX],
                               'k',
                               'Im(Tz)')

        if self.cur_rot.tz.shape[0] > 23:
            trmid = self.cur_rot.tz[14:24, position].real
            trmax = np.abs(max(trmid))
            trmin = np.abs(min(trmid))
            trmm = max([trmax, trmin])
            if trmm < 0.25:
                tbounds = [-0.25, 0.25]
                ttik = [tbounds[0] / 2, 0, tbounds[1] / 2]
            elif trmm < 0.5 and trmm > 0.25:
                tbounds = [-0.5, 0.5]
                ttik = [tbounds[0] / 2, 0, tbounds[1] / 2]
            elif trmm < 0.75 and trmm > 0.5:
                tbounds = [-0.75, 0.75]
                ttik = [tbounds[0] / 2, 0, tbounds[1] / 2]
            else:
                tbounds = [-1, 1]
                ttik = [tbounds[0] / 2, 0, tbounds[1] / 2]

            plot.set_xlim(xmin=tbounds[0], xmax=tbounds[1])
            plot.xaxis.set_ticks(ttik)
            plot.set_xticklabels(ttik, fontsize=8)

        return real, imag

    def _plot_error_guide(self, position):
        self.error_guide_plots = []
        start = 4
        end = 29
        periods = self.data.periods[start:end]
        zxy = self.cur_rot.rho[start:end, self.XY]
        zyx = self.cur_rot.rho[start:end, self.YX]
        error = np.zeros(zyx.shape)
        zxy_guide = [np.zeros(zyx.shape), np.zeros(zyx.shape)]
        zyx_guide = [np.zeros(zyx.shape), np.zeros(zyx.shape)]
        for i in range(error.shape[0]):
            zxy_guide[0][i] = zxy[i] - zxy[i] * 0.05
            zxy_guide[1][i] = zxy[i] + zxy[i] * 0.05
            zyx_guide[0][i] = zyx[i] - zyx[i] * 0.05
            zyx_guide[1][i] = zyx[i] + zyx[i] * 0.05

        zxy_fill = self.axr.fill_between(
            periods, zxy_guide[0], zxy_guide[1], color='k', alpha=0.05)
        zyx_fill = self.axr.fill_between(
            periods, zyx_guide[0], zyx_guide[1], color='k', alpha=0.05)
        zxy_low, = self.axr.plot(
            periods, zxy_guide[0], color='k', linewidth=0.25)
        zxy_high, = self.axr.plot(
            periods, zxy_guide[1], color='k', linewidth=0.25)
        zyx_low, = self.axr.plot(
            periods, zyx_guide[0], color='k', linewidth=0.25)
        zyx_high, = self.axr.plot(
            periods, zyx_guide[1], color='k', linewidth=0.25)
        self.error_guide_plots.append(zxy_fill)
        self.error_guide_plots.append(zyx_fill)
        self.error_guide_plots.append(zxy_low)
        self.error_guide_plots.append(zxy_high)
        self.error_guide_plots.append(zyx_low)
        self.error_guide_plots.append(zyx_high)

        pxy = self.cur_rot.phi[start:end, self.XY]
        pyx = self.cur_rot.phi[start:end, self.YX]
        pxy_fill = self.axp.fill_between(
            periods, pxy - 2, pxy + 2, color='k', alpha=0.05)
        pyx_fill = self.axp.fill_between(
            periods, pyx - 2, pyx + 2, color='k', alpha=0.05)
        pxy_low, = self.axp.plot(periods, pxy - 2, color='k', linewidth=0.25)
        pxy_high, = self.axp.plot(periods, pxy + 2, color='k', linewidth=0.25)
        pyx_low, = self.axp.plot(periods, pyx - 2, color='k', linewidth=0.25)
        pyx_high, = self.axp.plot(periods, pyx + 2, color='k', linewidth=0.25)
        self.error_guide_plots.append(pxy_fill)
        self.error_guide_plots.append(pyx_fill)
        self.error_guide_plots.append(pxy_low)
        self.error_guide_plots.append(pxy_high)
        self.error_guide_plots.append(pyx_low)
        self.error_guide_plots.append(pyx_high)

    def _plot_line(self, plot, x: np.array, y: np.array, x_err: np.array, y_err: np.array,
                   marker: str, color: str, label: str):
        line = plot.errorbar(x, y, xerr=x_err, yerr=y_err, color=color,
                             marker=marker, linestyle='none', mfc='none',
                             capsize=3, label=label)
        return line

    def _legend(self):
        # Define the initial handle labels and order
        label_set = ['Zxy', 'Zyx']
        if self.diagonals:
            label_set = ['Zxx'] + label_set + ['Zyy']

        # Get line handles and labels from the graph
        handles, labels = self.axr.get_legend_handles_labels()
        # Remove the duplicate handles/labels and reorder
        handles = [handles[labels.index(i)] for i in label_set]
        labels = [labels[labels.index(i)] for i in label_set]
        # Remove the error bars from the legend symbols
        handles = [h[0] if isinstance(
            h, container.ErrorbarContainer) else h for h in handles]

        legend = self.axr.legend(handles, labels, loc='upper left')
        legend.set_draggable(state=True)

    def _tipper_legend(self):
        plot = self.aty
        label_set = ['Re(Tz)', 'Im(Tz)']

        # Get line handles and labels from the graph
        handles, labels = plot.get_legend_handles_labels()
        # Remove the duplicate handles/labels and reorder
        handles = [handles[labels.index(i)] for i in label_set]
        labels = [labels[labels.index(i)] for i in label_set]
        # Remove the error bars from the legend symbols
        handles = [h[0] if isinstance(
            h, container.ErrorbarContainer) else h for h in handles]

        legend = plot.legend(handles, labels, loc='upper left')
        legend.set_draggable(state=True)

    def _set_rotation_angle_labels(self):
        d = u"\u00b0"
        self.rotation_ang.setText(f'{self.theta}{d}')
        self.axr.set_xlabel(f'Geodetic Rotation: {self.theta}{d}')

    def _standard_yaxis_toggled(self, checked: bool):
        if checked:
            self.standard_axis = True
            self._set_rho_y_axis()
        else:
            self.standard_axis = False
            self._reload_graphs()

    def _diagonal_toggled(self, checked: bool):
        if checked:
            self.diagonals = True
            self._reload_graphs()
        else:
            self.diagonals = False
            self._reload_graphs()

    def _error_guide_toggled(self, checked: bool):
        if checked:
            self.error_guide = True
            self._reload_graphs()
        else:
            self.error_guide = False
            self._reload_graphs()

    def _set_rho_y_axis(self):
        self.standard_axis = True
        median = int(np.median(self.cur_rot.rho[:, self.XY]) +
                     np.median(self.cur_rot.rho[:, self.YX]))
        median = int(median / 2)
        self.axr.set_ylim(ymin=median / 100, ymax=median * 100)
        self.canvas.draw()

    def _slider_changed(self):
        self.theta = self.rotations[self._rotation_slider.value()]
        self._set_rotation_angle_labels()

    def _rotation_angle_changed(self):
        self.theta = self.rotations[self.rotation_slider.value()]
        self.cur_rot = self.data.data[self.rotations.index(self.theta)]
        self._set_rotation_angle_labels()
        self._reload_graphs()

    def _reload_graphs(self):
        try:
            for line in self.error_guide_plots:
                line.remove()
        except (AttributeError, ValueError):
            pass
        try:
            self.rxx.remove()
            self.ryy.remove()
            self.pxx.remove()
            self.pyy.remove()
        except (AttributeError, ValueError):
            pass
        self.rxy.remove()
        self.ryx.remove()
        self.pxy.remove()
        self.pyx.remove()
        self.zxr.remove()
        self.zxi.remove()
        self.zyr.remove()
        self.zyi.remove()
        self._plot()
        self._legend()
        if self.standard_axis:
            self._set_rho_y_axis()
        else:
            self.axr.autoscale()
            self.canvas.draw()

        self.canvas.flush_events()

    def save(self, path: str = None):
        file_dir = ''
        file_name = Path(self.title).stem + '.png'

        if path is not None:
            try:
                path = Path(path)
                path = path.parent.parent
                file_dir = os.path.join(path, 'plot')
                if not os.path.exists(file_dir):
                    os.makedirs(file_dir)
            except OSError:
                file_dir = ''

        file_path = os.path.join(file_dir, file_name)

        print(f'Saving image: {file_path}')

        self.canvas.figure.set_size_inches(18, 12)
        self.canvas.figure.savefig(file_path, dpi=100)


def file_dialog(prev_dir: str = str(Path.home())):
    file_path, _ = QtWidgets.QFileDialog.getOpenFileName(None,
                                                         'Open File dialog',
                                                         prev_dir,
                                                         filter='((*.zss *.zrr)'
                                                         )
    if file_path != '':
        return file_path


def plot(file_path: str = None, save: bool = False, quit: bool = False):
    app = Process(target=application, args=(file_path, save, quit,))
    app.start()
    app.join()


def application(file_path: str = None, save: bool = False, quit: bool = False):
    app = QtWidgets.QApplication(sys.argv)
    if file_path is None:
        file_path = file_dialog()
        if file_path is None:
            sys.exit()

    if not os.path.exists(file_path):
        print(f'File not found: {file_path}')
        sys.exit()

    file_name = Path(file_path).name
    print(f'Reading file: {file_path}')
    data = read(file_path)

    window = Aprespy(file_name, data)
    if save is True:
        window.save(file_path)

    if quit is True:
        sys.exit()

    window.show()
    sys.exit(app.exec_())


def save_no_gui(path: str = None):
    plot(path, save=True, quit=True)


def wait_for_file(path: str = None):
    SECONDS = 20
    if str is None:
        return None

    start = datetime.now()
    print('Waiting for file...')
    while True:
        if os.path.exists(path):
            break
        elif (datetime.now() - start).total_seconds() > 10:
            print(f'ERROR: {SECONDS} seconds have passed, Exiting')
            break


@click.command()
@click.option('-p', '--path', help='zss/zrr file path')
@click.option('-s', '--save', is_flag=True, help='save png file')
@click.option('-ng', '--no_gui', is_flag=True, help='exit without displaying the gui')
@click.option('-ss', '--ss', is_flag=True, help='flag to check if it is running in matlab SS mode')
def main(path: str = None, save: bool = False, no_gui: bool = False, ss: bool = False):
    if ss is True and path is not None:
        wait_for_file(path)
    plot(path, save, no_gui)


if __name__ == "__main__":
    main()
