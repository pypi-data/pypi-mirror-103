"""
cellpose dock widget module
"""
from napari_plugin_engine import napari_hook_implementation
from qtpy.QtWidgets import QWidget, QHBoxLayout, QPushButton
from magicgui import magic_factory


import sys, pathlib, os, time
import numpy as np
import cv2
from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QLabel, QTextBrowser
from PyQt5 import QtCore

import napari 
import napari.utils.notifications
from napari import Viewer, gui_qt
from napari.qt.threading import thread_worker
from napari.layers import Image, Shapes
from napari_plugin_engine import napari_hook_implementation
from magicgui import magicgui, magic_factory

from cellpose.models import CellposeModel, Cellpose
from cellpose.utils import masks_to_outlines, fill_holes_and_remove_small_masks
from cellpose.dynamics import get_masks
from cellpose.transforms import resize_image

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from cellpose.__main__ import logger_setup
import logging

logger, log_file = logger_setup()

class TextWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(800,400)
        self.label = QtWidgets.QLabel('keep open to see cellpose run info')
        self.logTextBox = QtWidgets.QPlainTextEdit(self)
        self.logTextBox.setReadOnly(True)
        self.cursor = self.logTextBox.textCursor()
        self.cursor.movePosition(self.cursor.End)    
        
        layout = QtWidgets.QVBoxLayout()
        # Add the new logging box widget to the layout
        layout.addWidget(self.label)
        layout.addWidget(self.logTextBox)
        self.setLayout(layout)
        self.show()
#if not hasattr(widget, 'logger'):
#    widget.logger = TextWindow()
#    widget.logger.show()
#    log_worker = read_logging(log_file, widget.logger)
#    log_worker.start()

@thread_worker
def read_logging(log_file, logwindow):
    with open(log_file, 'r') as thefile:
        #thefile.seek(0,2) # Go to the end of the file
        while True:
            line = thefile.readline()
            if not line:
                time.sleep(0.01) # Sleep briefly
                continue
            else:
                logwindow.cursor.movePosition(logwindow.cursor.End)
                logwindow.cursor.insertText(line)
                yield line
            
main_channel_choices = [('average all channels', 0), ('0=red', 1), ('1=green', 2), ('2=blue', 3),
                        ('3', 4), ('4', 5), ('5', 6), ('6', 7), ('7', 8), ('8', 9)]
optional_nuclear_channel_choices = [('none', 0), ('0=red', 1), ('1=green', 2), ('2=blue', 3),
                                    ('3', 4), ('4', 5), ('5', 6), ('6', 7), ('7', 8), ('8', 9)]

@thread_worker
def run_cellpose(image, model_type, custom_model, channels, diameter,
                 net_avg, resample, cellprob_threshold, 
                 model_match_threshold, do_3D, stitch_threshold):
    flow_threshold = (31.0 - model_match_threshold) / 10.
    if model_match_threshold==0.0:
        flow_threshold = 0.0
        logger.info('flow_threshold=0 => no masks thrown out due to model mismatch')
    logger.info(f'computing masks with cellprob_threshold={cellprob_threshold}, flow_threshold={flow_threshold}')
    pretrained_model = custom_model if model_type=='custom' else model_type
    CP = CellposeModel(pretrained_model=pretrained_model, gpu=True)
    masks, flows_orig, _ = CP.eval(image, 
                                   channels=channels, 
                                   channels_last=True,
                                   diameter=diameter,
                                   net_avg=net_avg,
                                   resample=resample,
                                   cellprob_threshold=cellprob_threshold,
                                   flow_threshold=flow_threshold,
                                   do_3D=do_3D,
                                   stitch_threshold=stitch_threshold)
    del CP 
    segmentation = (masks, flows_orig)
    return segmentation

@thread_worker
def compute_diameter(image, channels, model_type):
    CP = Cellpose(model_type = model_type, gpu=True)
    diam = CP.sz.eval(image, channels=channels, channels_last=True)[0]
    diam = np.around(diam, 2)
    del CP
    return diam

@thread_worker 
def compute_masks(masks_orig, flows_orig, cellprob_threshold, model_match_threshold):
    flow_threshold = (31.0 - model_match_threshold) / 10.
    if model_match_threshold==0.0:
        flow_threshold = 0.0
        logger.info('flow_threshold=0 => no masks thrown out due to model mismatch')
    logger.info(f'computing masks with cellprob_threshold={cellprob_threshold}, flow_threshold={flow_threshold}')
    maski = get_masks(flows_orig[3].copy(), iscell=(flows_orig[2] > cellprob_threshold),
                      flows=flows_orig[1], threshold=flow_threshold)
    if flows_orig[1].ndim < 4:
        maski = fill_holes_and_remove_small_masks(maski)
    maski = resize_image(maski, masks_orig.shape[-2], masks_orig.shape[-1],
                                    interpolation=cv2.INTER_NEAREST)
    return maski 

#logo = os.path.join(__file__, 'logo/logo_small.png')
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QFileDialog, QProgressBar, QHBoxLayout, QGroupBox
from napari_plugin_engine import napari_hook_implementation
from pathlib import Path
from PyQt5 import QtCore
from magicgui.widgets import FunctionGui, create_widget

def my_function(a):
    return a

class MyGui(FunctionGui):
    def __init__(self,viewer: napari.viewer.Viewer,
            image: Image
          ):
        param_options = (label_head = dict(widget_type='Label', label=f'<h2> cellpose </h2>'), 
            model_type = dict(widget_type='ComboBox', label='model type', choices=['cyto', 'nuclei', 'custom'], value='cyto', tooltip='model type'),
            custom_model = dict(widget_type='FileEdit', label='custom model path: '),
            main_channel = dict(widget_type='ComboBox', label='channel to segment', choices=main_channel_choices, value=0, tooltip='model type'),
            optional_nuclear_channel = dict(widget_type='ComboBox', label='optional nuclear channel', choices=optional_nuclear_channel_choices, value=0, tooltip='model type'),
            diameter = dict(widget_type='LineEdit', label='diameter', value=30),
            compute_diameter_shape  = dict(widget_type='PushButton', text='compute diameter from shape layer'),
            compute_diameter_button  = dict(widget_type='PushButton', text='compute diameter from image'),
            cellprob_threshold = dict(widget_type='FloatSlider', name='cellprob_threshold', value=0.0, min=-8.0, max=8.0, step=0.2),
            model_match_threshold = dict(widget_type='FloatSlider', name='model_match_threshold', value=27.0, min=0.0, max=30.0, step=0.2, tooltip='threshold on gradient match to accept a mask (set lower to get more cells)'),
            compute_masks_button  = dict(widget_type='PushButton', text='recompute last masks with new cellprob + model match', enabled=False),
            net_average = dict(widget_type='CheckBox', text='average 4 nets', value=True),
            resample_dynamics = dict(widget_type='CheckBox', text='resample dynamics', value=False),
            process_3D = dict(widget_type='CheckBox', text='process stack as 3D', value=False, tooltip='use default 3D processing where flows in X, Y, and Z are computed and dynamics run in 3D to create masks'),
            stitch_threshold_3D = dict(widget_type='LineEdit', label='stitch threshold slices', value=0, tooltip='across time or Z, stitch together masks with IoU threshold of "stitch threshold" to create 3D segmentation'),
            clear_previous_segmentations = dict(widget_type='CheckBox', text='clear previous results', value=True),
            output_flows = dict(widget_type='CheckBox', text='output flows and cellprob', value=True),
            output_outlines = dict(widget_type='CheckBox', text='output outlines', value=True))
        super().__init__(
          my_function,
          call_button=True,
          layout='vertical',
          param_options=param_options
            )
        print('init')

class MyWidget(QWidget):
    def __init__(self,viewer: napari.viewer.Viewer,
            image: Image
          ):
    super().__init__()
    

@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return MyWidget

