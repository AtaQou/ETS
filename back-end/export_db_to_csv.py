import argparse
import csv
import json
import sqlite3
from datetime import datetime
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export SQLite database records to CSV files."
    )
    parser.add_argument(
        "--db-path",
        default=str(Path(__file__).resolve().parent / "ETSsqLiteDB"),
        help="Path to the SQLite database file.",
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help="Output directory for CSV files. Defaults to back-end/db_exports/<timestamp>.",
    )
    parser.add_argument(
        "--table",
        action="append",
        default=None,
        help="Table name to export. Repeat the flag to export multiple specific tables.",
    )
    parser.add_argument(
        "--single-file",
        action="store_true",
        help="Also export all rows into one CSV file named all_tables.csv.",
    )
    return parser.parse_args()


def build_output_dir(out_dir_arg: str | None) -> Path:
    if out_dir_arg:
        out_dir = Path(out_dir_arg).expanduser().resolve()
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_dir = Path(__file__).resolve().parent / "db_exports" / timestamp
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def get_tables(conn: sqlite3.Connection) -> list[str]:
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
          AND name NOT LIKE 'sqlite_%'
        ORDER BY name
        """
    )
    return [row[0] for row in cursor.fetchall()]


def get_table_columns(conn: sqlite3.Connection, table_name: str) -> list[str]:
    cursor = conn.cursor()
    cursor.execute(f'PRAGMA table_info("{table_name}")')
    return [row[1] for row in cursor.fetchall()]


def export_table_csv(conn: sqlite3.Connection, table_name: str, output_path: Path) -> int:
    columns = get_table_columns(conn, table_name)
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM "{table_name}"')
    rows = cursor.fetchall()

    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        if columns:
            writer.writerow(columns)
        writer.writerows(rows)

    return len(rows)


def export_single_csv(conn: sqlite3.Connection, table_names: list[str], output_path: Path) -> int:
    total_rows = 0
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["table_name", "row_json"])
        writer.writeheader()

        for table_name in table_names:
            columns = get_table_columns(conn, table_name)
            cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM "{table_name}"')
            for row in cursor.fetchall():
                row_dict = dict(zip(columns, row))
                writer.writerow(
                    {
                        "table_name": table_name,
                        "row_json": json.dumps(row_dict, ensure_ascii=False),
                    }
                )
                total_rows += 1
    return total_rows


def main() -> None:
    args = parse_args()
    db_path = Path(args.db_path).expanduser().resolve()
    if not db_path.exists():
        raise FileNotFoundError(f"Database file does not exist: {db_path}")

    out_dir = build_output_dir(args.out_dir)
    conn = sqlite3.connect(str(db_path))
    try:
        existing_tables = get_tables(conn)
        if not existing_tables:
            print("No user tables found in database.")
            return

        if args.table:
            requested = list(dict.fromkeys(args.table))
            missing = sorted(set(requested) - set(existing_tables))
            if missing:
                raise ValueError(f"Tables not found: {', '.join(missing)}")
            tables_to_export = requested
        else:
            tables_to_export = existing_tables

        summary: list[tuple[str, int]] = []
        for table_name in tables_to_export:
            output_path = out_dir / f"{table_name}.csv"
            row_count = export_table_csv(conn, table_name, output_path)
            summary.append((table_name, row_count))

        print(f"Export completed in: {out_dir}")
        for table_name, row_count in summary:
            print(f"{table_name}.csv rows: {row_count}")

        if args.single_file:
            single_path = out_dir / "all_tables.csv"
            total_rows = export_single_csv(conn, tables_to_export, single_path)
            print(f"all_tables.csv rows: {total_rows}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
