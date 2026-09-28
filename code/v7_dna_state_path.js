/* EV V7 isolated DNA persistence; native pattrstorage client names stay unchanged. */
autowatch=1;outlets=1;
var profile=typeof jsarguments!=='undefined'?String(jsarguments[1]):'ev', pending=null, initialized=false;
function root(){return String(this.patcher.filepath).replace(/\\/g,'/').replace(/\/[^/]*$/,'').replace(/\/patchers$/,'');}
function paths(){var r=root.call(this);return {local:r+'/presets/local/v7_'+profile+'_sound_dna.json',factory:r+'/presets/v7_factories/'+profile+'_sound_dna_factory.json'};}
function exists(p){var f=new File(v7ReadPath(p), 'read');var yes=f.isopen;if(yes)f.close();return yes;}
function save(){if(!initialized)return;outlet(0,'store',1);outlet(0,'delete',99);outlet(0,'write',paths.call(this).local);}
function readState(reset){
 if(pending)pending.cancel();var p=paths.call(this),local=!reset&&exists(p.local),file=local?p.local:p.factory;
 if(!exists(file)){post('V7 EV DNA state missing: '+file+'\n');return;}
 outlet(0, 'read', v7ReadPath(file));pending=new Task(function(){pending=null;outlet(0,local?1:99);initialized=true;},this);pending.schedule(80);
}
function restore(){readState.call(this,false);}function reset(){readState.call(this,true);}
function notifydeleted(){if(pending)pending.cancel();}

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
