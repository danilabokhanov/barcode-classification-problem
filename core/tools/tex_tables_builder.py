import os
import pandas as pd
from pathlib import Path

_GROUP_COLORS = {
    1: "blue",
    2: "red",
    3: "OliveGreen",
    4: "BurntOrange",
    5: "Violet",
    6: "Teal",
    7: "Magenta",
    8: "Brown",
}

LATEX_TABLES_FOLDER = Path("../latex_tables")

_groups: dict[str, list[str]] = {}


def _register(table_name: str, group: str | None) -> None:
    if group is not None:
        _groups.setdefault(group, []).append(table_name)


def save_group(group: str, output_name: str) -> None:
    table_names = _groups.get(group, [])
    parts = []
    for name in table_names:
        path = LATEX_TABLES_FOLDER / f"{name}.tex"
        if path.exists():
            parts.append(path.read_text(encoding="utf-8"))
    combined = "\n\n".join(parts)
    os.makedirs(LATEX_TABLES_FOLDER, exist_ok=True)
    with (LATEX_TABLES_FOLDER / f"{output_name}.tex").open("w", encoding="utf-8") as f:
        f.write(combined)


def _escape_latex(s) -> str:
    return str(s).replace("_", "\\_").replace("%", "\\%")


def _escape_df_values(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].map(lambda x: _escape_latex(x) if isinstance(x, str) else x)
    return df


def _compress_dataframe(df: pd.DataFrame, decimals: int = 3):
    df = df.copy()
    num = df.round(decimals)
    cols = list(df.columns)
    groups = []
    start = 0
    for j in range(1, len(cols)):
        same = (num.iloc[:, j] == num.iloc[:, j - 1]).all()
        if not same:
            groups.append((start, j - 1))
            start = j
    groups.append((start, len(cols) - 1))
    keep = [g[0] for g in groups]
    df = df.iloc[:, keep]
    num = num.iloc[:, keep]
    df = df.astype(object)
    new_cols = []
    for s, e in groups:
        if s == e:
            new_cols.append(cols[s])
        else:
            new_cols.append(f"{cols[s]}--{cols[e]}")
    df.columns = new_cols
    for i in range(len(df)):
        for j in range(1, len(df.columns)):
            if num.iat[i, j] == num.iat[i, j - 1]:
                df.iat[i, j] = "="

    return df


def dataframe_to_latex_table(
    df: pd.DataFrame,
    table_name: str,
    caption: str | None = None,
    label: str | None = None,
    float_format: str = "%.3f",
    section_after: int | None = None,
    compress: bool = False,
    compress_row: str | None = None,
    group: str | None = None,
):
    df = df.copy()
    decimals = int(float_format.split(".")[1][0])
    if compress:
        df = _compress_dataframe(df, decimals)
    elif compress_row is not None and compress_row in df.index:
        num = df.round(decimals)
        df = df.astype(object)
        row_i = df.index.get_loc(compress_row)
        for j in range(1, len(df.columns)):
            if num.iat[row_i, j] == num.iat[row_i, j - 1]:
                df.iat[row_i, j] = "="
    df = _escape_df_values(df)
    df.index = df.index.map(lambda x: f"\\textit{{{_escape_latex(x)}}}")
    df.columns = [f"\\textit{{{_escape_latex(c)}}}" for c in df.columns]
    index_name = df.index.name or ""
    latex = df.to_latex(
        index=True,
        index_names=False,
        na_rep="-",
        float_format=float_format,
        escape=False,
        column_format="l|" + "c" * len(df.columns),
    )
    lines = latex.splitlines()
    header = " & ".join([f"\\textit{{{_escape_latex(index_name)}}}"] + list(df.columns)) + " \\\\"
    lines[2] = header
    lines = [
        l.replace("\\toprule", "\\hline")
        .replace("\\midrule", "\\hline")
        .replace("\\bottomrule", "\\hline")
        for l in lines
    ]
    if section_after is not None:
        data_start = 4
        insert_at = data_start + section_after
        if insert_at < len(lines):
            lines.insert(insert_at, "\\hline")
    latex = "\n".join(lines)
    if caption or label:
        latex = "\\begin{table}[ht]\n\\centering\n" + latex
        if caption:
            latex += f"\n\\caption{{{caption}}}"
        if label:
            latex += f"\n\\label{{{label}}}"
        latex += "\n\\end{table}"
    os.makedirs(LATEX_TABLES_FOLDER, exist_ok=True)
    with (LATEX_TABLES_FOLDER / f"{table_name}.tex").open("w", encoding="utf-8") as f:
        f.write(latex)
    _register(table_name, group)


def _single_tabular(df: pd.DataFrame, header: str, float_format: str, section_after: int | None) -> str:
    index_name = df.index.name or ""
    n_cols = len(df.columns)
    latex = df.to_latex(
        index=True,
        index_names=False,
        na_rep="-",
        float_format=float_format,
        escape=False,
        column_format="l|" + "c" * n_cols,
    )
    lines = latex.splitlines()
    lines = [
        l.replace("\\toprule", "\\hline")
        .replace("\\midrule", "\\hline")
        .replace("\\bottomrule", "\\hline")
        for l in lines
    ]
    col_header = " & ".join([f"\\textit{{{_escape_latex(index_name)}}}"] + list(df.columns)) + " \\\\"
    lines[2] = col_header
    header_row = f" & \\multicolumn{{{n_cols}}}{{c}}{{\\textit{{{header}}}}} \\\\"
    lines.insert(2, "\\hline")
    lines.insert(2, header_row)
    if section_after is not None:
        data_start = 6
        insert_at = data_start + section_after
        if insert_at < len(lines):
            lines.insert(insert_at, "\\hline")
    return "\n".join(lines)


def paired_dataframes_to_latex_table(
    df_left: pd.DataFrame,
    df_right: pd.DataFrame,
    left_header: str,
    right_header: str,
    table_name: str,
    caption: str | None = None,
    label: str | None = None,
    float_format: str = "%.3f",
    section_after: int | None = None,
    stacked: bool = False,
    group: str | None = None,
):
    df_left = _escape_df_values(df_left.copy())
    df_right = _escape_df_values(df_right.copy())

    df_left.index = df_left.index.map(lambda x: f"\\textit{{{_escape_latex(x)}}}")
    df_right.index = df_right.index.map(lambda x: f"\\textit{{{_escape_latex(x)}}}")
    df_left.columns = [f"\\textit{{{_escape_latex(c)}}}" for c in df_left.columns]
    df_right.columns = [f"\\textit{{{_escape_latex(c)}}}" for c in df_right.columns]

    if stacked:
        tab_left = _single_tabular(df_left, left_header, float_format, section_after)
        tab_right = _single_tabular(df_right, right_header, float_format, section_after)
        latex = tab_left + "\n\n\\vspace{8pt}\n\n" + tab_right
    else:
        n_left = len(df_left.columns)
        n_right = len(df_right.columns)
        index_name = df_left.index.name or ""

        col_format = "l|" + "c" * n_left + "|" + "c" * n_right
        df_combined = pd.concat([df_left, df_right], axis=1)

        latex = df_combined.to_latex(
            index=True,
            index_names=False,
            na_rep="-",
            float_format=float_format,
            escape=False,
            column_format=col_format,
        )
        lines = latex.splitlines()
        lines = [
            l.replace("\\toprule", "\\hline")
            .replace("\\midrule", "\\hline")
            .replace("\\bottomrule", "\\hline")
            for l in lines
        ]
        all_cols = list(df_left.columns) + list(df_right.columns)
        col_header = " & ".join([f"\\textit{{{_escape_latex(index_name)}}}"] + all_cols) + " \\\\"
        lines[2] = col_header
        multicolumn_row = (
            f" & \\multicolumn{{{n_left}}}{{c|}}{{\\textit{{{left_header}}}}}"
            f" & \\multicolumn{{{n_right}}}{{c}}{{\\textit{{{right_header}}}}} \\\\"
        )
        lines.insert(2, "\\hline")
        lines.insert(2, multicolumn_row)
        if section_after is not None:
            data_start = 6
            insert_at = data_start + section_after
            if insert_at < len(lines):
                lines.insert(insert_at, "\\hline")
        latex = "\n".join(lines)

    if caption or label:
        latex = "\\begin{table}[ht]\n\\centering\n" + latex
        if caption:
            latex += f"\n\\caption{{{caption}}}"
        if label:
            latex += f"\n\\label{{{label}}}"
        latex += "\n\\end{table}"
    os.makedirs(LATEX_TABLES_FOLDER, exist_ok=True)
    with (LATEX_TABLES_FOLDER / f"{table_name}.tex").open("w", encoding="utf-8") as f:
        f.write(latex)
    _register(table_name, group)


def _colorize_group_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy().astype(object)
    for i in range(len(df)):
        for j in range(len(df.columns)):
            val = df.iat[i, j]
            if isinstance(val, (int, float)) and not pd.isna(val):
                n = int(val)
                color = _GROUP_COLORS.get(n, "black")
                df.iat[i, j] = f"\\textcolor{{{color}}}{{{n}}}"
    return df


def paired_group_assignment_to_latex_table(
    df_left: pd.DataFrame,
    df_right: pd.DataFrame,
    left_header: str,
    right_header: str,
    table_name: str,
    caption: str | None = None,
    label: str | None = None,
    section_after: int | None = None,
    stacked: bool = False,
    group: str | None = None,
):
    df_left = _colorize_group_df(df_left)
    df_right = _colorize_group_df(df_right)

    df_left.index = df_left.index.map(lambda x: f"\\textit{{{_escape_latex(x)}}}")
    df_right.index = df_right.index.map(lambda x: f"\\textit{{{_escape_latex(x)}}}")
    df_left.columns = [f"\\textit{{{_escape_latex(c)}}}" for c in df_left.columns]
    df_right.columns = [f"\\textit{{{_escape_latex(c)}}}" for c in df_right.columns]

    if stacked:
        tab_left = _single_tabular(df_left, left_header, "%.0f", section_after)
        tab_right = _single_tabular(df_right, right_header, "%.0f", section_after)
        latex = tab_left + "\n\n\\vspace{8pt}\n\n" + tab_right
    else:
        n_left = len(df_left.columns)
        n_right = len(df_right.columns)
        index_name = df_left.index.name or ""

        col_format = "l|" + "c" * n_left + "|" + "c" * n_right
        df_combined = pd.concat([df_left, df_right], axis=1)

        latex = df_combined.to_latex(
            index=True,
            index_names=False,
            na_rep="-",
            float_format="%.0f",
            escape=False,
            column_format=col_format,
        )
        lines = latex.splitlines()
        lines = [
            l.replace("\\toprule", "\\hline")
            .replace("\\midrule", "\\hline")
            .replace("\\bottomrule", "\\hline")
            for l in lines
        ]
        all_cols = list(df_left.columns) + list(df_right.columns)
        col_header = " & ".join([f"\\textit{{{_escape_latex(index_name)}}}"] + all_cols) + " \\\\"
        lines[2] = col_header
        multicolumn_row = (
            f" & \\multicolumn{{{n_left}}}{{c|}}{{\\textit{{{left_header}}}}}"
            f" & \\multicolumn{{{n_right}}}{{c}}{{\\textit{{{right_header}}}}} \\\\"
        )
        lines.insert(2, "\\hline")
        lines.insert(2, multicolumn_row)
        if section_after is not None:
            data_start = 6
            insert_at = data_start + section_after
            if insert_at < len(lines):
                lines.insert(insert_at, "\\hline")
        latex = "\n".join(lines)

    if caption or label:
        latex = "\\begin{table}[ht]\n\\centering\n" + latex
        if caption:
            latex += f"\n\\caption{{{caption}}}"
        if label:
            latex += f"\n\\label{{{label}}}"
        latex += "\n\\end{table}"
    os.makedirs(LATEX_TABLES_FOLDER, exist_ok=True)
    with (LATEX_TABLES_FOLDER / f"{table_name}.tex").open("w", encoding="utf-8") as f:
        f.write(latex)
    _register(table_name, group)
