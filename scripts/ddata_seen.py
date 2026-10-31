#!/usr/bin/env python3
import csv, re, sys, os, collections

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log = sys.argv[1] if len(sys.argv) > 1 else os.path.join(root, 'logs', 'killtrack.csv')
ddata = os.path.join(root, 'common', 'areas', 'dungeon_data.tin')
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(root, 'logs', 'ddata_seen.txt')


def num(text):
    m = re.fullmatch(r'([\d.,]+)\s*([kKmMbB]?)', text.strip())
    if not m:
        return None
    mult = {'': 1, 'k': 10**3, 'm': 10**6, 'b': 10**9}[m.group(2).lower()]
    return int(float(m.group(1).replace(',', '')) * mult)


def fmt(n):
    for div, suffix in ((10**9, 'B'), (10**6, 'M'), (10**3, 'k')):
        if n >= div:
            return ('%g' % (n / div)) + suffix
    return str(n)


areas, steps = {}, collections.defaultdict(list)
for line in open(ddata, encoding='utf-8', errors='replace'):
    m = re.match(r'\.dd_area \{([^}]*)\} \{([^}]*)\}', line)
    if m:
        areas[m.group(2).lower()] = m.group(1)
        areas[m.group(1).lower()] = m.group(1)
    m = re.match(r'\.dd_step \{([^}]*)\} \{[^}]*\} \{(\d+)\} \{(\d+)\} \{[^}]*\} \{(\d+)\} \{(\d+)\}', line)
    if m:
        steps[m.group(1)].append((int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5))))

seen = {}
if os.path.exists(log):
    for row in csv.reader(open(log, encoding='utf-8', errors='replace')):
        if len(row) < 9:
            continue
        area, scaler, cls = row[2], row[3], num(row[6])
        if cls is None or not scaler.isdigit():
            continue
        key = (area, int(scaler))
        lo, hi, count = seen.get(key, (cls, cls, 0))
        seen[key] = (min(lo, cls), max(hi, cls), count + 1)

lines = []
for (area, scaler), (lo, hi, count) in sorted(seen.items()):
    key = areas.get(area.lower())
    if key is None:
        lines.append('UNKNOWN AREA  %-28s scaler %-4d seen %s - %s (%d kills)' % (area, scaler, fmt(lo), fmt(hi), count))
        continue
    row = next((s for s in steps[key] if s[0] <= scaler <= s[1]), None)
    if row is None:
        tier = max(1, min(7, len(str(hi)) - 3))
        lines.append('NEW           %-28s scaler %-4d seen %s - %s (%d kills)' % (area, scaler, fmt(lo), fmt(hi), count))
        lines.append('              .dd_step {%s} {%d} {%d} {%d} {%s - %s} {%d} {%d} {%d};' % (key, scaler, scaler, scaler, fmt(lo).lower(), fmt(hi).lower(), lo, hi, tier))
    elif row[2] and (lo < row[2] or hi > row[3]):
        lines.append('OUTSIDE       %-28s scaler %-4d seen %s - %s, ddata %s - %s (%d kills)' % (area, scaler, fmt(lo), fmt(hi), fmt(row[2]), fmt(row[3]), count))

text = '\n'.join(lines) if lines else 'nothing new: every logged kill fits an existing ddata row'
open(out, 'w').write(text + '\n')
print(text)
