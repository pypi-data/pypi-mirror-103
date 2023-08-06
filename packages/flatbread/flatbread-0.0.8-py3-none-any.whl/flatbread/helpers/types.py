from typing import TypeVar, Hashable

AxisAlias = TypeVar('AxisAlias', str, int)
IndexName = TypeVar('IndexName', bound=Hashable)
LevelAlias = TypeVar('LevelAlias', int, IndexName)
