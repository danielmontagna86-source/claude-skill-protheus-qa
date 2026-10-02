"""Failure controls for the rc.4 review. Synthetic data and owned processes only."""
import contextlib
import io
import json
import os
import signal
import struct
import subprocess
import sys
import tempfile
import time
import unittest
import zipfile
import zlib
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import tirqa_core as core
import tirqa_evidence as evidence
import tirqa_runner as runner
from tirqa_cli import main as cli
from verify_distribution import verify_archive
from test_tirqa import case, profile, policy, FakeHelper
from test_review_regressions import complete_result
from qa_test_fixtures import png_bytes


def png_chunk(kind, payload):
    return struct.pack('>I', len(payload)) + kind + payload + struct.pack('>I', zlib.crc32(kind + payload) & 0xffffffff)


def make_png(stream=None, *, width=1, height=1, depth=8, color=2, interlace=0, filter_byte=0):
    if stream is None: stream = zlib.compress(bytes([filter_byte, 0, 0, 0]))
    return (b'\x89PNG\r\n\x1a\n' + png_chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, depth, color, 0, 0, interlace))
            + png_chunk(b'IDAT', stream) + png_chunk(b'IEND', b''))


def archive_bytes(extras=None):
    files = {'VERSION': b'0.2.0-rc.4\n', 'SKILL.md': b'# Fixture, never an installed skill\n'}
    files.update(extras or {})
    manifest = {'skill': 'testing-protheus-routines', 'version': '0.2.0-rc.4',
                'files': {name: core.digest(data) for name, data in files.items()}}
    files['PACKAGE_MANIFEST.json'] = core.encoded(manifest)
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w') as archive:
        for name, data in files.items():
            info = zipfile.ZipInfo('testing-protheus-routines/' + name)
            info.create_system = 3; info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    return stream.getvalue()


class JsonAndPolicyReviewTests(unittest.TestCase):
    def test_float_overflow_is_blocked_at_parse(self):
        for value in (b'1e999', b'-1e999'):
            with self.subTest(value=value), self.assertRaises(core.Blocked):
                core.parse_json(b'{"value":' + value + b'}')

    def test_finite_float_still_accepted(self):
        self.assertEqual(core.parse_json(b'{"value":1.25}')['value'], 1.25)

    def test_expiry_types_are_structured_blocks(self):
        manifest = core.bundle_manifest(core.bundle_files(case(), profile()))
        for value in (None, 1, True, [], {}):
            with self.subTest(value=value), self.assertRaises(core.Blocked):
                item = policy(manifest); item['expires_at'] = value
                core.approve(item, case(), profile(), manifest)

    def test_malformed_expiry_is_structured_block(self):
        manifest = core.bundle_manifest(core.bundle_files(case(), profile()))
        item = policy(manifest); item['expires_at'] = 'not-a-date'
        with self.assertRaises(core.Blocked): core.approve(item, case(), profile(), manifest)

    def test_duplicate_identity_markers_are_blocked(self):
        p = profile()
        for check in p['identity_checks']: check['text'] = 'Protheus'
        with self.assertRaises(core.Blocked): core.validate_profile(p)

    def test_cli_bad_policy_cannot_traceback_or_spawn(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); manifest = core.generate(case(), profile(), root / 'bundle')
            approval = policy(manifest); approval['expires_at'] = 123
            core.write_json(root / 'approval.json', approval); (root / 'approval.json').chmod(0o600)
            with patch.object(runner.subprocess, 'Popen') as spawn, contextlib.redirect_stdout(io.StringIO()) as console:
                code = cli('run', ['--bundle', str(root/'bundle'), '--policy', str(root/'approval.json'), '--output', str(root/'run'), '--execute'])
            self.assertEqual(code, 2); self.assertEqual(json.loads(console.getvalue())['status'], 'BLOCKED')
            spawn.assert_not_called(); self.assertFalse((root/'run').exists())


class PngReviewTests(unittest.TestCase):
    def test_valid_rgb_png(self): self.assertTrue(evidence.png_is_structurally_valid(make_png()))
    def test_valid_browser_rgba_png(self): self.assertTrue(evidence.png_is_structurally_valid(png_bytes()))
    def test_crc_valid_but_invalid_deflate(self): self.assertFalse(evidence.png_is_structurally_valid(make_png(b'garbage')))
    def test_truncated_deflate_with_recalculated_crc(self): self.assertFalse(evidence.png_is_structurally_valid(make_png(zlib.compress(b'\0\0\0\0')[:-2])))
    def test_excess_pixel_bytes(self): self.assertFalse(evidence.png_is_structurally_valid(make_png(zlib.compress(b'\0'*100))))
    def test_missing_pixel_bytes(self): self.assertFalse(evidence.png_is_structurally_valid(make_png(zlib.compress(b'\0'))))
    def test_invalid_scanline_filter(self): self.assertFalse(evidence.png_is_structurally_valid(make_png(filter_byte=5)))
    def test_invalid_bitdepth_color_combination(self): self.assertFalse(evidence.png_is_structurally_valid(make_png(depth=1, color=2)))
    def test_trailing_zlib_stream(self): self.assertFalse(evidence.png_is_structurally_valid(make_png(zlib.compress(b'\0'*4) + zlib.compress(b'\0'))))
    def test_palette_required_for_indexed_png(self): self.assertFalse(evidence.png_is_structurally_valid(make_png(zlib.compress(b'\0\0'), color=3)))
    def test_adam7_single_pixel(self): self.assertTrue(evidence.png_is_structurally_valid(make_png(interlace=1)))
    def test_png_memory_limit_before_inflate(self): self.assertFalse(evidence.png_is_structurally_valid(make_png(width=30000,height=30000)))


class ArchiveReviewTests(unittest.TestCase):
    def test_current_release_archive_is_valid(self): self.assertEqual(verify_archive(archive_bytes())['status'], 'VERIFIED')
    def test_windows_case_collision(self):
        with self.assertRaises(core.Blocked): verify_archive(archive_bytes({'skill.md': b'alias'}))
    def test_windows_trailing_period(self):
        with self.assertRaises(core.Blocked): verify_archive(archive_bytes({'SKILL.md.': b'alias'}))
    def test_windows_reserved_devices(self):
        for name in ('NUL.txt', 'COM1.py', 'aux', 'LPT\u00b9.txt'):
            with self.subTest(name=name), self.assertRaises(core.Blocked): verify_archive(archive_bytes({name:b'x'}))
    def test_windows_invalid_characters(self):
        for name in ('data:secret', 'name?.txt', 'file|name', 'bad\x01name'):
            with self.subTest(name=name), self.assertRaises(core.Blocked): verify_archive(archive_bytes({name:b'x'}))
    def test_noncanonical_archive_paths(self):
        for name in ('./notes.md', 'scripts//notes.md', 'scripts/./notes.md'):
            with self.subTest(name=name), self.assertRaises(core.Blocked): verify_archive(archive_bytes({name:b'x'}))
    def test_file_directory_collision(self):
        with self.assertRaises(core.Blocked): verify_archive(archive_bytes({'scripts': b'file','scripts/test.py':b'x'}))
    def test_encrypted_flag_blocked_before_read(self):
        # A marked entry must be rejected rather than prompting for a password.
        data = bytearray(archive_bytes())
        pos = data.index(b'PK\x01\x02'); data[pos+8] |= 1
        with self.assertRaises(core.Blocked): verify_archive(bytes(data))


class EvidenceEnvelopeReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name); (self.root/'screenshots').mkdir()
        (self.root/'screenshots/end.png').write_bytes(png_bytes())
        core.write_json(self.root/'case.json',case());core.write_json(self.root/'profile.json',profile())
        self.result = complete_result()
        self.result.update(exit_code=0, private_cleanup='REMOVED', evidence_status='LOCAL_ONLY')
    def collect(self):
        core.write_json(self.root/'result.json', self.result)
        return runner.collect(self.root,create=True)
    def test_pass_timeout_exit_is_blocked(self):
        self.result['exit_code']=124
        with self.assertRaises(core.Blocked): self.collect()
    def test_pass_boolean_exit_is_blocked(self):
        self.result['exit_code']=False
        with self.assertRaises(core.Blocked): self.collect()
    def test_pass_cleanup_failure_is_blocked(self):
        self.result['private_cleanup']='FAILED_REQUIRES_OPERATOR'
        with self.assertRaises(core.Blocked): self.collect()
    def test_pass_quarantine_is_blocked(self):
        self.result['evidence_status']='QUARANTINED'
        with self.assertRaises(core.Blocked): self.collect()
    def test_missing_finalization_is_blocked(self):
        del self.result['private_cleanup']
        with self.assertRaises(core.Blocked): self.collect()
    def test_failure_cannot_claim_erp_validated(self):
        self.result.update(status='ERROR', erp_validated=True)
        with self.assertRaises(core.Blocked): self.collect()
    def test_valid_finished_simulation(self): self.assertEqual(self.collect()['execution_mode'],'simulated')


class OwnedProcessReviewTests(unittest.TestCase):
    def test_descendant_not_left_running_when_parent_exits(self):
        # Real platform process control. The child heartbeats into a synthetic temp file.
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); ready=root/'child'; beat=root/'heartbeat'
            child=("import signal,time,pathlib,os;" +
                   ("signal.signal(signal.SIGTERM,signal.SIG_IGN);" if os.name!='nt' else '') +
                   "pathlib.Path(%r).write_text(str(os.getpid()));\nwhile True:\n pathlib.Path(%r).write_text(str(time.time()));time.sleep(.03)" % (str(ready),str(beat)))
            parent="import subprocess,sys,time;subprocess.Popen([sys.executable,'-c',%r]);time.sleep(30)" % child
            options = {'creationflags':subprocess.CREATE_NEW_PROCESS_GROUP} if os.name=='nt' else {'start_new_session':True}
            proc=subprocess.Popen([sys.executable,'-c',parent], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **options)
            try:
                end=time.monotonic()+10
                while (not ready.exists() or not beat.exists()) and time.monotonic()<end:time.sleep(.03)
                self.assertTrue(ready.exists() and beat.exists())
                runner.stop_tree(proc); time.sleep(.2)
                first=beat.stat().st_mtime_ns; time.sleep(.15)
                self.assertEqual(first,beat.stat().st_mtime_ns,'owned child still active after stop_tree')
                self.assertIsNotNone(proc.poll())
            finally:
                if os.name=='nt':
                    for pid in ([int(ready.read_text())] if ready.exists() else []) + [proc.pid]:
                        subprocess.run(['taskkill','/PID',str(pid),'/T','/F'],capture_output=True,timeout=10,check=False)
                else:
                    try:os.killpg(proc.pid,signal.SIGKILL)
                    except ProcessLookupError:
                        # The disposable process group was already stopped by the test.
                        pass
                proc.wait(timeout=10)


class FullOfflineFlowTests(unittest.TestCase):
    def test_documented_offline_cli_chain(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);core.write_json(root/'case.json',case());core.write_json(root/'profile.json',profile())
            (root/'sample.prw').write_bytes('// ação\nUser Function ZQA()\nReturn'.encode('cp1252'))
            commands=[('inspect',[str(root/'sample.prw'),'--encoding','cp1252']),
                      ('validate',['--case',str(root/'case.json'),'--profile',str(root/'profile.json')]),
                      ('generate',['--case',str(root/'case.json'),'--profile',str(root/'profile.json'),'--output',str(root/'bundle')])]
            for command,args in commands:
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    self.assertEqual(cli(command,args),0)
                self.assertIsInstance(json.loads(output.getvalue()),dict)
            core.verify_bundle(root/'bundle')
    def test_parent_to_worker_to_collector_simulated(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); manifest=core.generate(case(),profile(),root/'bundle')
            core.write_json(root/'approval.json',policy(manifest));(root/'approval.json').chmod(0o600)
            output=root/'run'
            class SimulatedProcess:
                def wait(self,**kwargs):
                    return runner.run_worker(output/'.private',factory=lambda _:FakeHelper(output/'screenshots'))
                def poll(self):return 0
            with patch.object(runner,'preflight',return_value={'status':'READY_FOR_AUTHORIZATION'}), \
                 patch.dict(os.environ,{'TIR_USER':'qa_operator','TIR_PASSWORD':'offline_secret'}), \
                 patch.object(runner,'private_directory',side_effect=lambda p:p.mkdir(parents=True,mode=0o700)), \
                 patch.object(runner.subprocess,'Popen',return_value=SimulatedProcess()):
                result=runner.execute(root/'bundle',root/'approval.json',output)
            self.assertEqual(result['status'],'PASS'); self.assertFalse(result['erp_validated'])
            self.assertEqual(runner.collect(output)['status'],'PASS')
            self.assertFalse((output/'.private').exists())


class DistributionSnapshotReviewTests(unittest.TestCase):
    def test_extracts_the_verified_bytes_even_if_file_is_replaced(self):
        import test_packaged_skill as packaged
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); path = root / 'package.zip'
            original = archive_bytes(); path.write_bytes(original)
            def verify_then_replace(data):
                result = verify_archive(data)
                path.write_bytes(archive_bytes({'SKILL.md': b'replaced-after-verification'}))
                return result
            def fake_run(args, **kwargs):
                content = (Path(kwargs['cwd']) / 'SKILL.md').read_bytes()
                self.assertNotEqual(content, b'replaced-after-verification')
                return subprocess.CompletedProcess(args, 0)
            with patch.object(sys, 'argv', ['test_packaged_skill.py', '--zip', str(path), '--output', str(root/'result.json')]), \
                 patch.object(packaged, 'verify_archive', side_effect=verify_then_replace), \
                 patch.object(packaged.subprocess, 'run', side_effect=fake_run):
                self.assertEqual(packaged.main(), 0)
