"""Homebrew follows and attests the primary macOS download format."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import update


class UpdateTests(unittest.TestCase):
    def test_primary_installer_is_selected_and_attested(self):
        for suffix in ['zip', 'dmg']:
            with self.subTest(suffix=suffix), tempfile.TemporaryDirectory() as temporary:
                version = '0.2.2'
                stem = f'Monoprint-{version}-aarch64-apple-darwin'
                data = {stem + '.zip': b'app zip', stem + '.dmg': b'app disk image',
                        'appcast-macos-arm64.xml': b'feed', 'provenance.sigstore.json': b'provenance'}
                files = [{'file': name, 'sha256': hashlib.sha256(value).hexdigest(), 'bytes': len(value)}
                         for name, value in data.items() if name != 'provenance.sigstore.json']
                primary = next(f for f in files if f['file'] == stem + '.' + suffix)
                base = update.BASE + '/download/v' + version + '/'
                manifest = {'repository': update.REPOSITORY, 'distribution': True,
                            'version': version, 'tag': 'v' + version, 'commit': 'a' * 40,
                            'files': files, 'downloads': {'macos-arm64': primary | {'url': base + primary['file']}}}
                data['release.json'] = json.dumps(manifest).encode()
                release = {'tag_name': 'v' + version, 'draft': False, 'prerelease': False,
                           'html_url': update.BASE + '/tag/v' + version,
                           'assets': [{'name': name, 'state': 'uploaded', 'browser_download_url': base + name,
                                       'size': len(value), 'digest': 'sha256:' + hashlib.sha256(value).hexdigest()}
                                      for name, value in data.items()]}
                cask = Path(temporary) / 'monoprint.rb'
                cask.write_text('  version "0.2.1"\n  sha256 "old"\n  url "https://example.com/old.zip"\n')
                with patch.object(update, 'CASK', cask), patch.object(update.subprocess, 'check_output', return_value=json.dumps(release)), patch.object(update, 'read', side_effect=lambda url: data[url.removeprefix(base)]), patch.object(update.subprocess, 'run') as run:
                    update.main()
                self.assertIn(hashlib.sha256(data[stem + '.' + suffix]).hexdigest(), cask.read_text())
                self.assertTrue(run.call_args_list[0].args[0][3].endswith('.' + suffix))
                self.assertEqual(run.call_count, 2)
                self.assertIn('aarch64-apple-darwin.' + suffix + '"', cask.read_text())
                self.assertIn('https://github.com/ozanvos/monoprint/releases/download/v#{version}/', cask.read_text())


if __name__ == '__main__':
    unittest.main()
