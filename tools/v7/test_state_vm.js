/* Synchronous file/Task simulation verifies state logic only, not native Max I/O. */
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const code=fs.readFileSync('code/v7_profile_state.js','utf8');let disk={},last=[];
function Context(profile){
 const f=JSON.parse(fs.readFileSync('presets/v7_factories/'+profile+'_profile.json','utf8'));
 disk['/repo/presets/v7_factories/'+profile+'_profile.json']=JSON.stringify(f);
 function File(path,mode){this.path=path;this.mode=mode;this.position=0;this.isopen=mode==='write'||disk[path]!==undefined;this.eof=(disk[path]||'').length;this.readstring=(n)=>{let s=disk[path].slice(this.position,this.position+n);this.position+=s.length;return s;};this.writestring=(s)=>{disk[path]=s;this.eof=s.length;};this.close=()=>{};}
 let c={File,Task:function(fn,self){this.schedule=()=>fn.call(self);this.cancel=()=>{};},jsarguments:['x',profile],patcher:{filepath:'/repo/patchers/host.maxpat'},outlet:(...a)=>last.push(a),post:()=>{},arrayfromargs:x=>Array.from(x),console};
 vm.createContext(c);vm.runInContext(code,c);c.restore();return c;
}
let profiles=['ev','v10','v12','ioniq6n','ferrari'];
for(let i=0;i<profiles.length;i++){
 let p=profiles[i],c=Context(p);c.messagename='v7_sub_db';c.anything(-25+i);c.messagename='throttle';c.anything(.9);c.save();
 let doc=JSON.parse(disk['/repo/presets/local/v7_'+p+'_profile.json']);assert.equal(doc.values.v7_sub_db,-25+i);assert(!('throttle' in doc.values));
 let restored=Context(p);assert.equal(restored.state.v7_sub_db,-25+i);
 restored.messagename='v7_sub_db';restored.anything(-10);restored.save();disk['/repo/presets/local/v7_'+p+'_profile.json']='corrupt';
 let recovered=Context(p);assert.equal(recovered.state.v7_sub_db,-25+i);recovered.reset();assert.equal(recovered.state.v7_sub_db,JSON.parse(disk['/repo/presets/v7_factories/'+p+'_profile.json']).values.v7_sub_db);
}
// Published binding fallback is read-only; a later local save must not overwrite it.
let bprofile='ev';let local='/repo/presets/local/v7_ev_profile.json';let bound='/repo/presets/v7_bindings/ev_profile.json';
let saved=JSON.parse(disk[local+'.bak']);saved.values.v7_sub_db=-31;disk[bound]=JSON.stringify(saved);delete disk[local];delete disk[local+'.bak'];
let boundContext=Context(bprofile);assert.equal(boundContext.state.v7_sub_db,-31);
boundContext.messagename='v7_sub_db';boundContext.anything(-27);boundContext.save();
assert.equal(JSON.parse(disk[bound]).values.v7_sub_db,-31);assert.equal(Context(bprofile).state.v7_sub_db,-27);
assert(!Context('v10').validDocument({schema_version:7,profile:'ev',values:{}},'v10'));
console.log(JSON.stringify({pass:true,profiles,scope:'JS VM I/O simulation only'}));
