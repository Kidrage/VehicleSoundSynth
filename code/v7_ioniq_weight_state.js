/* IONIQ weight repair: versioned, explicit saves; previous states read-only. */
autowatch=1;
outlets=2;
var kind=typeof jsarguments!=='undefined'?String(jsarguments[1]):'dna';
var pending=null, initialized=kind==='dna';
function paths(k,patchPath){
    var root=String(patchPath).replace(/\/[^/]*$/,'').replace(/\/patchers$/,'');
    if(k!=='dna' && k!=='soundscape')throw new Error('Unsupported weight state kind');
    var name=k==='dna'?'ioniq6n_sound_dna_v4':'ioniq6n_soundscape_modes_v3';
    var previous=k==='dna'?['ioniq6n_sound_dna_v3','ioniq6n_sound_dna_v2','ioniq6n_sound_dna']:
        ['ioniq6n_soundscape_modes_v2','ioniq6n_soundscape_modes'];
    return {local:root+'/presets/local/v7_'+name+'.json',factory:root+'/presets/v7_factories/'+name+'_factory.json',
        previous:previous.map(function(n){return root+'/presets/local/v7_'+n+'.json';})};
}
function remap(data){
    var result={};
    for(var key in data)if(Object.prototype.hasOwnProperty.call(data,key)){
        var name=key.replace(/ioniq6n_soundscape_(ignition|evolution|lightspeed)(?:_bed_v2)?_beap~/g,
            'ioniq6n_soundscape_$1_bed_v3_beap~');
        result[name]=data[key];
    }
    return result;
}
function merge(factory,saved){
    var data=remap(saved||{}),result={};
    for(var key in factory)if(Object.prototype.hasOwnProperty.call(factory,key)){
        var value=data[key],expected=factory[key];
        var valid=Array.isArray(value) && value.length===expected.length && value.every(function(x,i){
            return typeof expected[i]==='number'?(typeof x==='number' && isFinite(x)):
                (key==='n_sound_mode_state' && ['ignition','evolution','lightspeed'].indexOf(x)>=0);
        });
        result[key]=(valid?value:expected).slice();
        if(key.indexOf('dna_')===0 || /::bed_(weight_balance|foundation)$/.test(key)){
            result[key][0]=Math.max(0,Math.min(1,result[key][0]));
        }
    }
    return result;
}
function readData(path,slot){
    var f=new File(v7ReadPath(path), 'read'),text='';
    if(!f.isopen)return null;
    while(f.position<f.eof)text+=f.readstring(65536);
    f.close();
    try{
        var data=JSON.parse(text).pattrstorage.slots[String(slot)].data;
        return data && typeof data==='object' && !Array.isArray(data)?data:null;
    }catch(e){post('IONIQ weight: invalid state '+path+'\n');return null;}
}
function cancel(){if(pending){pending.cancel();pending=null;}}
function save(){
    if(!initialized)return;
    cancel();
    outlet(0,'store',1);outlet(0,'delete',99);
    outlet(0,'write',paths(kind,this.patcher.filepath).local);
    if(kind==='soundscape')outlet(1,'soundscape_status','Weight Bed V3 Saved','ioniq6n');
}
function readState(resetFactory){
    cancel();
    var all=paths(kind,this.patcher.filepath),factory=readData(all.factory,99);
    if(!factory){post('IONIQ weight: missing factory; keeping current state\n');return;}
    var saved=resetFactory?null:readData(all.local,1);
    if(!saved && !resetFactory){
        for(var i=0;i<all.previous.length && !saved;i++)saved=readData(all.previous[i],1);
    }
    var data=merge(factory,saved);
    outlet(0, 'read', v7ReadPath(all.factory));
    pending=new Task(function(){
        pending=null;
        for(var key in data)if(Object.prototype.hasOwnProperty.call(data,key)){
            outlet.apply(null,[0,'setstoredvalue',key,1].concat(data[key]));
        }
        outlet(0,1);
        if(resetFactory)save.call(this);
    },this);
    pending.schedule(80);
}
function restore(){readState.call(this,false);}
function reset(){readState.call(this,true);}
function ready(){initialized=true;}
function notifydeleted(){cancel();}
if(typeof module!=='undefined' && module.exports)module.exports={paths:paths,remap:remap,merge:merge};

/* Read-only published tone binding fallback. Writes always remain presets/local/v7_*.
 * No V6 local file is imported. Native pattrstorage client paths remain unchanged.
 */
function v7PhysicalExists(path){var f=new File(path,'read'),found=f.isopen;if(found)f.close();return found;}
function v7ReadPath(path){
    path=String(path);
    if(path.indexOf('/presets/local/v7_')>=0 && !v7PhysicalExists(path)){
        var binding=path.replace('/presets/local/v7_','/presets/v7_bindings/');
        if(v7PhysicalExists(binding))return binding;
    }
    return path;
}

// Physical-only JSON read: appended AFTER fallback rewriting by the generator.
// Verification and last-good backup must never resolve to a published binding.
function v7ReadPhysical(path){
    var f=new File(path,'read'),s='';if(!f.isopen)return null;
    if(f.eof>4194304){f.close();return null;}
    while(f.position<f.eof){var part=f.readstring(65536);if(!part.length){f.close();return null;}s+=part;}
    f.close();try{return JSON.parse(s);}catch(e){return null;}
}
