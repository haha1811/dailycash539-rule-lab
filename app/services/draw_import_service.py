import csv
from datetime import datetime
from io import StringIO

from sqlalchemy.orm import Session

from app.models.draw import Draw

REQUIRED_COLUMNS = ["draw_no", "draw_date", "n1", "n2", "n3", "n4", "n5"]


def _validate_numbers(numbers: list[int]) -> None:
    if len(set(numbers)) != 5:
        raise ValueError("同一期號碼不能重複")
    if not all(1 <= n <= 39 for n in numbers):
        raise ValueError("號碼必須在 1~39")


def import_draws_csv(db: Session, raw_csv: str, source: str = "csv_import") -> dict:
    reader = csv.DictReader(StringIO(raw_csv.strip()))
    if not reader.fieldnames:
        raise ValueError("CSV 欄位缺失")
    if any(col not in reader.fieldnames for col in REQUIRED_COLUMNS):
        raise ValueError(f"CSV 必須包含欄位: {REQUIRED_COLUMNS}")

    inserted, skipped = 0, 0
    for row in reader:
        draw_no = row["draw_no"].strip()
        if db.query(Draw).filter(Draw.draw_no == draw_no).first():
            skipped += 1
            continue

        numbers = [int(row[f"n{i}"]) for i in range(1, 6)]
        _validate_numbers(numbers)
        draw_date = datetime.strptime(row["draw_date"], "%Y-%m-%d").date()

        draw = Draw(
            draw_no=draw_no,
            draw_date=draw_date,
            n1=numbers[0],
            n2=numbers[1],
            n3=numbers[2],
            n4=numbers[3],
            n5=numbers[4],
            numbers_sorted=",".join(map(str, sorted(numbers))),
            source=source,
        )
        db.add(draw)
        inserted += 1

    db.commit()
    return {"inserted": inserted, "skipped": skipped}
