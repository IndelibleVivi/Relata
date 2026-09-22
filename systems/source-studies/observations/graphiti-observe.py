"""Isolated source-branch observations; does not import Graphiti or use services."""
import argparse
import ast
import asyncio
import json
import re
import subprocess
from pathlib import Path
from types import SimpleNamespace as NS

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source', type=Path, required=True, help='Graphiti checkout at the report commit')
ROOT = parser.parse_args().source.resolve()
expected_commit = '16cdf7045378c8d53ae01f94e2fa60d238cb0f68'
actual_commit = subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip()
dirty = subprocess.check_output(['git', '-C', str(ROOT), 'status', '--porcelain'], text=True)
if actual_commit != expected_commit or dirty:
    parser.error('The observation requires a clean checkout at ' + expected_commit)
ns = {'re': re}
def load_function(path, name, class_name=None):
    tree = ast.parse((ROOT / path).read_text())
    container = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == class_name) if class_name else tree
    function = next(n for n in container.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name)
    module = ast.Module(body=[ast.ImportFrom(module='__future__', names=[ast.alias(name='annotations')], level=0), function], type_ignores=[])
    exec(compile(ast.fix_missing_locations(module), str(ROOT / path), 'exec'), ns)
    return ns[name]

load_function('graphiti_core/utils/maintenance/dedup_helpers.py', '_normalize_string_exact')
resolve = load_function('graphiti_core/utils/maintenance/edge_operations.py', 'resolve_extracted_edge')
remove = load_function('graphiti_core/graphiti.py', 'remove_episode', 'Graphiti')

async def main():
    old = NS(uuid='old', source_node_uuid='a', target_node_uuid='b', fact='Lin works at Cedar', episodes=['e1'], valid_at='2026-01-01', invalid_at='2026-02-01', expired_at='2026-02-02')
    new = NS(uuid='new', source_node_uuid='a', target_node_uuid='b', fact='Lin works at Cedar', episodes=['e3'], valid_at='2026-03-01', invalid_at=None, expired_at=None)
    resolved, duplicates, invalidations = await resolve(None, new, [old], [], NS(uuid='e3'))
    assert resolved is old and resolved.invalid_at == '2026-02-01' and resolved.episodes == ['e1', 'e3']
    output = {'exact_recurrence_branch': {'reused_old_edge': resolved is old, 'valid_at': resolved.valid_at, 'invalid_at': resolved.invalid_at, 'episodes': resolved.episodes, 'llm_calls': 0}}
    for delete_uuid in ['e1', 'e2']:
        deletions = []
        edge = NS(uuid='shared-edge', episodes=['e1', 'e2'])
        entity = NS(uuid='shared-node', summary='Lin works at Cedar')
        async def episode_delete(driver):
            deletions.append(['episode', delete_uuid])
        episode = NS(uuid=delete_uuid, entity_edges=['shared-edge'], delete=episode_delete)
        async def get_episode(driver, uuid): return episode
        async def get_edges(driver, uuids): return [edge]
        async def mentioned(driver, episodes): return [entity]
        async def query(*args, **kwargs): return ([{'episode_count': 2}], None, None)
        async def delete_edges(driver, uuids): deletions.append(['edges', uuids])
        async def delete_nodes(driver, uuids): deletions.append(['nodes', uuids])
        ns.update(EpisodicNode=NS(get_by_uuid=get_episode), EntityEdge=NS(get_by_uuids=get_edges), get_mentioned_nodes=mentioned, Edge=NS(delete_by_uuids=delete_edges), Node=NS(delete_by_uuids=delete_nodes))
        await remove(NS(driver=NS(execute_query=query)), delete_uuid)
        expected = ['shared-edge'] if delete_uuid == 'e1' else []
        assert deletions[0] == ['edges', expected]
        assert edge.episodes == ['e1', 'e2'] and entity.summary == 'Lin works at Cedar'
        output['delete_' + delete_uuid] = {'deletion_calls': deletions, 'unchanged_edge_sources': edge.episodes, 'unchanged_shared_summary': entity.summary}
    print(json.dumps(output, ensure_ascii=False, indent=2))

asyncio.run(main())
