import sys
import napari 
from napari import Viewer, gui_qt
from cellpose_napari._dock_widget import widget_wrapper

def main():
    fns = sys.argv[1:]
    viewer = Viewer()
    if len(fns) > 0:
        viewer.open(fns, stack=False)
    viewer.window.add_dock_widget(widget_wrapper(), area='right')
    napari.run()

if __name__ == '__main__':
    main()