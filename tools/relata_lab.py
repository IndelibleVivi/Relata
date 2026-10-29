#!/usr/bin/env python3
"""Local Studio, fixed offline computation and portable research workspace CLI."""
from pathlib import Path
import argparse
import json
import sys
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from relata_lab.application import Application
from relata_lab.core import Lab, LabError


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path, required=True, help='Private local workspace, outside the Git checkout')
    sub = parser.add_subparsers(dest='action', required=True)
    serve = sub.add_parser('serve')
    serve.add_argument('--port', type=int, default=8765)
    sub.add_parser('state')
    sub.add_parser('catalog')
    legacy = sub.add_parser('register-legacy')
    legacy.add_argument('path', type=Path)
    legacy.add_argument('--format', required=True, choices=['rc005-practice-workspace-1', 'rc005-native-workspace-1', 'future-question-workspace-1'])
    legacy.add_argument('--native-run', type=Path)
    legacy.add_argument('--key')
    read_legacy = sub.add_parser('read-legacy')
    read_legacy.add_argument('id')
    run = sub.add_parser('instrument')
    run.add_argument('suite', choices=['measurement', 'applicability', 'opportunity'])
    command = sub.add_parser('command')
    command.add_argument('name')
    command.add_argument('--input', required=True, type=Path)
    command.add_argument('--key', default=None)
    for name in ('backup', 'restore'):
        sub.add_parser(name).add_argument('archive', type=Path)
    export = sub.add_parser('export')
    export.add_argument('archive', type=Path)
    export.add_argument('--profile', choices=['research-transfer','public-publication'], required=True)
    export.add_argument('--refs', type=Path, required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    if args.workspace.resolve().is_relative_to(repo):
        parser.error('Choose a private workspace outside the source checkout.')
    try:
        if args.action == 'serve':
            from relata_lab.service import serve
            serve(args.workspace, args.port)
            return 0
        if args.action == 'restore':
            restored = Lab.restore(args.archive, args.workspace)
            if isinstance(restored, Lab):
                result = {'restored': True, 'objects': len(restored.list_objects())}
                restored.close()
            else:
                result = restored
        else:
            app = Application(args.workspace)
            try:
                key = getattr(args, 'key', None) or uuid.uuid4().hex
                if args.action == 'state':
                    result = app.state()
                elif args.action == 'catalog':
                    result = app.command('catalog.install', {}, key)
                elif args.action == 'register-legacy':
                    from relata_lab.compat import register_legacy
                    result = register_legacy(app.lab, args.path, args.format, key, native_run=args.native_run)
                elif args.action == 'read-legacy':
                    result = app.command('legacy.read', {'id': args.id}, key)
                elif args.action == 'instrument':
                    result = app.command('instrument.run', {'suite': args.suite}, key)
                elif args.action == 'command':
                    result = app.command(args.name, json.loads(args.input.read_text()), key)
                elif args.action == 'backup':
                    result = app.lab.backup(args.archive)
                else:
                    result = app.lab.export_bundle(args.archive, args.profile, json.loads(args.refs.read_text()))
            finally:
                app.close()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (LabError, ValueError, OSError) as exc:
        print(json.dumps({'error': getattr(exc, 'code', 'invalid'), 'message': str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
