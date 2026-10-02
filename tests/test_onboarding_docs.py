"""Onboarding documentation contracts; no network, TIR or ERP execution."""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from package_skill import collect_files
from tirqa_core import CONTRACT

GUIDES = ('INSTALL.md', 'INSTALL_WITH_AI.md', 'USAGE_WITH_AI.md')
CLI = ('inspect_sources.py', 'validate_case.py', 'preflight_tir.py',
       'generate_tir_tests.py', 'run_tir_suite.py', 'collect_evidence.py')


class OnboardingDocsTests(unittest.TestCase):
    def test_readme_has_three_direct_entrypoints(self):
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        for guide in GUIDES:
            self.assertIn(f']({guide})', readme)
            self.assertTrue((ROOT / guide).is_file())

    def test_relative_links_resolve(self):
        for name in (*GUIDES, 'README.md', 'USAGE.md', 'TIR_QUICKSTART.md'):
            text = (ROOT / name).read_text(encoding='utf-8')
            for target in re.findall(r'\]\(([^)]+)\)', text):
                if '://' in target or target.startswith('#'):
                    continue
                target = target.split('#', 1)[0]
                self.assertTrue((ROOT / target).exists(), f'{name}: {target}')

    def test_installation_version_matches_release(self):
        version = (ROOT / 'VERSION').read_text(encoding='utf-8').strip()
        for name in ('INSTALL.md', 'INSTALL_WITH_AI.md', 'README.md'):
            text = (ROOT / name).read_text(encoding='utf-8')
            versions = set(re.findall(r'\b\d+\.\d+\.\d+-rc\.\d+\b', text))
            self.assertEqual(versions, {version}, name)
        self.assertTrue((ROOT / f'RELEASE_NOTES/v{version}.md').exists())

    def test_all_guides_are_in_distributable_inventory(self):
        selected = {p.relative_to(ROOT).as_posix() for p in collect_files(ROOT)}
        self.assertTrue(set(GUIDES).issubset(selected))

    def test_usage_reproduces_canonical_contract_in_order(self):
        text = (ROOT / 'USAGE_WITH_AI.md').read_text(encoding='utf-8')
        headings = re.findall(r'^\d+\. (.+)$', text, flags=re.M)
        self.assertEqual(headings, CONTRACT)

    def test_installation_guards_and_no_nested_clone(self):
        text = (ROOT / 'INSTALL.md').read_text(encoding='utf-8')
        ai = (ROOT / 'INSTALL_WITH_AI.md').read_text(encoding='utf-8')
        self.assertIn('Get-FileHash -LiteralPath $Zip -Algorithm SHA256', text)
        self.assertIn('if (Test-Path -LiteralPath $Destination) { throw', text)
        self.assertIn('Não instalar TIR', ai)
        # The AI recipe explicitly refuses changes to approval and credentials.
        self.assertIn('Não aprovar dependências', ai)
        self.assertIn('Não solicitar/imprimir senhas', ai)
        for document in (text, ai, (ROOT / 'README.md').read_text(encoding='utf-8')):
            self.assertNotRegex(document, r'git clone[^\n]+\.(?:claude|agents)[/\\]skills')

    def test_documented_cli_entrypoints_accept_help(self):
        for entry in CLI:
            process = subprocess.run([sys.executable, str(ROOT / 'scripts' / entry), '--help'],
                                     capture_output=True, text=True, timeout=15)
            self.assertEqual(process.returncode, 0, entry)
            self.assertIn('usage:', process.stdout.lower())

    def test_incomplete_templates_block_without_generating_bundle(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'must-not-exist'
            for script, extra in [('validate_case.py', []),
                                  ('generate_tir_tests.py', ['--output', str(output)])]:
                process = subprocess.run([sys.executable, str(ROOT / 'scripts' / script),
                    '--case', str(ROOT / 'templates/tir/case.example.json'),
                    '--profile', str(ROOT / 'templates/tir/profile.example.json'), *extra],
                    capture_output=True, text=True, timeout=15)
                self.assertEqual(process.returncode, 2)
                self.assertEqual(json.loads(process.stdout)['status'], 'BLOCKED')
                self.assertFalse(output.exists())

    def test_powershell_recipe_blocks(self):
        text = (ROOT / 'INSTALL.md').read_text(encoding='utf-8')
        blocks = re.findall(r'```powershell\n(.*?)```', text, flags=re.S)
        self.assertEqual(len(blocks), 3)
        self.assertIn("$ErrorActionPreference = 'Stop'", blocks[0])
        self.assertIn('$Agent', blocks[1])
        if os.name == 'nt':
            # Parse, do not execute download/copy commands. Mandatory on Windows CI.
            with tempfile.TemporaryDirectory() as directory:
                for index, block in enumerate(blocks):
                    path = Path(directory) / f'recipe-{index}.ps1'
                    path.write_text(block, encoding='utf-8-sig')
                    command = ("$tokens=$null; $errors=$null; "
                        "[System.Management.Automation.Language.Parser]::ParseFile("
                        "'" + str(path).replace("'", "''") + "', [ref]$tokens, [ref]$errors) | Out-Null; "
                        "if ($errors.Count -gt 0) { $errors | Out-String | Write-Output; exit 1 }; exit 0")
                    process = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive',
                        '-Command', command], capture_output=True, text=True, timeout=30)
                    self.assertEqual(process.returncode, 0, process.stdout + process.stderr)

    def test_canonical_skill_bytes_preserved(self):
        data = (ROOT / 'SKILL.md').read_bytes().replace(b'\r\n', b'\n')
        blob = hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()
        self.assertEqual(blob, '138e231d58d603a3b3a7e32351921d1af5545124')


if __name__ == '__main__':
    unittest.main()
