import { test } from 'node:test';
import assert from 'node:assert/strict';
import { report } from './period-report.mjs';
const options = {start:'2026-01-02',end:'2026-01-03',timezone:'Asia/Tokyo',actor:'dev'};
const event = {id:'1',source:'forge',kind:'authored',title:'Add bounded reads',actor:'dev',timestamp:'2026-01-01T16:00:00Z',status:'open',url:'https://example.test/mr/1?token=private'};
test('local date boundaries, deduplication and attribution are preserved',()=>{
 const text=report([event,event,{...event,id:'2',actor:'other'},{...event,id:'3',kind:'review',subject_author:'dev'}],options);
 assert.match(text,/2026-01-02 \| authored/);assert.match(text,/Included 1 unique records/);assert.match(text,/\| open \|/);assert.doesNotMatch(text,/token=|private/);
});
test('a wider period uses supplied bounds without imposing yesterday',()=>{
 const text=report([{...event,timestamp:'2026-01-03T15:01:00Z'}],options);
 assert.match(text,/No matching evidence/);assert.match(text,/Coverage is limited/);
});
test('invalid dates, timestamps and unsafe source URLs fail',()=>{
 assert.throws(()=>report([event],{...options,start:'2026-02-30'}),/real YYYY/);
 assert.throws(()=>report([{...event,timestamp:'2026-01-02'}],options),/ISO timestamp/);
 assert.throws(()=>report([{...event,url:'javascript:alert(1)'}],options),/HTTP/);
});

test('equivalent instants are deduplicated and impossible dates are refused',()=>{
 const equivalent={...event,timestamp:event.timestamp.replace('Z','+00:00')};
 assert.match(report([event,equivalent],options),/Included 1 unique records/);
 assert.throws(()=>report([{...event,timestamp:'2026-02-30T12:00:00Z'}],{...options,start:'2026-03-01',end:'2026-03-03'}),/date|timestamp/);
});
test('documented reviewed kind excludes self-review',()=>{
 assert.match(report([{...event,kind:'reviewed',subject_author:'dev'}],options),/No matching evidence/);
});

test('CLI refuses aliased input/output before overwriting',async()=>{
 const {mkdtempSync,writeFileSync,readFileSync,symlinkSync,rmSync}=await import('node:fs');
 const {tmpdir}=await import('node:os');const {join}=await import('node:path');const {spawnSync}=await import('node:child_process');
 const directory=mkdtempSync(join(tmpdir(),'period-guard-'));
 try {
  const input=join(directory,'evidence.json'),raw=JSON.stringify([event]);writeFileSync(input,raw);
  symlinkSync(directory,join(directory,'alias'));
  const result=spawnSync(process.execPath,[new URL('./period-report.mjs',import.meta.url).pathname,'--input',input,'--output',join(directory,'alias/evidence.json'),'--start',options.start,'--end',options.end,'--timezone',options.timezone,'--actor',options.actor,'--overwrite'],{encoding:'utf8'});
  assert.notEqual(result.status,0);assert.equal(readFileSync(input,'utf8'),raw);
 } finally {rmSync(directory,{recursive:true,force:true});}
});
