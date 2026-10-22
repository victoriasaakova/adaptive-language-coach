"""Pure calendar-day SRS helpers. No file writes, network calls or reminders."""
from copy import deepcopy
from datetime import date, timedelta

OFFSETS = (1, 3, 7, 14)

def day(value):
    return date.fromisoformat(value)

def next_due(entry):
    origin = day(entry["introduced_on"])
    pending = [n for n in OFFSETS if n not in entry["passed_offsets"]]
    if not pending:
        return None
    due = origin + timedelta(days=pending[0])
    if entry.get("retry_on"):
        due = min(due, day(entry["retry_on"]))
    if entry["reviews"]:
        last = max(day(r["date"]) for r in entry["reviews"])
        due = max(due, last + timedelta(days=1))
    return due.isoformat()

def review(entry, on, correct, assisted=False, novel_use=True):
    """Return a new entry; a pass requires retrieval plus original use."""
    today = day(on)
    origin = day(entry["introduced_on"])
    if today < origin or any(today < day(r["date"]) for r in entry["reviews"]):
        raise ValueError("Review cannot predate introduction or existing reviews")
    out = deepcopy(entry)
    due = next_due(entry)
    success = correct and not assisted and novel_use
    pending = [n for n in OFFSETS if n not in entry["passed_offsets"]]
    if not success:
        if not pending:
            out["introduced_on"] = on
            out["passed_offsets"] = []
        out["retry_on"] = (today + timedelta(days=1)).isoformat()
    elif due and today >= day(due):
        if pending and today >= origin + timedelta(days=pending[0]):
            out["passed_offsets"].append(pending[0])
        out["retry_on"] = None
    out["reviews"].append({"date": on, "result": "pass" if success else "retry",
                           "assisted": assisted, "evidence": "record learner evidence separately"})
    out["status"] = "cycle_complete" if len(out["passed_offsets"]) == 4 else "learning"
    return out
