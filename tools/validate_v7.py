#!/usr/bin/env python3
"""Run all legacy and V7 tests; portable mode explicitly reports unavailable dependencies.
Assertions and unknown errors always fail. No skip is a native/Max acceptance.
"""
from __future__ import annotations
import argparse,json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))


def dependency_reason(error):
    exc=error[1]
    if isinstance(exc,FileNotFoundError):
        text=str(exc)
        if 'BEAP clipping not found:' in text: return 'Max 8.6.5 / BEAP clippings unavailable'
        if '/usr/bin/afconvert' in text: return 'macOS afconvert unavailable'
    if isinstance(exc,subprocess.CalledProcessError):
        stderr=exc.stderr or b''
        if isinstance(stderr,bytes):stderr=stderr.decode('utf-8','replace')
        if 'BEAP clipping not found:' in stderr:return 'Max / BEAP needed by legacy generator unavailable'
        args=list(exc.cmd) if isinstance(exc.cmd,(list,tuple)) else []
        # One legacy test executes git show inside a Node subprocess, whose stderr
        # is inherited rather than returned. Skip only if its literal required
        # historical commit is genuinely absent, never for other Node failures.
        if args[:2]==['node','-e'] and len(args)>2 and "['show','cff9d08:code/drive_model.js']" in args[2]:
            available=subprocess.run(['git','cat-file','-e','cff9d08^{commit}'],cwd=ROOT,capture_output=True)
            if available.returncode:return 'Original historical commit not present in worktree archive: cff9d08'

        if args and args[0]=='git' and len(args)>2 and args[1] in ('show','ls-tree'):
            import re
            refs=[x.split(':')[0] for x in args[2:] if re.fullmatch(r'[0-9a-f]{7,40}(?::.*)?',x)]
            for ref in refs:
                available=subprocess.run(['git','cat-file','-e',ref+'^{commit}'],cwd=ROOT,capture_output=True)
                if available.returncode:return 'Original historical commit not present in worktree archive: '+ref
    return None


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--portable',action='store_true');parser.add_argument('--report',type=Path);args=parser.parse_args()
    class Result(unittest.TextTestResult):
        def addError(self,test,err):
            reason=dependency_reason(err) if args.portable else None
            if reason:self.addSkip(test,reason)
            else:super().addError(test,err)
    suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'))
    result=unittest.TextTestRunner(verbosity=2,resultclass=Result).run(suite)
    report={'scope':'Full legacy + V7 suite; native Max/BEAP/audio device/vehicle acceptance NOT executed',
      'mode':'portable' if args.portable else 'strict','tests_run':result.testsRun,
      'passed':result.testsRun-len(result.errors)-len(result.failures)-len(result.skipped),
      'failures':[t.id() for t,_ in result.failures],'errors':[t.id() for t,_ in result.errors],
      'skips':[{'test':t.id(),'reason':reason} for t,reason in result.skipped],
      'native_max_accepted':False,'vehicle_accepted':False,'portable_success':result.wasSuccessful()}
    if args.report:args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    return 0 if result.wasSuccessful() else 1
if __name__=='__main__':sys.exit(main())
