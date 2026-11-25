from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.sync_reports import SECTIONS, marker, plan_updates


class ReportSyncTests(unittest.TestCase):
    def setUp(self):
        temp = TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        (self.root / 'data').mkdir()
        (self.root / 'data/catalogue-notes.json').write_text('{}\n', encoding='utf-8')
        self.index = self.root / 'README.md'
        self.index.write_text(
            'Paper catalogue snapshot taken on 24 November 2026.\n\n'
            'The reports cover 0 publications, 0 preprints and 0 working papers from the MSCA catalogue.\n\n'
            '| [IRP-1](IRP-1/README.md) | Candidate A | 0 | 0 | 0 | ✅ | ✅ |\n'
            '| [IRP-2](IRP-2/README.md) | Candidate B | 0 | 0 | 0 | ❌ | ❌ |\n',
            encoding='utf-8',
        )
        self.reports = [self.root / f'IRP-{n}/README.md' for n in (1, 2)]
        for path in self.reports:
            path.parent.mkdir()
            content = 'Paper catalogue snapshot dated 24 November 2026.\n\n## Research interests\n\nCandidate-written interest.\n\n'
            for section in SECTIONS:
                content += (
                    f"## {section}\n\n{marker(section, 'BEGIN')}\n\nNo {section.lower()} are listed for this IRP.\n\n"
                    f"{marker(section, 'END')}\n\n"
                )
            content += '## Manuscripts in progress\n\nCandidate-written manuscript.\n'
            path.write_text(content, encoding='utf-8')
        self.today = date(2026, 11, 25)
        self.publication = {
            'id': 'shared-paper', 'title': 'Shared preprint', 'year': '2026',
            'authors': 'Doe, Jane;Smith, Alex', 'irp_numbers': '1;2',
            'link': 'https://zenodo.org/records/1234', 'type': 'preprint',
        }
        self.working = {
            'id': 'shared-paper', 'title': 'Working draft', 'year': '',
            'authors': 'Jane Doe, Alex Smith', 'irp_numbers': '1', 'link': '',
            'status': 'draft',
        }
        self.feed = {'publications': [self.publication], 'working_papers': [self.working]}

    def apply_sync(self):
        for path, content in plan_updates(self.root, self.feed, self.today).items():
            path.write_text(content, encoding='utf-8')

    def test_updates_shared_records_without_touching_manual_material(self):
        self.apply_sync()
        report_1, report_2 = [path.read_text(encoding='utf-8') for path in self.reports]
        for content in (report_1, report_2):
            self.assertIn('snapshot dated 25 November 2026', content)
            self.assertIn('[Zenodo](https://zenodo.org/records/1234)', content)
            self.assertIn('Candidate-written interest.', content)
            self.assertIn('Candidate-written manuscript.', content)
        self.assertIn('Draft available.', report_1)
        self.assertNotIn('Working draft', report_2)
        index = self.index.read_text(encoding='utf-8')
        self.assertIn('0 publications, 1 preprints and 1 working papers', index)
        self.assertIn('Candidate A | 0 | 1 | 1 | ✅ | ✅', index)
        self.assertIn('Candidate B | 0 | 1 | 0 | ❌ | ❌', index)
        self.assertEqual(plan_updates(self.root, self.feed, date(2026, 11, 26)), {})

    def test_removal_reassignment_and_publication_replace_the_previous_listing(self):
        self.apply_sync()
        self.feed['working_papers'] = []
        self.publication.update({
            'type': 'journal-article', 'venue': 'A journal', 'title': 'Published paper',
            'irp_numbers': '2', 'preprint_url': 'https://arxiv.org/abs/1234.56789',
        })
        self.apply_sync()
        report_1, report_2 = [path.read_text(encoding='utf-8') for path in self.reports]
        self.assertNotIn('shared-paper', report_1)
        self.assertNotIn('Shared preprint', report_2)
        self.assertIn('Published paper', report_2.split('## Preprints')[0])
        self.assertIn('[Preprint](https://arxiv.org/abs/1234.56789)', report_2)

    def test_missing_feed_collection_or_markers_fails_without_writing(self):
        before = {path: path.read_bytes() for path in (self.index, *self.reports)}
        with self.assertRaisesRegex(ValueError, 'Missing catalogue list'):
            plan_updates(self.root, {'publications': []}, self.today)
        self.assertEqual(before, {path: path.read_bytes() for path in before})
        self.reports[1].write_text('Manual report', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Expected one marked'):
            self.apply_sync()
        self.assertEqual(self.reports[0].read_bytes(), before[self.reports[0]])
        self.assertEqual(self.index.read_bytes(), before[self.index])
