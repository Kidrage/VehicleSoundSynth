#!/usr/bin/env python3
"""Export explicit control contracts and visible live UI status, without reading presets.

Reports are local QA artifacts. Unmeasured controls remain native_unverified;
wire reachability and Gen source tests never imply full-runtime audibility.
"""
import argparse
import csv
import json
from pathlib import Path
try:
    from . import build_project as b
except ImportError:
    import build_project as b


def contracts():
    registry = b.design_registry()
    result = {}
    for group in registry['contracts']:
        for name in group['selectors'].split():
            if name in result:
                raise ValueError('Duplicate control contract: '+name)
            result[name] = dict(registry['contract_defaults'], **group)
            result[name].pop('selectors')
            result[name]['bounds'] = registry['normalized'].get(name, [])
    required = set(registry['direct']) | set(registry['normalized'])
    required.update(name for modes in registry['modes'].values() for name in modes)
    if required - result.keys():
        raise ValueError('Undocumented selectors: '+str(required-result.keys()))
    return result


def visible_controls(root):
    """Follow actual patcher instances, including embedded BEAP; no old-version scan."""
    known = contracts()
    rows = []
    ui = {'flonum','number','slider','dial','toggle','button','message','umenu',
          'live.dial','live.slider','live.toggle','live.numbox','live.text','live.menu',
          'gain~','live.gain~','filtergraph~','function','tab'}
    def namespace_for(path,profile):
        name=path.name
        if name=='ferrari_dna_v4_designer~.maxpat': return 'ferrari_sound_dna_v4.json'
        if name=='ioniq6n_sound_dna_v4~.maxpat': return 'ioniq6n_sound_dna_v4.json'
        if name=='ioniq6n_sound_dna_v3~.maxpat': return 'ioniq6n_sound_dna_v3.json'
        if profile=='ioniq6n' and ('_bed_v3_beap~' in name or name=='ioniq6n_cinematic_soundscape_host_v3~.maxpat'): return 'ioniq6n_soundscape_modes_v3.json'
        if '_dna_v3_designer' in name: return profile+'_sound_dna_v3.json'
        if name.startswith('vehicle_noise_'): return profile+('_noise_v2.json' if '_v2~' in name else '_noise_v1.json')
        if 'soundscape' in name and profile=='ferrari': return 'ferrari_soundscape_v7.json'
        if 'soundscape' in name and profile=='ioniq6n': return 'ioniq6n_soundscape_modes_v2.json'
        if 'soundscape' in name: return profile+'_soundscape_v5.json'
        if '_sound_dna~' in name: return profile+'_sound_dna.json'
        if '_pop_v' in name: return profile+('_pop_v3.json' if profile=='ferrari' else '_pop_v4.json')
        if '_engine_start_' in name: return profile+'_start_v3.json'
        if name=='vehicle_bus_eq~.maxpat': return profile+'_vehicle_bus_eq.json'
        if name=='module_mixer.maxpat': return ('ferrari_realism_v2' if profile=='ferrari' else profile)+'_module_mixer_noise_v1.json'
        return 'not independently persisted; see owning host contract'
    for profile in b.PROFILE_ORDER:
        seen = set()
        def visit(path, embedded=None, scope=''):
            document = embedded if embedded is not None else json.loads(path.read_text())['patcher']
            if embedded is None:
                if path in seen: return
                seen.add(path)
            boxes = {x['box']['id']:x['box'] for x in document.get('boxes', [])}
            edges = [x['patchline'] for x in document.get('lines', [])]
            for identity, box in boxes.items():
                namespace = scope+'/'+str(box.get('varname',identity))
                if box.get('maxclass') in ui and box.get('presentation'):
                    # Short message-path discovery is a navigation aid, not a
                    # claim that the signal survives the entire audio graph.
                    frontier, visited, selectors, mapping = [identity], set(), set(), []
                    for _ in range(4):
                        next_nodes=[]
                        for node in frontier:
                            if node in visited: continue
                            visited.add(node)
                            text=boxes.get(node,{}).get('text','')
                            if text and node!=identity: mapping.append(text)
                            words=text.replace(',', ' ').split()
                            if words and words[0]=='prepend': words=words[1:]
                            if words and words[0] in known: selectors.add(words[0])
                            next_nodes.extend(e['destination'][0] for e in edges if e['source'][0]==node)
                        frontier=next_nodes
                    selector=' '.join(sorted(selectors))
                    contract=known.get(selector,{})
                    parameter=box.get('saved_attribute_attributes',{}).get('valueof',{})
                    minimum=box.get('minimum',parameter.get('parameter_mmin',0 if parameter else 'Max object default / not explicit'))
                    maximum=box.get('maximum',parameter.get('parameter_mmax','Max object default / not explicit'))
                    if 'parameter_enum' in parameter:
                        minimum,maximum=0,len(parameter['parameter_enum'])-1
                    map_text=' → '.join(mapping)
                    if parameter:
                        map_text=('BEAP '+str(box.get('varname',identity))+'; unitstyle='+str(parameter.get('parameter_unitstyle',0))
                            +'; UI exponent='+str(parameter.get('parameter_exponent',1))+'; local path: '+map_text)
                    rows.append(dict(profile=profile,file=path.relative_to(root).as_posix(),
                        object=namespace,selector=selector or box.get('varname','local UI'),
                        owner=contract.get('owner','local patcher / embedded BEAP'),
                        UI_min=minimum,UI_max=maximum,
                        clamp_bounds=json.dumps(contract.get('bounds',[])),
                        DSP_mapping=box.get('hint') or box.get('annotation') or contract.get('payload',map_text or 'UI action; no scalar DSP mapping'),
                        effective_context=contract.get('context','see candidate parameter guide; native context unmeasured'),
                        save_namespace=(namespace_for(path,profile) if path.name in ('ferrari_dna_v4_designer~.maxpat','ioniq6n_sound_dna_v3~.maxpat','ioniq6n_sound_dna_v4~.maxpat')
                                        else contract.get('save',namespace_for(path,profile))),
                        native_audio_result='not measured for this exact UI control',
                        metric_before='',metric_after='',status='native_unverified',
                        evidence_file='tests/test_runtime_design_routing.py; tests/test_dna_v3.py (structural only)'))
                if 'patcher' in box:
                    visit(path,box['patcher'],namespace)
                    continue
                reference=box.get('name','') if box.get('maxclass')=='bpatcher' else box.get('text','').split(' ',1)[0]
                reference=reference.replace('Patcher:/','')
                basename=Path(reference).name
                if not basename.endswith('.maxpat'): basename += '.maxpat'
                candidate=root/'patchers'/basename
                if candidate.is_file(): visit(candidate)
        visit(root/'main.maxpat')
        visit(root/b.PROFILE_CONFIG[profile]['runtime'])
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    output=args.output.resolve()
    if output==root or root in output.parents:
        parser.error('Reports must stay outside the project')
    output.mkdir(parents=True,exist_ok=True)
    contract_rows=[dict(selector=name,**value) for name,value in contracts().items()]
    rows=visible_controls(root)
    for name,data in (('contracts.csv',contract_rows),('visible_controls.csv',rows)):
        with (output/name).open('w',newline='') as handle:
            writer=csv.DictWriter(handle,fieldnames=list(data[0]))
            writer.writeheader(); writer.writerows(data)
    print(json.dumps({'contracts':len(contract_rows),'visible_controls':len(rows),
                      'status':'native_unverified unless separately evidenced','output':str(output)}))


if __name__=='__main__':
    main()
