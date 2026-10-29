"""Run-scoped authored analysis, exact citation validation and claim boundaries.

The application exposes context as a read action. The two writes are dispatched
through Lab._dispatch so object creation and its command receipt share one
transaction.
"""
from __future__ import annotations

from copy import deepcopy

from .core import encoded, require


FORMAT = 'relata-authored-analysis-1'
OBSERVATION_FIELDS = {'input', 'governing_history', 'text', 'actions'}
RELATIONS = {'supports', 'challenges', 'context'}
MAX_TITLE_BYTES = 1_024
MAX_TEXT_BYTES = 65_536
MAX_QUOTE_BYTES = 16_384


def observation_text(content):
    """Return only literal/canonical text regions available for exact quoting."""
    result = {}
    for field in ('input', 'governing_history', 'text'):
        value = content.get(field)
        if isinstance(value, str):
            result[field] = value
    if 'actions' in content:
        result['actions'] = encoded(content['actions'])
    return result


def _run(lab, run_id):
    run = lab.get_object(run_id)
    require(run['kind'] == 'run', 'analysis.run_id must reference a run.')
    return run


def _scoped_context(lab, run):
    observations = [o for o in lab._rows('observation') if o['run_id'] == run['id']]
    observation_ids = {o['id'] for o in observations}
    all_reviews = lab._rows('review')
    reviews = [r for r in all_reviews if r['observation_id'] in observation_ids]
    review_ids = {r['id'] for r in reviews}
    rounds = []
    for candidate in lab.list_objects('round'):
        scoped_ids = [oid for oid in candidate['body']['observation_ids'] if oid in observation_ids]
        if scoped_ids:
            item = deepcopy(candidate)
            item['body']['observation_ids'] = scoped_ids
            rounds.append(item)
    dispositions = []
    for candidate in lab._rows('disposition'):
        scoped_ids = [rid for rid in candidate['review_ids'] if rid in review_ids]
        if scoped_ids:
            item = deepcopy(candidate)
            item['review_ids'] = scoped_ids
            dispositions.append(item)
    return observations, rounds, reviews, dispositions


def review_snapshot(reviews, dispositions):
    """Snapshot scoped reviewer heads and dispositions, never analysis prose."""
    superseded = {review['supersedes'] for review in reviews if review.get('supersedes')}
    heads = [review for review in reviews if review['id'] not in superseded]
    heads.sort(key=lambda review: (
        review['round_id'], review['observation_id'], review['reviewer'], review['id']))
    return {
        'review_heads': [{
            'round_id': review['round_id'],
            'observation_id': review['observation_id'],
            'reviewer': review['reviewer'],
            'review_id': review['id'],
        } for review in heads],
        'disposition_ids': sorted(disposition['id'] for disposition in dispositions),
    }


def review_changes(saved, current):
    """Count changed reviewer-head slots and changed disposition entries.

    A same-reviewer amendment changes one head slot. A new reviewer changes one
    slot. Adding a disposition changes one disposition entry.
    """
    old_heads = {
        (head['round_id'], head['observation_id'], head['reviewer']): head['review_id']
        for head in saved.get('review_heads', [])
    }
    new_heads = {
        (head['round_id'], head['observation_id'], head['reviewer']): head['review_id']
        for head in current.get('review_heads', [])
    }
    count = len(set(old_heads) ^ set(new_heads))
    count += sum(old_heads[key] != new_heads[key] for key in set(old_heads) & set(new_heads))
    count += len(set(saved.get('disposition_ids', [])) ^ set(current.get('disposition_ids', [])))
    return count


def context(lab, run_id):
    """Return one run's observations, review context and current analyses."""
    run = _run(lab, run_id)
    study = lab.get_object(run['body']['study']['id'], run['body']['study']['revision'])
    observations, rounds, reviews, dispositions = _scoped_context(lab, run)
    current_snapshot = review_snapshot(reviews, dispositions)
    analyses = []
    for candidate in lab.list_objects('analysis'):
        if not any(ref['id'] == run['id'] for ref in candidate['refs']):
            continue
        item = deepcopy(candidate)
        if item['body'].get('format') == FORMAT:
            saved = item['body'].get('review_snapshot', {})
            count = review_changes(saved, current_snapshot)
            item['review_changed'] = count > 0
            item['review_change_count'] = count
        analyses.append(item)
    return {
        'run': run,
        'study': study,
        'coverage': lab.coverage(run['id']),
        'observations': observations,
        'observation_text': {
            observation['id']: observation_text(observation['content'])
            for observation in observations
        },
        'rounds': rounds,
        'reviews': reviews,
        'dispositions': dispositions,
        'review_snapshot': current_snapshot,
        'analyses': analyses,
    }


def _text_field(value, label, nonempty=False):
    require(isinstance(value, str), label + ' must be text.')
    if nonempty:
        require(bool(value.strip()), label + ' must be nonempty.')
    return value


def _limits(value):
    require(isinstance(value, list) and all(isinstance(item, str) for item in value),
            'limits must be a list of text items.')
    return list(value)


def _validate_evidence(lab, run, evidence):
    require(isinstance(evidence, list) and evidence,
            'Authored analysis requires at least one evidence item.')
    selected, rounds = set(), {}
    result = []
    for item in evidence:
        require(isinstance(item, dict), 'Each evidence item must be an object.')
        require({'kind', 'id', 'relation', 'note'} <= set(item)
                <= {'kind', 'id', 'relation', 'note', 'quote'},
                'Evidence items need kind, id, relation and note, with optional quote.')
        kind, ident = item['kind'], item['id']
        require(kind in {'observation', 'review'} and isinstance(ident, str) and ident,
                'Evidence kind must be observation or review with a record ID.')
        require(item['relation'] in RELATIONS,
                'Evidence relation must be supports, challenges or context.')
        _text_field(item['note'], 'Evidence note')
        key = (kind, ident)
        require(key not in selected, 'Evidence selections must not contain duplicates.')
        selected.add(key)
        quote = item.get('quote')
        if kind == 'observation':
            record = lab._get_record(ident, 'observation')
            require(record['run_id'] == run['id'], 'Observation evidence belongs to another run.')
            literals = observation_text(record['content'])
            allowed_fields = OBSERVATION_FIELDS
        else:
            record = lab._get_record(ident, 'review')
            observation = lab._get_record(record['observation_id'], 'observation')
            require(observation['run_id'] == run['id'], 'Review evidence belongs to another run.')
            round_object = lab.get_object(record['round_id'])
            require(round_object['kind'] == 'round', 'Review evidence round is missing.')
            rounds[round_object['id']] = round_object
            literals = {'rationale': record['judgment']['rationale']}
            allowed_fields = {'rationale'}
        if quote is not None:
            require(isinstance(quote, dict) and set(quote) == {'field', 'text'},
                    'Evidence quote needs field and text.')
            require(quote['field'] in allowed_fields,
                    'Evidence quote field is not allowed for this record.')
            require(isinstance(quote['text'], str) and bool(quote['text']),
                    'Evidence quote text must be nonempty literal text.')
            require(len(quote['text'].encode('utf-8')) <= MAX_QUOTE_BYTES,
                    'Evidence quote exceeds the 16,384-byte citation limit.')
            require(quote['field'] in literals and quote['text'] in literals[quote['field']],
                    'Evidence quote is not an exact substring of the selected literal field.')
        result.append(deepcopy(item))
    return result, list(rounds.values())


def _save_payload(lab, payload):
    run = _run(lab, payload['run_id'])
    title = _text_field(payload['title'], 'Analysis title', nonempty=True)
    require(len(title.encode('utf-8')) <= MAX_TITLE_BYTES,
            'Analysis title exceeds the 1,024-byte limit.')
    text = _text_field(payload['text'], 'Analysis text', nonempty=True)
    require(len(text.encode('utf-8')) <= MAX_TEXT_BYTES,
            'Analysis text exceeds the 65,536-byte limit.')
    alternatives = _text_field(payload['alternatives'], 'Analysis alternatives')
    require(len(alternatives.encode('utf-8')) <= MAX_TEXT_BYTES,
            'Analysis alternatives exceed the 65,536-byte limit.')
    limits = _limits(payload['limits'])
    evidence_items, rounds = _validate_evidence(lab, run, payload['evidence'])
    _, _, reviews, dispositions = _scoped_context(lab, run)
    body = {
        'format': FORMAT,
        'run_id': run['id'],
        'text': text,
        'alternatives': alternatives,
        'limits': limits,
        'evidence_items': evidence_items,
        'evidence': 'authored interpretation',
        'acceptance': 'unreviewed',
        'review_snapshot': review_snapshot(reviews, dispositions),
    }
    refs = [{'id': run['id'], 'revision': run['revision'], 'relation': 'run'}]
    refs.extend({'id': round_object['id'], 'revision': round_object['revision'],
                 'relation': 'review-context'} for round_object in rounds)
    ident = payload.get('id')
    expected = payload.get('expected_revision')
    if ident is not None:
        require(isinstance(ident, str) and ident, 'Analysis id must be nonempty text.')
        existing = lab.get_object(ident)
        require(existing['kind'] == 'analysis' and existing['body'].get('format') == FORMAT,
                'Only authored analyses may use analysis.save revision.')
        require(existing['body'].get('run_id') == run['id'],
                'An authored analysis cannot move to another run.')
        require(type(expected) is int and expected > 0,
                'Analysis revision requires expected_revision.')
        return lab._object({
            'id': ident,
            'expected_revision': expected,
            'title': title,
            'body': body,
            'refs': refs,
            'visibility': 'private',
        }, True)
    require(expected is None, 'expected_revision requires an existing analysis id.')
    object_payload = {
        'kind': 'analysis',
        'title': title,
        'body': body,
        'refs': refs,
        'visibility': 'private',
    }
    return lab._object(object_payload, False)


def save(lab, payload):
    """Create or revise immutable authored analysis within Lab's transaction."""
    return _save_payload(lab, payload)


def claim(lab, payload):
    """Create a separately authored claim bound to one exact private analysis."""
    analysis_ref = payload['analysis']
    require(isinstance(analysis_ref, dict) and set(analysis_ref) == {'id', 'revision'},
            'Claim.analysis needs exact id and revision.')
    analysis_object = lab.get_object(analysis_ref['id'], analysis_ref['revision'])
    require(analysis_object['kind'] == 'analysis'
            and analysis_object['body'].get('format') == FORMAT,
            'Claim must derive from an exact authored-analysis revision.')
    require(analysis_object['visibility'] == 'private',
            'Authored-analysis claims require a private analysis.')
    title = _text_field(payload['title'], 'Claim title', nonempty=True)
    require(len(title.encode('utf-8')) <= MAX_TITLE_BYTES,
            'Claim title exceeds the 1,024-byte limit.')
    text = _text_field(payload['text'], 'Claim text', nonempty=True)
    require(len(text.encode('utf-8')) <= MAX_TEXT_BYTES,
            'Claim text exceeds the 65,536-byte limit.')
    limits = _limits(payload['limits'])
    visibility = payload.get('visibility', 'private')
    require(visibility in {'private', 'public'},
            'Claim visibility must be private or public.')
    return lab._object({
        'kind': 'claim',
        'title': title,
        'body': {
            'text': text,
            'limits': limits,
            'evidence': 'authored inference',
            'acceptance': 'unreviewed',
        },
        'refs': [{
            'id': analysis_object['id'],
            'revision': analysis_object['revision'],
            'relation': 'derived-from',
        }],
        'visibility': visibility,
    }, False)
