import pytest
from PyQt6.QtWidgets import QApplication, QVBoxLayout
from mediagui.gui import MainWindow

@pytest.fixture
def app():
    test_app = QApplication([])
    yield test_app
    test_app.quit()

def test_main_window(app, qtbot):
    window = MainWindow()
    qtbot.addWidget(window)

    # Check if the window title is set correctly
    assert window.windowTitle() == "mediaGUI"

    # Check if the minimum size is set correctly
    assert window.minimumSize().width() == 400
    assert window.minimumSize().height() == 400

    # Check if the central widget is set
    assert window.centralWidget() is not None

    # Check if the layout is set correctly
    layout = window.centralWidget().layout()
    assert layout is not None
    assert isinstance(layout, QVBoxLayout)