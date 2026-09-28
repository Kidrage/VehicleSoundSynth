#!/usr/bin/env python3
"""Audit actual exported WAVs; no source/component identity or CAN values inferred.
Reports finite/silence/clipping, 7 band RMS values and narrow-line concentration.
Narrow-line share is a review flag, never an automatic realism verdict.
"""
from __future__ import annotations
import argparse,csv,json,math
from pathlib import Path
import numpy as np
import soundfile as sf
BANDS=[(20,120),(120,250),(250,600),(600,1200),(1200,2000),(2000,6000),(6000,12000)]

def analyze(path:Path):
    x,sr=sf.read(path,always_2d=True,dtype='float64');info=sf.info(path)
    if not len(x) or not np.isfinite(x).all(): raise ValueError('Empty/non-finite WAV: '+str(path))
    if np.max(abs(x))<1e-10: raise ValueError('Silent WAV: '+str(path))
    n=1<<int(math.ceil(math.log2(sr*.5)));hop=n//2;rows=[]
    window=np.hanning(n);scale=sr*np.sum(window**2)
    for start in range(0,max(1,len(x)-n+1),hop):
        seg=x[start:start+n];valid=len(seg)
        if len(seg)<n:seg=np.pad(seg,((0,n-len(seg)),(0,0)))
        fft=np.fft.rfft(seg*window[:,None],axis=0);p=np.mean(abs(fft)**2,axis=1)*2/scale
        p[0]*=.5;p[-1]*=.5;f=np.fft.rfftfreq(n,1/sr);df=sr/n
        row={'time_s':round(start/sr,6),'rms_dbfs':20*np.log10(max(np.sqrt(np.mean(seg[:valid]**2)),1e-12))}
        for lo,hi in BANDS:row[f'{lo}_{hi}_dbfs']=10*np.log10(max(np.sum(p[(f>=lo)&(f<min(hi,sr/2))])*df,1e-24))
        mask=(f>=20)&(f<=6000);total=np.sum(p[mask]);eligible=np.where(mask)[0];peak=eligible[np.argmax(p[mask])]
        share=np.sum(p[max(0,peak-1):peak+2])/max(total,1e-24)
        row.update(peak_line_hz=float(f[peak]),peak_3bin_share=float(share),review_dominant_line=bool(share>.45));rows.append(row)
    # Mid/Side and correlation are recording descriptors, not physical stem separation.
    stereo=None
    if x.shape[1]==2:
        l,r=x[:,0],x[:,1];mid=(l+r)*.5;side=(l-r)*.5
        stereo={'lr_correlation':float(np.corrcoef(l,r)[0,1]) if np.std(l)*np.std(r)>1e-12 else None,
                'side_minus_mid_db':float(20*np.log10(max(np.sqrt(np.mean(side**2)),1e-12)/max(np.sqrt(np.mean(mid**2)),1e-12)))}
    return {'file':path.name,'sample_rate':sr,'channels':x.shape[1],'frames':len(x),'duration_s':len(x)/sr,'format':info.format,'subtype':info.subtype,
            'sample_peak_dbfs':float(20*np.log10(max(np.max(abs(x)),1e-12))),
            'rms_dbfs':float(20*np.log10(max(np.sqrt(np.mean(x*x)),1e-12))),
            'near_full_scale_samples':int(np.sum(abs(x)>=.9999)),
            'dominant_line_review_frames':sum(r['review_dominant_line'] for r in rows),'stereo':stereo,
            'scope':'WAV sample/FFT analysis; no LUFS/true-peak/car-SPL/component-origin/RPM inferred'},rows

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('wav',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    try:info,rows=analyze(a.wav)
    except (OSError,ValueError) as e:raise SystemExit(str(e))
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'summary.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n')
    with (a.out/'band_features.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    print(json.dumps(info,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
