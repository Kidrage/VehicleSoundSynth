/* V7 separates independent noise; accepted V6 body/FX settings migrate intact. */
autowatch=1;
outlets=2;
var initialized=false;
function projectRoot() {
    var path=String(this.patcher.filepath || '');
    return path.slice(0,path.lastIndexOf('/')).replace(/\/patchers$/,'');
}
function statePath(){return projectRoot()+'/presets/local/v7_ferrari_soundscape_v7.json';}
function factoryPath(){return projectRoot()+'/presets/v7_factories/ferrari_soundscape_v7_factory.json';}
function exists(path){var f=new File(v7ReadPath(path), 'read');var ok=f.isopen;if(ok)f.close();return ok;}
function prime(){outlet(0, 'read', v7ReadPath(factoryPath()));}
function factory(){prime();}
function reset(){prime();}
function ready(){initialized=true;prime();outlet(1,'soundscape_status','Ferrari Body V7','ferrari');}
function save(){
    if(!initialized)return;
    outlet(0,'store',1);outlet(0,'delete',99);outlet(0,'write',statePath());prime();
    outlet(1,'soundscape_status','Local Body V7 Saved','ferrari');
}
function migrate(previous){
    var data=((((previous||{}).pattrstorage||{}).slots||{})['1']||{}).data||{};
    var out={};
    for(var key in data)if(Object.prototype.hasOwnProperty.call(data,key))out[key.replace(/ferrari_soundscape_v6_beap~/g,'ferrari_soundscape_v7_beap~')]=data[key];
    return out;
}
function restore(){
    if(exists(statePath())){outlet(0, 'read', v7ReadPath(statePath()));return;}
    var old=projectRoot()+'/presets/local/v7_ferrari_soundscape_v6.json';
    if(!exists(old))return;
    var f=new File(v7ReadPath(old), 'read'),text='';
    while(f.isopen&&f.position<f.eof)text+=f.readstring(65536);
    f.close();
    try {
        var values=migrate(JSON.parse(text));outlet(0,'store',1);
        for(var key in values)if(Object.prototype.hasOwnProperty.call(values,key))
            outlet.apply(null,[0,'setstoredvalue',key,1].concat(values[key]));
    }catch(error){post('Ferrari V7 migration skipped: '+error+'\n');}
}
if(typeof module!=='undefined')module.exports={migrate:migrate};

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
