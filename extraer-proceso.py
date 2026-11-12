"""Extracción de solo lectura. No exporta conversaciones completas ni credenciales."""
import argparse, collections, hashlib, json, re, sqlite3
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('--db', required=True)
ap.add_argument('--out', required=True)
args = ap.parse_args()
out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
db = sqlite3.connect(Path(args.db).resolve().as_uri() + '?mode=ro', uri=True)
sessions = {
 'intro_m3': 'ses_eaf084409ffeHJjlRRmBnYDkmB',
 'video_sesion_m4': 'ses_eaefaa565ffeM0Dcgon5dmRa9k',
 'video_sesion_entregas': 'ses_eae37137bffeFbaIQykmqyfhSa',
 'video_m2': 'ses_eb3038cebffedtibT66O1J6iJ2',
 'epilogo': 'ses_ead57ff34ffe2iuDcwuJKqt16H',
}
results = []
for label, sid in sessions.items():
 rows = db.execute('select seq,type,time_created,data from session_message where session_id=? order by seq',(sid,)).fetchall()
 messages = [(q,ty,t,json.loads(d)) for q,ty,t,d in rows]
 assistants = [(q,t,d) for q,ty,t,d in messages if ty=='assistant']
 tool_counts=collections.Counter(); errors=[]; checks=[]; renders=[]; tokens=collections.Counter(); models=collections.Counter()
 for q,t,d in assistants:
  model=d.get('model',{}); models[model.get('providerID','')+'/'+model.get('id','')]+=1
  tok=d.get('tokens',{})
  for k in ['input','output','reasoning']:tokens[k]+=tok.get(k,0) or 0
  for k in ['read','write']:tokens['cache_'+k]+=tok.get('cache',{}).get(k,0) or 0
  for z in d.get('content',[]):
   if z.get('type')!='tool':continue
   tool_counts[z.get('name','')]+=1;st=z.get('state',{});inp=st.get('input',{});cmd=inp.get('command',inp.get('cmd',''))
   if st.get('status')=='error': errors.append({'seq':q,'tool':z.get('name'),'tipo':'error explícito de herramienta'})
   if re.search(r'hyperframes(?:@[^\s]+)?\s+check\b',cmd):checks.append(q)
   if re.search(r'hyperframes(?:@[^\s]+)?\s+render\b',cmd) and '--help' not in cmd:renders.append(q)
 ends=[d.get('time',{}).get('completed',t) or t for q,t,d in assistants]
 starts=[t for q,ty,t,d in messages if ty=='user']
 result={'unidad':'sesión; no necesariamente un video','etiqueta':label,'session_id':sid,'mensajes_usuario':len(starts),'mensajes_asistente':len(assistants),'modelos':dict(models),'herramientas':dict(tool_counts),'checks_seq':checks,'render_invocaciones_seq':renders,'errores_herramienta':errors,'tokens_campos_separados':dict(tokens),'cost_campo_opencode':sum(d.get('cost',0) or 0 for q,t,d in assistants),'duracion_pared_segundos':(max(ends)-min(starts))/1000 if ends and starts else None,'tiempo_humano_minutos':None,'costo_total_facturado':None}
 if label=='intro_m3':
  byseq={q:(t,d) for q,ty,t,d in messages}
  result['primera_entrega_segundos']=(byseq[1108][1]['time']['completed']-byseq[4][0])/1000
  result['revision_hasta_segunda_entrega_segundos']=(byseq[1502][1]['time']['completed']-byseq[1118][0])/1000
  text=byseq[4][1]['text']
  result['encargo_original_sha256']=hashlib.sha256(text.encode()).hexdigest()
  text=re.sub(r'[A-Za-z]:\\Users\\[^\\]+\\Proyectos\\mision-geometria-curso', '[PROYECTO]', text)
  text=re.sub(r'[A-Za-z]:\\Users\\[^\\]+\\Downloads\\Actualizacion\\Modulo 3\.txt', '[FUENTE]/Modulo 3.txt', text)
  (out/'encargo-m3-real-depurado.txt').write_text('Encargo real. Sesión de producción M3, secuencia 4. Solo se sustituyeron dos rutas personales por [PROYECTO] y [FUENTE]. Los nombres abreviados dentro de esta transcripción pertenecen al registro original. Modelo identificado en la bitácora: Xiaomi MiMo-V2.6-Flash.\n\n'+text,encoding='utf8')
 results.append(result)
(out/'metricas-sesiones.json').write_text(json.dumps({'fecha_extraccion':'2026-11-11','reglas':'Mensajes canónicos de session_message, tipo assistant; se cuenta cada invocación una vez. render --help excluido. completed de herramienta no prueba que el comando o el video pasara QA. Los errores explícitos no son inventario exhaustivo de fallos de proceso. cost es telemetría, no factura. Tiempo de pared no es tiempo humano.','sesiones':results},ensure_ascii=False,indent=2),encoding='utf8')
for r in results:print(r['etiqueta'],r['mensajes_asistente'],len(r['checks_seq']),len(r['render_invocaciones_seq']),len(r['errores_herramienta']),round(r['cost_campo_opencode'],6),round(r['duracion_pared_segundos']/60,2) if r['duracion_pared_segundos'] else None)
