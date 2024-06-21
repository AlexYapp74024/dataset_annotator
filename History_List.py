import sys
import typing
import builtins
from enum import Enum
from typing import *

from dataclasses import dataclass
_T = TypeVar("_T")

class ChangeType(Enum):
    ADD = 0
    REMOVE = 1
    CHNAGE = 2

ADD = ChangeType.ADD
REMOVE = ChangeType.REMOVE
CHNAGE = ChangeType.CHNAGE

@dataclass
class Change():
    operation: int
    indices: Iterable
    prev_val: List[_T]|None

class HistoryList(list, MutableSequence[_T]):
    
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], Iterable):
            super().__init__(*args)
        else:
            super().__init__(args)

        self.hist : List[Change] = []
        self.undoing = False

    def clear_history(self):
        self.hist.clear()

    def undo(self):
        try:
            self.undoing = True
            last_change = self.hist.pop()

            match last_change.operation:
                case ChangeType.ADD:
                    for i in last_change.indices: del self[i]
                
                case ChangeType.REMOVE:
                    for i, obj in zip(last_change.indices, last_change.prev_val): 
                        self.insert(i,obj)
                
                case ChangeType.CHNAGE:
                    for i, obj in zip(last_change.indices, last_change.prev_val): 
                        self[i] = obj
            
        except Exception as e:
            raise e
        
        finally:
            self.undoing = False

    def append(self, object: _T, /) -> None: 
        if not self.undoing: self.hist.append(Change(ADD, (len(self),), None))
        super().append(object)

    def extend(self, iterable: Iterable[_T], /) -> None: 
        raise NotImplementedError

    def pop(self, index: SupportsIndex = -1, /) -> _T: 
        if not self.undoing: self.hist.append(Change(REMOVE, (index,), (self[index],)))
        return super().pop(index)

    def insert(self, index: SupportsIndex, object: _T, /) -> None: 
        if not self.undoing: self.hist.append(Change(ADD, (index,), None))
        super().insert(index, object)

    def remove(self, value: _T, /) -> None: 
        raise NotImplementedError

    def sort(self: list,    *, key: None = None, reverse: bool = False) -> None: 
        raise NotImplementedError

    def __setitem__(self, key: SupportsIndex|slice, value: _T, /) -> None: 
        if not self.undoing: 
            match type(key):
                case builtins.int: 
                    self.hist.append(Change(CHNAGE, (key,), (self[key],)))
                case builtins.slice:
                    raise NotImplementedError
        super().__setitem__(key,value)
    
    def __delitem__(self, key: SupportsIndex | slice, /) -> None: 
        if not self.undoing:
            match type(key):
                case builtins.int: 
                    self.hist.append(Change(REMOVE, (key,), (self[key],)))
                case builtins.slice:
                    self.hist.append(Change(REMOVE, range(len(self))[key], self[key]))

        super().__delitem__(key)

    def __add__(self, value: list[_T], /) -> list[_T]: 
        raise NotImplementedError
    def __iadd__(self, value: Iterable[_T], /) -> Self: 
        raise NotImplementedError  # type: ignore[misc]
    def __mul__(self, value: SupportsIndex, /) -> list[_T]: 
        raise NotImplementedError
    def __rmul__(self, value: SupportsIndex, /) -> list[_T]: 
        raise NotImplementedError
    def __imul__(self, value: SupportsIndex, /) -> Self: 
        raise NotImplementedError
    
    def __iter__(self) -> Iterator[_T]:
        a = super().__iter__()
        return super().__iter__()
    
