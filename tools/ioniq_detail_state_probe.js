/* QA only: exercise live nested UI -> Save/Reload/Reset, never production. */
autowatch = 1;
var tasks = [], result = {checks:[]};
function later(fn,ms) {var t=new Task(fn,this);tasks.push(t);t.schedule(ms);}
function bang() {
    try {
        var dna=this.patcher.getnamed('qa_voice').subpatcher();
        var state=dna.getnamed('qa_state');
        var macro=dna.getnamed('dna_motor_order');
        var filter=dna.getnamed('DNA_Cavity').subpatcher().getnamed('Freq');
        var mixer=dna.getnamed('DNA_Layer_Mixer').subpatcher().getnamed('in2');
        function values() {return [Number(macro.getvalueof()),Number(filter.getvalueof()),Number(mixer.getvalueof())];}
        function check(name,expected) {
            var actual=values();
            result.checks.push({name:name,actual:actual,expected:expected,
                pass:actual.every(function(x,i){return Math.abs(x-expected[i])<.001;})});
        }
        result.designer_path=dna.filepath;
        check('initial factory',[.72,315,-5]);
        macro.message(.41);filter.message(460);mixer.message(-12);
        state.message('save');
        later(function() {
            macro.message(.1);filter.message(200);mixer.message(-20);
            state.message('restore');
            later(function() {
                check('save then reload',[.41,460,-12]);
                state.message('reset');
                later(function() {
                    check('factory reset',[.72,315,-5]);
                    macro.message(.1);filter.message(200);mixer.message(-20);
                    state.message('restore');
                    later(function() {check('reset persisted',[.72,315,-5]);finish();},250);
                },250);
            },250);
        },200);
    } catch(error) {result.error=String(error);finish();}
}
function finish() {
    var file=new File(String(jsarguments[1]),'write','TEXT');
    if(file.isopen) {file.writestring(JSON.stringify(result));file.close();}
    post('IONIQ state QA '+JSON.stringify(result)+'\n');
}
function notifydeleted() {for(var i=0;i<tasks.length;i++)tasks[i].cancel();}
