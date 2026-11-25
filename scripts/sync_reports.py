#!/usr/bin/env python3
"""Update the marked paper catalogue blocks and counts from MSCA GitHub Pages."""

import argparse
from collections import Counter
from datetime import datetime, timezone
import html
import json
from pathlib import Path
import re
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
PAGES = 'https://msca-dn-digital-finance.github.io/Publications/'
FEED = PAGES + 'data/research.json'
SECTIONS = ('Publications', 'Preprints', 'Working papers')
TYPES = {
    'journal-article': ('Publications', 'Journal article'),
    'conference-paper': ('Publications', 'Conference paper'),
    'book-chapter': ('Publications', 'Book chapter'),
    'preprint': ('Preprints', 'Preprint'),
    'working-paper': ('Working papers', 'Working paper'),
    'other': ('Publications', 'Other catalogue entry'),
}
STAGES = {
    'idea': 'Research idea',
    'in-progress': 'In progress',
    'draft': 'Draft available',
    'under-review': 'Under review',
    'paused': 'Paused',
    'completed': 'Completed',
}
INDEX_ROW = re.compile(
    r'^(\| \[IRP-(\d+)\]\(IRP-\2/README\.md\) \| [^|\n]+ \| )'
    r'\d+ \| \d+ \| \d+( \|[^\n]+)$', re.M
)
REPORT_DATE = r'(?m)^Paper catalogue snapshot dated [^.]+\.'
INDEX_DATE = r'Paper catalogue snapshot taken on [^.]+\.'
TOTALS = r'The reports cover \d+ publications, \d+ preprints and \d+ working papers from the MSCA catalogue\.'


def download_feed():
    request = Request(FEED, headers={'User-Agent': 'MSCA-DIGITAL-Midterm-Reports/1.0'})
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def validate_feed(feed, report_numbers):
    if not isinstance(feed, dict):
        raise ValueError('Expected a catalogue object')
    records = []
    for collection, kind in [('publications', 'publication'), ('working_papers', 'working-paper')]:
        if not isinstance(feed.get(collection), list):
            raise ValueError(f'Missing catalogue list {collection}')
        ids = set()
        key = 'type' if kind == 'publication' else 'status'
        fields = ('id', 'title', 'authors', 'year', 'irp_numbers', 'link', key)
        for row in feed[collection]:
            if not isinstance(row, dict) or any(not isinstance(row.get(key), str) for key in fields):
                raise ValueError(f'Invalid record in {collection}')
            entry_id = row['id']
            numbers = re.split(r'\s*[;,]\s*', row['irp_numbers'].strip()) if row['irp_numbers'].strip() else []
            if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', entry_id) or entry_id in ids:
                raise ValueError(f'Invalid or duplicate paper ID {entry_id!r}')
            if not row['title'].strip() or not row['authors'].strip():
                raise ValueError(f'Missing title or authors for {entry_id}')
            if row['year'] and not re.fullmatch(r'[0-9]{4}', row['year']):
                raise ValueError(f'Invalid year for {entry_id}')
            if len(set(numbers)) != len(numbers) or not set(numbers).issubset(report_numbers):
                raise ValueError(f'Unexpected IRP assignment for {entry_id}: {numbers}')
            value, allowed = (row['type'], TYPES) if kind == 'publication' else (row['status'], STAGES)
            if value not in allowed:
                raise ValueError(f'Unknown catalogue type or stage {value!r} for {entry_id}')
            for key in ('link', 'preprint_url'):
                url = row.get(key, '')
                if not isinstance(url, str) or (url and not is_web_url(url)):
                    raise ValueError(f'Invalid {key} for {entry_id}')
            for key in ('doi', 'venue'):
                if not isinstance(row.get(key, ''), str):
                    raise ValueError(f'Invalid {key} for {entry_id}')
            ids.add(entry_id)
            records.append((row, kind, numbers))
    if not any(numbers for _, _, numbers in records):
        raise ValueError('The catalogue returned no records assigned to an IRP')
    return records


def is_web_url(url):
    parts = urlsplit(url)
    return parts.scheme in ('https', 'http') and bool(parts.netloc) and not any(char.isspace() for char in url)


def text(value):
    escaped = html.escape(' '.join(value.split()), quote=False)
    return re.sub(r'([\\*_~\[\]|])', r'\\\1', escaped).replace('`', '&#96;')


def link(label, url):
    return f'[{label}]({quote(url, safe=":/%?&=#@+;,!~*-._")})'


def authors(row, kind, note):
    value = row['authors']
    for original, corrected in note.get('author_corrections', {}).items():
        value = value.replace(original, corrected)
    if kind == 'working-paper' and ';' not in value:
        return ' · '.join(text(name.strip()) for name in value.split(','))
    names = []
    for name in value.split(';'):
        name = name.strip()
        if ', ' in name:
            family, given = name.split(', ', 1)
            family = family.title() if family.isupper() else family
            given = given.title() if given.isupper() else given
            name = f'{given} {family}'
        names.append(text(name))
    return ' · '.join(names)


def classify(row, kind, note):
    if kind == 'working-paper':
        return 'Working papers', STAGES[row['status']]
    paper_type = row['type']
    if paper_type == 'other':
        paper_type = note.get('other_type', paper_type)
    if row.get('doi', '').lower() == note.get('accepted_preprint_doi'):
        paper_type = 'preprint'
    return TYPES[paper_type]


def render(row, kind, label, notes, number, current_year):
    title = row['title']
    if title == notes.get('source_title'):
        title = notes.get('irp_titles', {}).get(number, notes.get('title', title))
    venue = row.get('venue', '')
    if row.get('type') == 'other':
        venue = venue or notes.get('other_venue', '')
    year = row['year']
    details = label
    if kind == 'working-paper' and year and int(year) > current_year:
        details = f'{label} · Catalogue year {year}'
        year = ''
    if venue and label in ('Journal article', 'Conference paper', 'Book chapter'):
        details += f' · {text(venue)}'
    citation = authors(row, kind, notes) + (f' ({year})' if year else '')
    body = [f'- **{text(title)}**', f'  {citation}. {details}.']
    summary = notes.get('summary', '')
    if number in notes.get('omit_summary_for', []):
        summary = ''
    if notes.get('accepted_preprint_doi') and row.get('doi', '').lower() != notes['accepted_preprint_doi']:
        summary = ''
    if summary:
        body.append(f'  {summary}')
    links = []
    url = row['link']
    if url:
        if urlsplit(url).hostname in ('zenodo.org', 'www.zenodo.org'):
            source = 'Zenodo'
        else:
            source = 'Linked draft' if kind == 'working-paper' else 'Publisher' if label in ('Journal article', 'Conference paper', 'Book chapter') else 'Record'
        links.append(link(source, url))
    doi = row.get('doi', '')
    if doi.lower().startswith('10.48550/arxiv.'):
        links.append(link('arXiv', 'https://arxiv.org/abs/' + doi.split('.', 2)[2]))
    elif doi and not (url and doi.lower().startswith('10.5281/zenodo.')):
        links.append(link('DOI', 'https://doi.org/' + doi))
    preprint = row.get('preprint_url')
    if preprint and preprint != url:
        links.append(link('Preprint', preprint))
    path = 'working-papers.html' if kind == 'working-paper' else ''
    links.append(link('MSCA catalogue', f'{PAGES}{path}#{kind}/{row["id"]}'))
    body.append('  ' + ' · '.join(links))
    return '\n\n'.join(body)


def marker(section, boundary):
    return f'<!-- {boundary} MSCA {section.upper()} -->'


def replace_block(content, section, replacement):
    start, end = marker(section, 'BEGIN') + '\n', '\n' + marker(section, 'END')
    before, found, rest = content.partition(start)
    _, closed, after = rest.partition(end)
    if not found or not closed or content.count(start) != 1 or content.count(end) != 1:
        raise ValueError(f'Expected one marked {section} block')
    return before + start + '\n' + replacement + '\n' + end + after


def replace_once(pattern, replacement, content):
    updated, count = re.subn(pattern, replacement, content)
    if count != 1:
        raise ValueError(f'Expected one match for {pattern}')
    return updated


def plan_updates(root, feed, today):
    index_path = root / 'README.md'
    index = index_path.read_text(encoding='utf-8')
    numbers = [match[2] for match in INDEX_ROW.finditer(index)]
    report_paths = {number: root / f'IRP-{number}/README.md' for number in numbers}
    if not numbers or len(numbers) != len(report_paths) or set(report_paths.values()) != set(root.glob('IRP-*/README.md')):
        raise ValueError('The index must list each IRP report once')
    notes = json.loads((root / 'data/catalogue-notes.json').read_text(encoding='utf-8'))
    assigned = {number: {section: [] for section in SECTIONS} for number in numbers}
    totals = Counter()
    records = validate_feed(feed, set(numbers))
    records.sort(key=lambda entry: (-int(entry[0]['year'] or 0), entry[0]['title'].casefold(), entry[0]['id']))
    for row, kind, irps in records:
        if not irps:
            continue
        note = notes.get(kind, {}).get(row['id'], {})
        section, label = classify(row, kind, note)
        totals[section] += 1
        for number in irps:
            assigned[number][section].append(render(row, kind, label, note, number, today.year))

    date = f'{today.day} {today:%B %Y}'
    updates = {}
    for number, path in report_paths.items():
        previous = path.read_text(encoding='utf-8')
        updated = previous
        for section in SECTIONS:
            items = assigned[number][section]
            if items:
                block = '\n\n'.join(items)
            elif section == 'Publications' and number == '9' and any(
                '#publication/zenodo-24165580)' in entry for entry in assigned[number]['Preprints']
            ):
                block = 'The catalogue links an accepted manuscript. See the preprint and publication status below.'
            else:
                block = f'No {section.lower()} are listed for this IRP.'
            updated = replace_block(updated, section, block)
        if updated != previous:
            updates[path] = replace_once(REPORT_DATE, f'Paper catalogue snapshot dated {date}.', updated)

    def update_row(match):
        counts = [str(len(assigned[match[2]][section])) for section in SECTIONS]
        return match[1] + ' | '.join(counts) + match[3]

    updated_index = INDEX_ROW.sub(update_row, index)
    count_text = 'The reports cover {} publications, {} preprints and {} working papers from the MSCA catalogue.'
    updated_index = replace_once(TOTALS, count_text.format(*(totals[section] for section in SECTIONS)), updated_index)
    if updates or updated_index != index:
        updated_index = replace_once(INDEX_DATE, f'Paper catalogue snapshot taken on {date}.', updated_index)
        if updated_index != index:
            updates[index_path] = updated_index
    return updates


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--feed', type=Path, help='Use a local copy of the Pages JSON feed')
    args = parser.parse_args()
    feed = json.loads(args.feed.read_text(encoding='utf-8')) if args.feed else download_feed()
    updates = plan_updates(ROOT, feed, datetime.now(timezone.utc).date())
    for path, content in updates.items():
        path.write_text(content, encoding='utf-8')
        print(f'Updated {path.relative_to(ROOT)}')
    if not updates:
        print('The reports already match the Pages catalogue.')


if __name__ == '__main__':
    main()
