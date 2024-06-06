from PySide6 import (
    QtWidgets as qtw, 
    QtGui as qtg, 
    QtCore as qtc,
)
from PySide6.QtCore import Qt
from typing import Callable

class TableAutoComplete(qtw.QStyledItemDelegate):
    def __init__(self, list_fn: Callable[[None], list[str]]) -> None:
        super().__init__()
        self.list_fn = list_fn

    def createEditor(self, parent, option, index):
        editor = qtw.QLineEdit(parent)
        autoCompleter = qtw.QCompleter(self.list_fn(), parent)
        autoCompleter.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        autoCompleter.setFilterMode(Qt.MatchFlag.MatchContains)
        editor.setCompleter(autoCompleter)
        return editor
    
class CurrencyInputMask(qtw.QStyledItemDelegate):
    def __init__(self) -> None:
        super().__init__()

    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)
        if isinstance(editor, qtw.QLineEdit):
            validator = qtg.QRegularExpressionValidator(
                qtc.QRegularExpression(r"[0-9]*[.]{0,1}[0-9]{0,2}"), editor
            )
            editor.setValidator(validator)
        return editor
    
def align_text_right(item: qtw.QTableWidgetItem):
    item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
    return item