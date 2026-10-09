/* Deterministic simulated Max File/Task harness; not native pattrstorage acceptance. */
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const code=fs.readFileSync('code/v7_profile_state.js','utf8');
const contracts=JSON.parse(fs.readFileSync('assets/v7/state_contracts.json'));
function Context(profile){
 let disk={},events=[],tasks=[];
 const factory=JSON.parse(fs.readFileSync('presets/v7_factories/'+profile+'_profile.json'));
 disk['/repo/presets/v7_factories/'+profile+'_profile.json']=JSON.stringify(factory);
 function File(path,mode){this.path=path;this.position=0;this.isopen=mode==='write'||disk[path]!==undefined;this.eof=(disk[path]||'').length;this.readstring=n=>{let s=disk[path].slice(this.position,this.position+n);this.position+=s.length;return s;};this.writestring=s=>{disk[path]=s;this.eof=s.length;};this.close=()=>{};}
 let c={File,Task:function(fn,self){this.schedule=()=>tasks.push(()=>fn.call(self));this.cancel=()=>{};},jsarguments:['x',profile],patcher:{filepath:'/repo/patchers/host.maxpat'},outlet:(...a)=>events.push(a),arrayfromargs:x=>Array.from(x),post:()=>{}};
 vm.createContext(c);vm.runInContext(code,c);c.restore();
 return {c,disk,factory,events,send(n,...a){c.messagename=n;return c.anything(...a);},flush(){const t=tasks;tasks=[];for(let f of t)f();}};
}
let checks=0;
for (let profile of Object.keys(contracts)) {
 let {c,disk,factory,send,flush}=Context(profile),local='/repo/presets/local/v7_'+profile+'_profile.json';
 assert(c.validDocument(factory,profile));checks++;
 let old=JSON.parse(JSON.stringify(factory));delete old.schema_revision;
 for(let key of ['v7_order2_db','v7_order3_db','v7_speed_weight_db','v7_speed_edge_db'])delete old.values[key];
 disk[local]=JSON.stringify(old);c.restore();assert.equal(c.state.v7_speed_weight_db,0);assert(c.validDocument(old,profile));checks++;
 let missing=JSON.parse(JSON.stringify(factory));delete missing.values.v7_core_db;
 let range=JSON.parse(JSON.stringify(factory));range.values.v7_sub_db=100;
 let partial=JSON.parse(JSON.stringify(factory));partial.schema_revision=2;delete partial.values.v7_order2_db;
 for(let bad of [missing,range,partial])assert(!c.validDocument(bad,profile));checks+=3;
 let backup=JSON.parse(JSON.stringify(factory));backup.values.v7_sub_db=-33;
 let bound=JSON.parse(JSON.stringify(factory));bound.values.v7_sub_db=-29;
 disk[local+'.bak']=JSON.stringify(backup);disk['/repo/presets/v7_bindings/'+profile+'_profile.json']=JSON.stringify(bound);
 disk[local]=JSON.stringify(range);c.restore();assert.equal(c.state.v7_sub_db,-33);delete disk[local];c.restore();assert.equal(c.state.v7_sub_db,-33);checks+=2;
 send('v7_order2_db',-6);send('v7_speed_weight_db',2);send('save_profile_sound');
 let saved=JSON.parse(disk[local]);assert.equal(saved.schema_revision,2);assert.equal(saved.values.v7_order2_db,-6);assert.equal(saved.values.v7_speed_weight_db,2);
 let result=c.verifyOwners();assert(!result.complete);assert.equal(result.confirmed,1);checks+=3;
 for(let owner of contracts[profile].slice(1)){
   disk['/repo/presets/local/v7_'+owner.file]=JSON.stringify({pattrstorage:{name:owner.storage,slots:{'1':{data:{knob:[.6]}}}}});
 }
 result=c.verifyOwners();assert.equal(result.valid,8);assert.equal(result.confirmed,1);assert(!result.complete);checks++;
 send('v7_storage_notice','wrong_engine',1);assert.equal(c.verifyOwners().confirmed,1);checks++;
 for(let owner of contracts[profile].slice(1))send('v7_storage_notice',owner.storage,1);
 flush();result=c.verifyOwners();assert(result.complete);assert.equal(result.confirmed,8);checks++;
 let last=contracts[profile].slice(-1)[0];
 send('v7_storage_notice',last.storage,'v7_'+last.file,0);assert(!c.verifyOwners().complete);checks++;
 send('v7_storage_notice',last.storage,'other_engine.json',1);assert(!c.verifyOwners().complete);checks++;
 send('v7_storage_notice',last.storage,1);send('v7_storage_notice',last.storage,0);assert(!c.verifyOwners().complete);checks++;
 send('v7_storage_notice',last.storage,1);disk['/repo/presets/local/v7_'+last.file]=JSON.stringify({pattrstorage:{name:'wrong_engine',slots:{'1':{data:{x:[1]}}}}});assert(!c.verifyOwners().complete);checks++;
 send('save_profile_sound');assert.equal(c.verifyOwners().confirmed,1);checks++;
}
console.log(JSON.stringify({pass:true,checks,scope:'Simulated JS File/Task; native save/reopen still required.'}));
