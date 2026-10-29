"""Focused acceptance checks for run-scoped authored analysis."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from relata_lab.application import Application
from relata_lab.core import Lab, LabError


class AnalysisTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.app = Application(self.root / 'workspace')
        self.seq = 0
        self.study, self.run = self.make_run('Primary run')
        self.other_study, self.other_run = self.make_run('Other run')
        self.observation = self.make_observation(self.run, action=True)
        self.other_observation = self.make_observation(self.other_run, action=False)
        self.round = self.make_round(self.observation)
        self.review = self.make_review(self.round, self.observation, 'reviewer-a')

    def tearDown(self):
        self.app.close()
        self.temp.cleanup()

    def command(self, name, payload, command_id=None):
        if command_id is None:
            self.seq += 1
            command_id = 'analysis-test-' + str(self.seq)
        return self.app.command(name, payload, command_id)

    def make_run(self, title):
        study = self.command('object.create', {
            'kind': 'study',
            'title': title + ' study',
            'body': {'text': title, 'analysis_unit': 'planned position'},
        })
        run = self.app.lab.command('run.create', {
            'title': title,
            'study': {'id': study['id'], 'revision': study['revision']},
            'trajectories': [{'id': 'main', 'label': 'Main'}],
            'positions': [{
                'id': 'p1', 'trajectory_id': 'main',
                'condition': 'same input', 'checkpoint': '1',
            }],
        }, 'run-' + title)
        return study, run

    def make_observation(self, run, action=False):
        content = {
            'transport': 'completed',
            'shape': 'action' if action else 'empty',
            'text': '',
            'input': 'literal input ' + run['id'],
            'governing_history': 'literal governing history',
            'transport_detail': 'not citable',
        }
        if action:
            content['actions'] = [{
                'name': 'notify',
                'amount': 1.0,
                'nested': {'z': 2, 'a': 'exact'},
            }]
        return self.app.lab.command('observation.record', {
            'run_id': run['id'],
            'position_ids': ['p1'],
            'content': content,
            'provenance': {'private': 'DO-NOT-PUBLISH'},
        }, 'observation-' + run['id'])

    def make_round(self, *observations):
        return self.app.lab.command('round.create', {
            'title': 'Shared review',
            'protocol': 'governing-history-1',
            'observation_ids': [observation['id'] for observation in observations],
            'contract': {'question': 'Use exact evidence.'},
            'pass': 'first',
            'disclosure': {'scope': 'literal evidence and response'},
        }, 'round-' + '-'.join(observation['id'] for observation in observations))

    def make_review(self, round_object, observation, reviewer, rationale='exact review rationale',
                    supersedes=None):
        return self.app.lab.command('review.submit', {
            'round_id': round_object['id'],
            'observation_id': observation['id'],
            'reviewer': reviewer,
            'supersedes': supersedes,
            'expected_head': supersedes,
            'judgment': {
                'response_act': 'action',
                'mapping': 'ambiguous',
                'rationale': rationale,
            },
        }, 'review-' + reviewer + '-' + str(self.seq) + '-' + str(len(self.app.lab.get_state()['reviews'])))

    def payload(self, evidence=None, **overrides):
        if evidence is None:
            evidence = [{
                'kind': 'observation',
                'id': self.observation['id'],
                'relation': 'supports',
                'note': 'The literal action is relevant.',
                'quote': {'field': 'actions', 'text': '"amount":1.0'},
            }]
        value = {
            'run_id': self.run['id'],
            'title': 'Interpretation',
            'text': 'The action is evidence for a bounded interpretation.',
            'alternatives': 'The action may instead reflect the fixture.',
            'limits': ['No independent semantic acceptance.'],
            'evidence': evidence,
        }
        value.update(overrides)
        return value

    def test_save_revise_history_quotes_and_review_change_signal(self):
        first = self.command('analysis.save', self.payload(), 'save-first')
        self.assertEqual(first['body']['format'], 'relata-authored-analysis-1')
        self.assertEqual(first['body']['run_id'], self.run['id'])
        self.assertEqual(first['body']['evidence'], 'authored interpretation')
        self.assertEqual(first['body']['acceptance'], 'unreviewed')
        self.assertEqual(first['body']['evidence_items'][0]['quote']['text'], '"amount":1.0')
        self.assertEqual(first['refs'], [{
            'id': self.run['id'], 'revision': 1, 'relation': 'run',
        }])
        self.assertEqual(first, self.command('analysis.save', self.payload(), 'save-first'))

        first_body = deepcopy(first['body'])
        amendment = self.make_review(
            self.round, self.observation, 'reviewer-a',
            rationale='amended rationale', supersedes=self.review['id'])
        independent = self.make_review(
            self.round, self.observation, 'reviewer-b', rationale='independent rationale')
        disposition = self.app.lab.command('review.disposition', {
            'round_id': self.round['id'],
            'review_ids': [self.review['id'], amendment['id'], independent['id']],
            'decision': 'retain disagreement',
            'rationale': 'The interpretations remain distinct.',
        }, 'disposition-primary')
        self.assertIsNotNone(disposition)

        context = self.command('analysis.context', {'run_id': self.run['id']}, 'context-after-review')
        head = next(item for item in context['analyses'] if item['id'] == first['id'])
        self.assertTrue(head['review_changed'])
        self.assertEqual(head['review_change_count'], 3)
        self.assertEqual(head['body'], first_body)
        self.assertEqual(self.app.lab.get_object(first['id'], 1)['body'], first_body)
        self.assertIn('"amount":1.0', context['observation_text'][self.observation['id']]['actions'])
        self.assertNotIn('transport_detail', context['observation_text'][self.observation['id']])
        self.assertEqual(first, self.command('analysis.save', self.payload(), 'save-first'))
        revision_payload = self.payload([
            {
                'kind': 'review',
                'id': independent['id'],
                'relation': 'challenges',
                'note': 'Capture the current review context.',
                'quote': {'field': 'rationale', 'text': 'independent rationale'},
            },
        ], id=first['id'], expected_revision=1)
        revision_result = self.command('analysis.save', revision_payload, 'retry-after-review')
        original_snapshot = deepcopy(revision_result['body']['review_snapshot'])
        third = self.make_review(
            self.round, self.observation, 'reviewer-c',
            rationale='later independent rationale')
        self.assertEqual(
            revision_result,
            self.command('analysis.save', revision_payload, 'retry-after-review'))
        self.assertEqual(
            self.app.lab.get_object(first['id'], 2)['body']['review_snapshot'],
            original_snapshot)
        self.assertNotIn(
            third['id'],
            {head['review_id'] for head in original_snapshot['review_heads']})

        revised_payload = self.payload([
            {
                'kind': 'review',
                'id': independent['id'],
                'relation': 'challenges',
                'note': 'A second reviewer challenges the first reading.',
                'quote': {'field': 'rationale', 'text': 'independent rationale'},
            },
            {
                'kind': 'observation',
                'id': self.observation['id'],
                'relation': 'context',
                'note': 'The empty response remains literal evidence.',
            },
        ], title='Revised interpretation', id=first['id'], expected_revision=2)
        revised = self.command('analysis.save', revised_payload, 'save-revision')
        self.assertEqual(revised['revision'], 3)
        self.assertIn({'id': self.round['id'], 'revision': 1, 'relation': 'review-context'},
                      revised['refs'])
        heads_by_reviewer = {
            head['reviewer']: head['review_id']
            for head in revised['body']['review_snapshot']['review_heads']
        }
        self.assertEqual(heads_by_reviewer, {
            'reviewer-a': amendment['id'],
            'reviewer-b': independent['id'],
            'reviewer-c': third['id'],
        })
        self.assertEqual(self.app.lab.get_object(first['id'], 1)['body'], first_body)
        context = self.command('analysis.context', {'run_id': self.run['id']}, 'context-revised')
        current = next(item for item in context['analyses'] if item['id'] == first['id'])
        self.assertFalse(current['review_changed'])
        self.assertEqual(current['review_change_count'], 0)

        with self.assertRaises(LabError) as error:
            self.command('analysis.save', revised_payload, 'stale-revision')
        self.assertEqual(error.exception.code, 'conflict')

    def test_cross_run_duplicates_relations_and_fabricated_quotes_are_rejected(self):
        other_round = self.make_round(self.observation, self.other_observation)
        other_review = self.make_review(other_round, self.other_observation, 'reviewer-other')
        shared_review = self.make_review(
            other_round, self.observation, 'reviewer-shared',
            rationale='in-run judgment from a shared round')
        cases = [
            self.payload([{
                'kind': 'observation', 'id': self.other_observation['id'],
                'relation': 'supports', 'note': 'foreign',
            }]),
            self.payload([{
                'kind': 'review', 'id': other_review['id'],
                'relation': 'context', 'note': 'foreign',
            }]),
            self.payload([
                {'kind': 'observation', 'id': self.observation['id'],
                 'relation': 'supports', 'note': 'first'},
                {'kind': 'observation', 'id': self.observation['id'],
                 'relation': 'context', 'note': 'duplicate'},
            ]),
            self.payload([{
                'kind': 'observation', 'id': self.observation['id'],
                'relation': 'neutral', 'note': 'bad relation',
            }]),
            self.payload([{
                'kind': 'observation', 'id': self.observation['id'],
                'relation': 'supports', 'note': 'fabricated',
                'quote': {'field': 'text', 'text': 'invented response'},
            }]),
            self.payload([{
                'kind': 'observation', 'id': self.observation['id'],
                'relation': 'supports', 'note': 'wrong field',
                'quote': {'field': 'transport_detail', 'text': 'not citable'},
            }]),
            self.payload([{
                'kind': 'review', 'id': self.review['id'],
                'relation': 'context', 'note': 'wrong review field',
                'quote': {'field': 'text', 'text': 'exact review rationale'},
            }]),
            self.payload([{
                'kind': 'observation', 'id': self.observation['id'],
                'relation': 'supports', 'note': 'empty quote',
                'quote': {'field': 'text', 'text': ''},
            }]),
        ]
        for index, payload in enumerate(cases):
            with self.subTest(index=index), self.assertRaises(LabError):
                self.command('analysis.save', payload, 'invalid-' + str(index))
        self.assertEqual([o for o in self.app.lab.list_objects() if o['kind'] == 'analysis'], [])

        context = self.command('analysis.context', {'run_id': self.run['id']}, 'context-scoped')
        self.assertEqual({o['id'] for o in context['observations']}, {self.observation['id']})
        self.assertEqual({review['id'] for review in context['reviews']},
                         {self.review['id'], shared_review['id']})
        self.assertEqual(context['rounds'][0]['body']['observation_ids'], [self.observation['id']])
        self.assertEqual(
            context['review_snapshot']['review_heads'],
            sorted([
                {
                    'round_id': self.round['id'],
                    'observation_id': self.observation['id'],
                    'reviewer': 'reviewer-a',
                    'review_id': self.review['id'],
                },
                {
                    'round_id': other_round['id'],
                    'observation_id': self.observation['id'],
                    'reviewer': 'reviewer-shared',
                    'review_id': shared_review['id'],
                },
            ], key=lambda head: tuple(head[key] for key in (
                'round_id', 'observation_id', 'reviewer', 'review_id'))))

        saved = self.command('analysis.save', self.payload([{
            'kind': 'review',
            'id': shared_review['id'],
            'relation': 'context',
            'note': 'The mixed round has an in-run judgment.',
            'quote': {'field': 'rationale', 'text': 'in-run judgment'},
        }]))
        self.assertIn({
            'id': other_round['id'], 'revision': 1, 'relation': 'review-context',
        }, saved['refs'])

    def test_required_fields_empty_observation_and_exact_review_quotes(self):
        for overrides in (
            {'title': ' '}, {'text': ''}, {'evidence': []},
            {'limits': 'not a list'}, {'run_id': self.other_study['id']},
        ):
            with self.subTest(overrides=overrides), self.assertRaises(LabError):
                self.command('analysis.save', self.payload(**overrides))

        saved = self.command('analysis.save', self.payload([
            {
                'kind': 'observation', 'id': self.observation['id'],
                'relation': 'context', 'note': 'Empty text remains legitimate.',
            },
            {
                'kind': 'review', 'id': self.review['id'],
                'relation': 'context', 'note': 'Quote only the rationale.',
                'quote': {'field': 'rationale', 'text': 'review rationale'},
            },
        ]))
        self.assertEqual(saved['body']['evidence_items'][0].get('quote'), None)
        self.assertEqual(saved['body']['evidence_items'][1]['quote']['text'], 'review rationale')
        self.assertEqual(saved['visibility'], 'private')

    def test_authored_field_size_bounds_are_enforced(self):
        invalid = (
            {'title': 't' * 1_025},
            {'text': 't' * 65_537},
            {'alternatives': '界' * 21_846},
        )
        for overrides in invalid:
            with self.subTest(field=next(iter(overrides))), self.assertRaises(LabError):
                self.command('analysis.save', self.payload(**overrides))

        saved = self.command('analysis.save', self.payload())
        with self.assertRaises(LabError):
            self.command('analysis.claim', {
                'analysis': {'id': saved['id'], 'revision': 1},
                'title': 'Bounded claim',
                'text': 't' * 65_537,
                'limits': [],
            })

    def test_claim_is_separately_authored_and_public_projection_withholds_analysis(self):
        private_text = 'PRIVATE ANALYSIS PROSE MUST NOT LEAK'
        saved = self.command('analysis.save', self.payload(text=private_text))
        claim = self.command('analysis.claim', {
            'analysis': {'id': saved['id'], 'revision': 1},
            'title': 'A separately worded claim',
            'text': 'Only this author-approved public text is disclosed.',
            'limits': ['The dependency remains private.'],
            'visibility': 'public',
        })
        self.assertEqual(claim['kind'], 'claim')
        self.assertEqual(claim['body'], {
            'text': 'Only this author-approved public text is disclosed.',
            'limits': ['The dependency remains private.'],
            'evidence': 'authored inference',
            'acceptance': 'unreviewed',
        })
        self.assertEqual(claim['refs'], [{
            'id': saved['id'], 'revision': 1, 'relation': 'derived-from',
        }])
        preview = self.command('publication.preview', {
            'selected': [{'id': claim['id'], 'revision': 1}],
            'title': 'Public claim',
        })
        rendered = json.dumps(preview, ensure_ascii=False)
        for private in (
            saved['id'], self.observation['id'], self.review['id'],
            self.run['id'], private_text, 'literal input', 'DO-NOT-PUBLISH',
        ):
            self.assertNotIn(private, rendered)
        self.assertTrue(preview['bundle']['objects'][0]['refs'][0]['withheld'])
        self.assertIn('Only this author-approved public text is disclosed.', rendered)

        default_claim = self.command('analysis.claim', {
            'analysis': {'id': saved['id'], 'revision': 1},
            'title': 'Private claim',
            'text': 'Private by default.',
            'limits': [],
        })
        self.assertEqual(default_claim['visibility'], 'private')
        with self.assertRaises(LabError):
            self.command('analysis.claim', {
                'analysis': {'id': self.run['id'], 'revision': 1},
                'title': 'Wrong kind',
                'text': 'Not an analysis.',
                'limits': [],
            })

    def test_backup_and_research_transfer_preserve_analysis_evidence_and_context(self):
        saved = self.command('analysis.save', self.payload([
            {
                'kind': 'review', 'id': self.review['id'],
                'relation': 'challenges', 'note': 'Keep the scoped judgment.',
                'quote': {'field': 'rationale', 'text': 'exact review rationale'},
            },
        ]))
        backup = self.root / 'workspace-backup.zip'
        self.app.lab.backup(backup)
        restored_backup = Lab.restore(backup, self.root / 'backup-restored')
        try:
            context = restored_backup.get_state()
            self.assertIn(saved['id'], {item['id'] for item in context['objects']})
            self.assertEqual(
                restored_backup.get_object(saved['id'])['body']['evidence_items'][0]['id'],
                self.review['id'])
            self.assertIn(self.review['id'], {item['id'] for item in context['reviews']})
        finally:
            restored_backup.close()

        transfer = self.root / 'analysis-transfer.zip'
        self.app.lab.export_bundle(
            transfer, 'research-transfer',
            [{'id': saved['id'], 'revision': saved['revision']}])
        restored_transfer = Lab.restore(transfer, self.root / 'transfer-restored')
        try:
            self.assertEqual(restored_transfer.get_object(saved['id'])['body'], saved['body'])
            self.assertEqual(restored_transfer._get_record(self.observation['id'], 'observation'),
                             self.observation)
            self.assertEqual(restored_transfer._get_record(self.review['id'], 'review'), self.review)
            self.assertEqual(restored_transfer.get_object(self.round['id'])['revision'], 1)
            self.assertEqual(restored_transfer.coverage(self.run['id'])['observation_count'], 1)
        finally:
            restored_transfer.close()

    def test_deterministic_and_authored_analyses_remain_both_readable(self):
        instrument = self.command('instrument.run', {'suite': 'measurement'})
        saved = self.command('analysis.save', self.payload())
        context = self.command('analysis.context', {'run_id': instrument['run']['id']})
        analyses = context['analyses']
        self.assertIn(instrument['analysis']['id'], {item['id'] for item in analyses})
        deterministic = next(item for item in analyses if item['id'] == instrument['analysis']['id'])
        self.assertEqual(deterministic['body'], instrument['analysis']['body'])
        self.assertNotIn('review_changed', deterministic)

        own_context = self.command('analysis.context', {'run_id': self.run['id']})
        authored = next(item for item in own_context['analyses'] if item['id'] == saved['id'])
        self.assertIn('review_changed', authored)


if __name__ == '__main__':
    unittest.main()
