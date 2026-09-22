/* Fixed-width architecture plates. Semantic truth remains in models/*.json.
 * Region order and node order are authored in each model. Long cross-region
 * routes use numbered source ports and matching arrival numbers; every edge is
 * drawn, and every exact action remains next to its source at reading size.
 * No HTML, fonts, network resources, browser, or layout service is required.
 */
const renderGuide = require('./render-guide.cjs');
const WIDTH = 1080;
const CARD = 418;
const X = [76, 586];
const FONT = 'Arial, "PingFang SC", "Microsoft YaHei", sans-serif';
const INK = '#203b42', MUTED = '#526b70', PAPER = '#ffffff';
const statusText = {observed:'已读源码', inferred:'推断', unknown:'未检查 / 未知'};
const kindText = {entry:'入口', process:'处理', decision:'选择 / 控制', store:'状态 / 存储', model:'模型', output:'交付', external:'外部'};
const palette = {entry:['#eaf2f3','#46666e'],process:['#ffffff','#a4b5b8'],decision:['#fff4df','#a78648'],store:['#e8f1e9','#55755e'],model:['#efedf6','#817694'],output:['#eaf2f3','#46666e'],external:['#f5f3ee','#999286']};
const esc = s => String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
// Deliberately conservative glyph widths leave tolerance for system-font fallback.
function units(s) { return [...s].reduce((n,c)=>n+(/[\u2e80-\uffff]/.test(c)?1:/[MW@%]/.test(c)?.8:/[il1.,:;|/ ()]/.test(c)?.35:.57),0); }
function wrap(s, width, size) {
  const limit=width/size, lines=[];
  for(const para of String(s).split('\n')) {
    let line='';
    for(const token of para.match(/[A-Za-z0-9_./:+-]+|[^A-Za-z0-9_./:+-]/g)||['']) {
      if(line && units(line+token)>limit){lines.push(line.trimEnd());line='';}
      if(units(token)>limit) {
        for(const c of token){if(line&&units(line+c)>limit){lines.push(line);line='';}line+=c;}
      } else line+=token;
    }
    lines.push(line.trimEnd());
  }
  return lines;
}
function text(x,y,lines,{size=17,weight=400,fill=INK,line=24,cls='',anchor='start',role='body'}={}) {
  if(!Array.isArray(lines)) lines=[lines];
  return `<text x="${x}" y="${y}" font-size="${size}" font-weight="${weight}" fill="${fill}" text-anchor="${anchor}" data-readability="${role}"${cls?` class="${cls}"`:''}>${lines.map((s,i)=>`<tspan x="${x}" dy="${i?line:0}">${esc(s)}</tspan>`).join('')}</text>`;
}
function renderSvg(model,view) {
  const prefix=`atlas-${model.id}-${view.id}`, nodes=new Map(), nodeNames=new Map(), edges=view.edges.map((e,i)=>({...e,id:`E${String(i+1).padStart(2,'0')}`,index:i}));
  view.nodes.forEach((n,i)=>nodeNames.set(n.id,`N${String(i+1).padStart(2,'0')}`));
  const guide=renderGuide(model,view,{text,wrap,esc,palette,statusText,nodeNames,edges,prefix});
  let y=guide.height;
  const regions=[], rows=[];
  for(const region of view.regions) {
    const members=view.nodes.filter(n=>n.region===region.id);
    if(!members.length)continue;
    const r={...region,y,rows:[]}; y+=60;
    for(let i=0;i<members.length;i+=2) {
      const row={nodes:members.slice(i,i+2), y};
      const incoming=edges.filter(e=>row.nodes.some(n=>n.id===e.to));
      row.arrivalSpace=Math.max(42, incoming.length*6+20);
      y+=row.arrivalSpace;
      let h=0;
      row.nodes.forEach((n,col)=>{
        const outgoing=edges.filter(e=>e.from===n.id);
        const lines=wrap(n.label,CARD-36,18);
        const titleHeight=Math.max(94,56+lines.length*25);
        let height=titleHeight;
        const ports=outgoing.map(e=>{
          const target=view.nodes.find(n=>n.id===e.to);
          const dest=wrap(`${e.id} → ${nodeNames.get(e.to)} · ${target.label.split('\n')[0]}${e.status==='observed'?'':'〔'+statusText[e.status]+'〕'}`,CARD-34,16);
          const action=wrap(e.label,CARD-34,16);
          const p={edge:e,dest,action,offset:height,height:18+dest.length*21+action.length*23};
          height+=p.height;return p;
        });
        if(!outgoing.length)height+=34;
        nodes.set(n.id,{...n,x:X[col],y,w:CARD,h:height,titleHeight,lines,ports,col,row,incoming:edges.filter(e=>e.to===n.id)});
        h=Math.max(h,height);
      });
      row.h=h;rows.push(row);r.rows.push(row);y+=h+30;
    }
    r.h=y-r.y;regions.push(r);y+=26;
  }
  const stateY=y+20;
  let stateBottom=stateY+62;
  const stateBlocks=[];
  for(let i=0;i<view.state_notes.length;i+=2) {
    let rowHeight=0;
    view.state_notes.slice(i,i+2).forEach((s,col)=>{
      const parts=[['状态归属',s.owner],['允许写入',s.writers],['变化与传播',s.changes],['边界',s.limits]];
      const lines=parts.flatMap(([k,v])=>wrap(`${k} · ${v}`,446,16));
      const h=lines.length*25+58;
      stateBlocks.push({s,col,y:stateBottom,lines,h});rowHeight=Math.max(rowHeight,h);
    });
    stateBottom+=rowHeight+22;
  }
  const height=(stateBlocks.length?stateBottom:stateY)+50;
  let svg=`<svg xmlns="http://www.w3.org/2000/svg" width="${WIDTH}" height="${height}" viewBox="0 0 ${WIDTH} ${height}" lang="zh-CN" role="img" aria-labelledby="${prefix}-title ${prefix}-desc" data-renderer="relata-native-svg-1" data-min-display-width="900">\n`;
  svg+=`<title id="${prefix}-title">${esc(model.name+' · '+view.title)}</title>\n<desc id="${prefix}-desc">${esc(view.question+' '+view.reading_guide+' 所有节点、关系和状态均来自固定版本公开源码的研究模型，不代表运行结果。节点 N 编号唯一；每条 E 关系在起点写明目标与完整动作，沿同号线路到达目标。')}</desc>\n`;
  svg+=`<style>text{font-family:${esc(FONT)}} .route{fill:none;stroke:#899da3;stroke-width:1.3;stroke-linejoin:round} .edge:hover .route{stroke:#bb5b35;stroke-width:3} .node{cursor:pointer} .node:hover .node-main{stroke:#bb5b35;stroke-width:2} .selected .node-main{stroke:#bb5b35;stroke-width:3}</style>\n`;
  svg+=`<defs><marker id="${prefix}-arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#607b82"/></marker></defs>\n<rect width="${WIDTH}" height="${height}" fill="${PAPER}"/>\n`;
  svg+=text(32,38,`${model.name} / ${view.title}`,{size:25,weight:600,role:'critical'});
  svg+=text(32,73,wrap(view.question,1016,17),{size:17,line:25});
  svg+=text(32,124,'N = 节点  ·  E = 有向关系；起点列出目标与完整动作，同号线箭头抵达目标。',{size:16,fill:MUTED});
  svg+=text(32,149,`公开源码研究 · ${model.commit.slice(0,12)} · ${view.nodes.length} 节点 / ${edges.length} 关系；虚线表示推断或未检查。`,{size:14,fill:MUTED,role:'supporting'});
  svg+=`<path d="M32 168H1048" stroke="#ccd7d7"/>\n`;
  svg+=guide.svg;
  // Boundaries first; cross-boundary wires next; opaque component text last.
  for(const r of regions) {
    svg+=`<g id="${prefix}-region-${r.id}" data-region="${r.id}" data-status="${r.status}" data-evidence="${r.evidence.join(' ')}"><title>${esc(r.label+' · '+statusText[r.status]+' · '+r.responsibility)}</title><rect x="68" y="${r.y}" width="944" height="${r.h}" rx="3" fill="#f7f9f8" stroke="#c7d3d2"${r.status!=='observed'?' stroke-dasharray="6 4"':''}/>`;
    svg+=text(84,r.y+28,r.label,{size:18,weight:600});
    svg+=text(996,r.y+27,statusText[r.status],{size:14,fill:MUTED,anchor:'end',role:'supporting'});svg+='</g>\n';
  }
  const arrivalCounter=new Map(), laneCounters=[0,0];
  const sideCounts=[0,1].map(col=>edges.filter(e=>nodes.get(e.from).col===col).length);
  for(const e of edges) {
    const a=nodes.get(e.from),b=nodes.get(e.to),port=a.ports.find(p=>p.edge.id===e.id);
    const startY=a.y+port.offset+14;
    const sourceX=a.col===0?a.x:a.x+a.w;
    const laneOffset=laneCounters[a.col]++*52/Math.max(1,sideCounts[a.col]-1);
    const lane=a.col===0?10+laneOffset:1070-laneOffset;
    const count=arrivalCounter.get(b.row)||0;arrivalCounter.set(b.row,count+1);
    const arrivalY=b.row.y+12+count*6;
    const targetSlot=b.incoming.findIndex(x=>x.id===e.id);
    const targetX=b.x+25+targetSlot*Math.min(45,(CARD-50)/Math.max(1,b.incoming.length-1));
    // Every edge has its own source action row. The outer route never crosses
    // component bodies; its destination trunk stays in the row's arrival gutter.
    const d=`M${sourceX} ${startY}H${lane}V${arrivalY}H${targetX}V${b.y-3}`;
    svg+=`<g class="edge" id="${prefix}-edge-${e.id}" data-edge="${e.id}" data-from="${e.from}" data-to="${e.to}" data-status="${e.status}" data-evidence="${e.evidence.join(' ')}"><title>${esc(e.id+' '+nodeNames.get(e.from)+' '+a.label.replaceAll('\n',' / ')+' → '+nodeNames.get(e.to)+' '+b.label.replaceAll('\n',' / ')+': '+e.label+' ['+statusText[e.status]+'] '+e.evidence.join(', '))}</title><path class="route" d="${d}" marker-end="url(#${prefix}-arrow)"${e.status!=='observed'?' stroke-dasharray="5 4"':''}/></g>\n`;
  }
  for(const n of nodes.values()) {
    const [fill,stroke]=palette[n.kind];
    const source=model.sources.find(s=>s.id===n.evidence[0]);
    if(source)svg+=`<a href="${esc(source.url)}" target="_blank">`;
    svg+=`<g class="node ${n.kind} ${n.status}" id="${prefix}-flowchart-${n.id}-0" data-node="${n.id}" data-status="${n.status}" data-evidence="${n.evidence.join(' ')}"><title>${esc(n.label+' · '+statusText[n.status]+' · '+n.note+' ['+n.evidence.join(', ')+']')}</title>`;
    svg+=`<rect x="${n.x}" y="${n.y}" width="${CARD}" height="${n.h}" fill="#ffffff" stroke="#d5dfdf"/>`;
    svg+=`<rect class="node-main" x="${n.x}" y="${n.y}" width="${CARD}" height="${n.titleHeight}" fill="${fill}" stroke="${stroke}"${n.status!=='observed'?' stroke-dasharray="5 4"':''}/>`;
    if(n.kind==='store')svg+=`<path d="M${n.x+1} ${n.y+5}H${n.x+CARD-1}" stroke="${stroke}" stroke-width="3"/>`;
    if(n.kind==='model')svg+=`<path d="M${n.x+5} ${n.y+1}V${n.y+n.titleHeight-1}" stroke="${stroke}" stroke-width="3"/>`;
    if(n.kind==='decision')svg+=`<path d="M${n.x+CARD-26} ${n.y+16}l6 -6 6 6 -6 6Z" fill="${stroke}"/>`;
    svg+=text(n.x+16,n.y+23,`${nodeNames.get(n.id)} · ${kindText[n.kind]}${n.status==='observed'?'':' · '+statusText[n.status]}`,{size:14,fill:MUTED,role:'supporting'});
    svg+=text(n.x+16,n.y+51,n.lines,{size:18,line:25,weight:500});
    // Arrival numbers live immediately above arrowheads, with opaque paper to
    // distinguish overlaid cross-routes without concealing the endpoint.
    n.incoming.forEach((e,i)=>{
      const tx=n.x+25+i*Math.min(45,(CARD-50)/Math.max(1,n.incoming.length-1));
      svg+=`<rect x="${tx-16}" y="${n.y-23}" width="32" height="17" fill="#f7f9f8"/>`+text(tx,n.y-10,e.id,{size:14,anchor:'middle',fill:MUTED,role:'supporting'});
    });
    for(const port of n.ports) {
      const py=n.y+port.offset;
      svg+=`<g data-edge-label="${port.edge.id}"><title>${esc(statusText[port.edge.status]+' · '+port.edge.evidence.join(', '))}</title><path d="M${n.x+12} ${py}H${n.x+CARD-12}" stroke="#dde4e3"/>`;
      svg+=text(n.x+16,py+23,port.dest,{size:16,line:21,weight:500,fill:'#355d67'});
      svg+=text(n.x+16,py+23+port.dest.length*21,port.action,{size:16,line:23});
      if(port.edge.status!=='observed')svg+=`<path d="M${n.x+3} ${py+8}V${py+port.height-7}" stroke="#917445" stroke-width="2" stroke-dasharray="4 3"/>`;
      svg+='</g>';
    }
    if(!n.ports.length)svg+=text(n.x+16,n.y+n.titleHeight+23,'本视图未继续画出出站关系',{size:14,fill:MUTED,role:'supporting'});
    svg+='</g>\n';
    if(source)svg+='</a>\n';
  }
  if(stateBlocks.length){
    svg+=text(32,stateY+26,'状态归属、允许写入与传播边界',{size:21,weight:600,role:'critical'});
    for(const b of stateBlocks){const x=b.col?560:32;svg+=`<g id="${prefix}-state-${stateBlocks.indexOf(b)+1}" data-evidence="${b.s.evidence.join(' ')}"><path d="M${x} ${b.y}H${x+486}" stroke="#cad7d1"/>`+text(x,b.y+29,b.lines,{size:16,line:25})+text(x,b.y+b.lines.length*25+39,`证据 ${b.s.evidence.join(' · ')}`,{size:14,fill:MUTED,role:'supporting'})+'</g>\n';}
  }
  return svg+'</svg>\n';
}
module.exports={renderSvg};
