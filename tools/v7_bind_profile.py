#!/usr/bin/env python3
"""Publish a complete, explicitly selected V7 tone snapshot (dry-run by default).
Reads only whitelisted V7 local owner files; never modifies local/V6 presets.
A published binding is read only when that owner's local V7 state is absent.
"""
from __future__ import annotations
import argparse, hashlib, json, math, os, re, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
MAX_BYTES = 4 * 1024 * 1024


def validate_values(value, at='root'):
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f'Non-finite value at {at}')
    if isinstance(value, str) and re.search(r'(?:/Users/|/home/|[A-Za-z]:[\\/]|token=|gh[pousr]_[A-Za-z0-9])', value):
        raise ValueError(f'Local path/credential-like value at {at}; clean the preset first')
    if isinstance(value, dict):
        for key, item in value.items():
            validate_values(item, at+'.'+str(key))
    elif isinstance(value, list):
        for i, item in enumerate(value): validate_values(item, f'{at}[{i}]')


def collect(root: Path, profile: str):
    owners = json.loads((root/'assets/v7/state_owners.json').read_text())
    if profile not in owners: raise ValueError('Unknown engine profile')
    result={}; missing=[]
    for name in owners[profile]:
        src=root/'presets/local'/('v7_'+name)
        if not src.is_file(): missing.append(src.name); continue
        if src.is_symlink(): raise ValueError('Symlink presets are not publishable: '+src.name)
        if src.stat().st_size > MAX_BYTES: raise ValueError('Preset too large: '+src.name)
        doc=json.loads(src.read_text(encoding='utf-8')); validate_values(doc)
        if name == profile+'_profile.json':
            if doc.get('schema_version') != 7 or doc.get('profile') != profile:
                raise ValueError('Profile/schema mismatch: '+name)
            contracts=json.loads((root/'assets/v7/parameter_contracts.json').read_text())['parameters']
            values=doc.get('values',{})
            if set(values) != set(contracts): raise ValueError('Incomplete/unknown V7 parameters: '+name)
            for k,spec in contracts.items():
                v=values[k]
                if type(v) not in (int,float) or not spec['min'] <= v <= spec['max']:
                    raise ValueError('Out-of-range V7 parameter: '+k)
        else:
            data=doc.get('pattrstorage',{}).get('slots',{}).get('1',{}).get('data')
            if not isinstance(data,dict) or not data: raise ValueError('Missing saved slot 1: '+name)
        text=json.dumps(doc,ensure_ascii=False,indent=2,allow_nan=False)+'\n'
        result[name]=text.encode('utf-8')
    if missing:
        raise ValueError('Incomplete engine save; no files changed. Missing: '+', '.join(missing))
    return result


def publish(root: Path, profile: str, write=False):
    files=collect(root,profile)
    hashes={name:hashlib.sha256(data).hexdigest() for name,data in sorted(files.items())}
    manifest={'schema_version':7,'profile':profile,'files':hashes,
              'validation':'Complete saved JSON owner set; native Max reload/listening still required.'}
    if write:
        dest=root/'presets/v7_bindings';dest.mkdir(parents=True,exist_ok=True)
        files[profile+'_binding_manifest.json']=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()
        previous={name:(dest/name).read_bytes() if (dest/name).exists() else None for name in files}
        written=[]
        try:
            # Validate and stage all files before touching any published tone.
            with tempfile.TemporaryDirectory(dir=dest,prefix='.staging-') as tmp:
                for name,data in files.items(): (Path(tmp)/name).write_bytes(data)
                for name in files:
                    os.replace(Path(tmp)/name,dest/name);written.append(name)
        except Exception:
            for name in written:
                if previous[name] is None: (dest/name).unlink(missing_ok=True)
                else: (dest/name).write_bytes(previous[name])
            raise
        for name,h in hashes.items():
            if hashlib.sha256((dest/name).read_bytes()).hexdigest()!=h: raise RuntimeError('Binding readback mismatch: '+name)
    return {**manifest,'write':write,'count':len(hashes)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('profile',choices=['ev','v10','v12','ioniq6n','ferrari'])
    parser.add_argument('--write',action='store_true',help='Explicitly publish; default only validates')
    parser.add_argument('--root',type=Path,default=ROOT)
    args=parser.parse_args()
    try: print(json.dumps(publish(args.root.resolve(),args.profile,args.write),ensure_ascii=False,indent=2))
    except (ValueError,OSError,KeyError,json.JSONDecodeError) as e: raise SystemExit(str(e))
if __name__=='__main__':main()
