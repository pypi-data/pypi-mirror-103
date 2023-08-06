"""
Functions for transforming table data into percentages and optionally
adding it alongside the original data.
"""

from functools import wraps, partial
from typing import Any

import pandas as pd # type: ignore

import flatbread.config as config
import flatbread.utils as utils
import flatbread.utils.log as log
import flatbread.axes as axes
import flatbread.levels as levels
import flatbread.aggregate.totals as totals
import flatbread.build.table as table
from flatbread.aggregate import AGG_SETTINGS


def round_percentages(
    s: pd.Series,
    ndigits: int = -1
) -> pd.Series:
    """
    Round percentages in a way that they always add up to 100%.
    Taken from `this SO answer <https://stackoverflow.com/a/13483486/10403856>`_
    """
    if ndigits < 0:
        return s
    cumsum = s.fillna(0).cumsum().round(ndigits)
    prev_baseline = cumsum.shift(1).fillna(0)
    return cumsum - prev_baseline


@log.entry
@config.load_settings(AGG_SETTINGS)
# @axes.get_axis_number
# @levels.get_level_number
def add(
    df:            pd.DataFrame,
    *,
    axis:           Any  = 0,
    level:          Any  = 0,
    ndigits:        int  = None,
    unit:           int  = 100,
    label_abs:      str  = None,
    label_rel:      str  = None,
    add_labels_to:  str  = None,
    totals_name:    str  = None,
    subtotals_name: str  = None,
    drop_totals:    bool = False,
    **kwargs
) -> pd.DataFrame:
    """
    Add percentages to ``df`` on ``level`` of ``axis`` rounded to ``ndigits``.

    This operation will result in a table containing the absolute values as well
    as the percentage values. The absolute and percentage columns will be
    labelled by an added level to the column index.

    (Sub)totals are required to calculate the percentages. If (sub)totals are
    present (``totals_name`` and ``subtotals_name`` are used to identify totals
    within the table) these will be used. When no (sub)totals are found, they
    will be added to the table. Set ``drop_totals`` to False to exlude them from
    the output.

    Set ``unit`` in order to calculate other fractions.

    Arguments
    ---------
    df : pd.DataFrame
    axis : {0 or 'index', 1 or 'columns', 2 or 'all'}, default 0
        Axis to use for calculating the percentages:

        * 0 : percentages of each row by the column totals
        * 1 : percentages of each column by the row totals
        * 2 : percentages of each field by the table total
    level : int, level name, default 0
        Level number or name for the level on which to calculate the
        percentages. Level 0 uses row/column totals, otherwise subtotals within
        the specified level are used.
    ndigits : int, default 1
        Number of digits used for rounding the percentages.
        Set to -1 for no rounding.
    unit : int, default 100,
        Unit of prevalence.
    label_abs : str, default 'abs'
        Value used for labelling the absolute columns.
    label_rel : str, default 'rel'
        Value used for labelling the relative columns.
    add_label_to : str, default 'bottom'
    totals_name : str, default 'Total'
        Name identifying the row/column totals.
    subtotals_name : str, default 'Subtotal'
        Name identifying the row/column subtotals.
    drop_totals : bool, default False
        Drop row/column totals from output.

    Returns
    -------
    pd.DataFrame
        DataFrame with added percentages.
    """
    # get_axis = lambda x: axes._get_axis_number(x) if pd.api.types.is_scalar(x) else x
    # axis = get_axis(axis)
    axis = axes._get_axis_number(axis)

    pct = df.pipe(
        transform,
        axis           = axis,
        level          = level,
        ndigits        = ndigits,
        unit           = unit,
        totals_name    = totals_name,
        subtotals_name = subtotals_name,
        drop_totals    = drop_totals,
    )
    df = df.pipe(
        totals._add_totals,
        axis  = axis,
        level = level,
    )
    if drop_totals:
        df = df.pipe(
            totals._drop_totals,
            axis           = axis,
            level          = level,
            totals_name    = totals_name,
            subtotals_name = subtotals_name,
        )
    df = table.combine_dfs(
        df,
        pct,
        label_abs,
        label_rel,
        add_labels_to=add_labels_to,
    )
    return df


@log.entry
@utils.copy
@config.load_settings(AGG_SETTINGS)
# @axes.get_axis_number
# @levels.get_level_number
def transform(
    df: pd.DataFrame,
    *,
    axis:           Any  = 0,
    level:          Any  = 0,
    ndigits:        int  = None,
    unit:           int  = 100,
    totals_name:    str  = None,
    subtotals_name: str  = None,
    drop_totals:    bool = False,
    **kwargs
) -> pd.DataFrame:
    """
    Transform values of ``df`` to percentages on ``level`` of ``axis`` rounded
    to ``ndigits``.

    (Sub)totals are required to calculate the percentages. If (sub)totals are
    present (``totals_name`` and ``subtotals_name`` are used to identify totals
    within the table) these will be used. When no (sub)totals are found, they
    will be added to the table. Set ``drop_totals`` to False to exlude them from
    the output.

    Set ``unit`` in order to calculate other fractions.

    Arguments
    ---------
    df : pd.DataFrame
    axis : {0 or 'index', 1 or 'columns', 2 or 'all'}, default 0
        Axis to use for calculating the percentages:

        * 0 : percentages of each row by the column totals
        * 1 : percentages of each column by the row totals
        * 2 : percentages of each field by the table total
    level : int, level name, default 0
        Level number or name for the level on which to calculate the
        percentages. Level 0 uses row/column totals, otherwise subtotals within
        the specified level are used.
    ndigits : int, default 1
        Number of digits used for rounding the percentages.
        Set to -1 for no rounding.
    unit : int, default 100,
        Unit of prevalence.
    totals_name : str, default 'Total'
        Name identifying the row/column totals.
    subtotals_name : str, default 'Subtotal'
        Name identifying the row/column subtotals.
    drop_totals : bool, default False
        Drop row/column totals from output.

    Returns
    -------
    pd.DataFrame
        DataFrame with added percentages.
    """
    f = partial(levels._get_level_number, df)
    is_scalar = pd.api.types.is_scalar
    get_axis = lambda x: axes._get_axis_number(x) if is_scalar(x) else x
    get_level = lambda x, y: f(x, y) if is_scalar(x) else x

    axis = get_axis(axis)
    get_level = get_level(axis, level)

    settings = dict(
        ndigits        = ndigits,
        unit           = unit,
        totals_name    = totals_name,
        subtotals_name = subtotals_name,
        drop_totals    = drop_totals,
    )
    kwargs.update(settings)
    if isinstance(axis, int):
        if axis < 2:
            return _axis_wise(df, axis=axis, level=level, **kwargs)
        else:
            return _table_wise(df, level=level, **kwargs)
    else:
        return _table_wise_multilevel(
            df,
            axlevels = axis,
            **kwargs
        )


@axes.transpose
@totals.add_totals(axis=0)
@totals.drop_totals(axis=0)
def _axis_wise(
    df:             pd.DataFrame,
    level:          int,
    totals_name:    str,
    subtotals_name: str,
    ndigits:        int,
    unit:           int,
    **kwargs
) -> pd.DataFrame:
    if level > 0:
        totals_name = subtotals_name
    if isinstance(df.index, pd.MultiIndex):
        totals = (
            df.xs(totals_name, level=level, drop_level=False)
            .reindex(df.index)
            .bfill()
        )
    else:
        totals = df.loc[totals_name]
    result = df.div(totals).multiply(unit)
    return result.pipe(round_percentages, ndigits=ndigits)


@totals.add_totals(axis=0)
@totals.add_totals(axis=1)
@totals.drop_totals(axis=0)
@totals.drop_totals(axis=1)
def _table_wise(
    df:             pd.DataFrame,
    level:          int,
    subtotals_name: str,
    ndigits:        int,
    unit:           int,
    **kwargs
) -> pd.DataFrame:
    if level == 0:
        totals = df.iloc[-1, -1]
        if df.index.nlevels > 1 or df.columns.nlevels > 1:
            frame = pd.DataFrame().reindex_like(df)
            frame.iloc[-1, -1] = totals
            totals = frame.bfill().bfill(axis=1)
    else:
        totals = (
            df.xs(subtotals_name, level=level, drop_level=False)
            .xs(subtotals_name, axis=1, level=level, drop_level=False)
            .reindex_like(df).bfill().bfill(axis=1)
        )
    result = df.div(totals).multiply(unit)
    return result.pipe(round_percentages, ndigits=ndigits)


@totals.add_totals(axis=2)
@totals.drop_totals(axis=2)
def _table_wise_multilevel(
    df:             pd.DataFrame,
    axlevels:       Any,
    totals_name:    str,
    subtotals_name: str,
    ndigits:        int,
    unit:           int,
    **kwargs
) -> pd.DataFrame:
    axlevels = [min(level) for level in axlevels]

    row_totals = totals_name if axlevels[0] == 0 else subtotals_name
    col_totals = totals_name if axlevels[1] == 0 else subtotals_name

    totals = (
        df.xs(row_totals, level=axlevels[0], drop_level=False)
        .xs(col_totals, axis=1, level=axlevels[1], drop_level=False)
        .reindex_like(df).bfill().bfill(axis=1)
    )

    result = df.div(totals).multiply(unit)
    return result.pipe(round_percentages, ndigits=ndigits)
