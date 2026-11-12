"""Acuerdo por criterio. No rellena datos faltantes ni mezcla consenso con evaluación."""
import argparse, csv, json
from collections import Counter

def read(path):
    with open(path,encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
    result={}
    for r in rows:
        key=(r['video'],r['sha256'],r['criterio'])
        if key in result:raise ValueError('Fila duplicada: '+str(key))
        value=r['puntuacion_0_1_2_3_NA_NE'].strip().upper()
        if value not in {'','0','1','2','3','NA','NE'}:raise ValueError('Código no válido: '+value)
        if value in {'0','1','2'} and not r['id_defectos'].strip():raise ValueError('Falta defecto para puntuación '+str(key))
        result[key]=value
    return result

def summarize(a,b):
    if set(a)!=set(b):raise ValueError('Las matrices difieren en videos, hashes o criterios')
    output={}
    for criterion in sorted({k[2] for k in a}):
        keys=[k for k in a if k[2]==criterion]
        pairs=[(int(a[k]),int(b[k])) for k in keys if a[k].isdigit() and b[k].isdigit()]
        n=len(pairs); exact=sum(x==y for x,y in pairs)
        kappa=None
        if n:
            ca=Counter(x for x,y in pairs); cb=Counter(y for x,y in pairs)
            observed=sum(abs(x-y)/3 for x,y in pairs)/n
            expected=sum(ca[i]*cb[j]*abs(i-j)/3 for i in range(4) for j in range(4))/n**2
            if expected>0:kappa=1-observed/expected
        output[criterion]={'videos':len(keys),'pares_numericos':n,'acuerdos_exactos':exact,'proporcion_acuerdo':exact/n if n else None,'kappa_lineal_descriptivo':kappa,'codigos_R1':dict(Counter(a[k] or 'faltante' for k in keys)),'codigos_R2':dict(Counter(b[k] or 'faltante' for k in keys))}
    return output

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--r1',required=True);p.add_argument('--r2',required=True);p.add_argument('--out',required=True);args=p.parse_args()
    result={'nota':'Descriptivo por criterio; no supone independencia entre ítems o videos. Kappa puede ser inestable con diez videos. null significa no estimable.','criterios':summarize(read(args.r1),read(args.r2))}
    with open(args.out,'w',encoding='utf8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
    print('Pares puntuados:',sum(r['pares_numericos'] for r in result['criterios'].values()))
