"""Small reversible IONIQ order enhancement; no Soundscape or drive ownership."""
SPECS = (('accel_orders', 'Accel Orders', 0., 1.),)
METADATA = {'accel_orders': ('DNA', '加速阶次', '0–1', '正加速 / >1200 RPM',
    '0=原声；0.30=轻增强；1=最大。只增强 1.5× / 2.25× 阶次，不改变主音高。')}


def source_code(legacy):
    code = 'Param accel_orders(0.30, min=0, max=1);\nHistory detail_env(0);\n' + legacy
    seam = 'order1 = '
    position = code.index(seam)
    code = code[:position] + '''// Positive acceleration only. No shift/vehicle-state feedback.
detail_progress = clamp((r-1200)/1800,0,1);
detail_window = detail_progress*detail_progress*(3-2*detail_progress);
detail_target = clamp(accel,0,1)*clamp(throttle,0,1)*clamp(load,0,1)*detail_window;
detail_tau = detail_target > detail_env ? .080 : .180;
detail_k = exp(-1/(samplerate*detail_tau));
detail_env = detail_target+(detail_env-detail_target)*detail_k;
detail_amount = slide(clamp(accel_orders,0,1),samplerate*.025,samplerate*.025)*detail_env;
''' + code[position:]
    for expression, factor in (('(0.13 + 0.12*motor_order)', '.50'),
                               ('(0.055 + 0.09*cavity_structure)', '.80')):
        if code.count(expression) != 1:
            raise ValueError('IONIQ accepted order seam changed: '+expression)
        code = code.replace(expression, expression+'*(1+'+factor+'*detail_amount)')
    return code


def complete_state(document):
    """Keep the accepted BEAP/audio graph; replace only legacy state actions."""
    patch = document['patcher']
    boxes = {x['box']['id']: x['box'] for x in patch['boxes']}
    def by_text(text):
        return next(x for x in boxes.values() if x.get('text') == text)
    state = by_text('js Patcher:/code/dna_v2_state_path.js ioniq6n')
    state['text'] = 'js Patcher:/code/ioniq_dna_v2_state.js'
    storage = next(x for x in boxes.values() if x.get('text','').startswith('pattrstorage '))
    storage['text'] = 'pattrstorage ioniq6n_sound_dna_v2 @savemode 0 @changemode 1 @autorestore 0 @greedy 1'
    reset = by_text('Reset DNA')
    reset['text'] = 'Factory Reset'
    reset['presentation_rect'][2] = 110.
    order = by_text('t b b')
    order['text'] = 't b'
    order['numoutlets'] = 1
    removed = {by_text(text)['id'] for text in ('delay 35', '1', 'closebang')}
    patch['boxes'] = [x for x in patch['boxes'] if x['box']['id'] not in removed]
    lines = []
    for entry in patch['lines']:
        line = entry['patchline']
        if line['source'][0] in removed or line['destination'][0] in removed or line['source'][0] == reset['id']:
            continue
        if line['source'][0] == order['id']:
            line['source'][1] = 0
        lines.append(entry)
    patch['boxes'].append({'box': {'id':'detail-reset', 'maxclass':'message', 'text':'reset',
        'patching_rect':[1180.,250.,50.,22.], 'numinlets':2, 'numoutlets':1}})
    for source, destination in ((reset['id'],'detail-reset'),('detail-reset',state['id'])):
        lines.append({'patchline': {'source':[source,0], 'destination':[destination,0]}})
    patch['lines'] = lines
    return document


def factory(document):
    try:
        from . import build_project as b
    except ImportError:
        import build_project as b
    data = {'dna_'+key:[value] for key,value in b.IONIQ6N_DNA_DEFAULTS.items()}
    data['dna_accel_orders'] = [.30]
    data.update(b.dna_v3.beap_factory_data(document))
    return {'pattrstorage': {'name':'ioniq6n_sound_dna_v2', 'slots': {'99': {'id':99, 'data':data}}}}
