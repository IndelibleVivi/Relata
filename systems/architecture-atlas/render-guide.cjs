const layouts=require('./guide-layouts.cjs');
module.exports=function renderGuide(model,view,{text,wrap,esc,palette,statusText,nodeNames,edges,prefix}){
  const plan=layouts[model.id]?.[view.id];
  if(!plan)throw new Error(`${model.id}/${view.id}: missing authored reading path`);
  const chosen=plan.rows.flat(), items=new Map(), cross=[], same=[];
  const note=wrap(plan.note,1016,16);
  const top=255+note.length*24, width=272;
  let nodeHeight=134;
  for(const id of chosen){
    const n=view.nodes.find(n=>n.id===id);if(!n)throw new Error(`${model.id}/${view.id}: guide node ${id} missing`);
    const label=wrap(n.label,width-28,18),region=view.regions.find(r=>r.id===n.region);
    const owner=wrap(region.label,width-28,14);
    nodeHeight=Math.max(nodeHeight,54+label.length*23+owner.length*19);
    items.set(id,{...n,labelLines:label,ownerLines:owner});
  }
  plan.rows.forEach((row,r)=>row.forEach((id,c)=>Object.assign(items.get(id),{x:32+c*372,y:top+r*(nodeHeight+130),row:r,col:c})));
  plan.edges.forEach(([from,to,verb],i)=>{
    const edge=edges.find(e=>e.from===from&&e.to===to);
    if(!edge)throw new Error(`${model.id}/${view.id}: guide relation ${from} -> ${to} has no model evidence`);
    const item={...edge,verb,a:items.get(from),b:items.get(to),guideIndex:i};
    if(!item.a||!item.b)throw new Error(`${model.id}/${view.id}: guide endpoint missing`);
    (item.a.row===item.b.row?same:cross).push(item);
  });
  const end=top+plan.rows.length*nodeHeight+(plan.rows.length-1)*130;
  let svg=`<g id="${prefix}-reading-path">`;
  svg+=text(32,204,'主路径导读',{size:21,weight:600,role:'critical'});
  svg+=text(186,203,'展开已有关系 · 不是全部分支或唯一执行顺序',{size:16,fill:'#526b70'});
  svg+=text(32,236,note,{size:16,line:24});
  const route=(e,d,lx,ly,lw=100,anchor='middle')=>{
    const offset=plan.labelOffsets?.[`${e.from}>${e.to}`]||[0,0];lx+=offset[0];ly+=offset[1];
    const lines=wrap(`${e.id} ${e.verb}${e.status==='observed'?'':'〔'+statusText[e.status]+'〕'}`,lw,16);
    let label=text(lx,ly-(lines.length-1)*21,lines,{size:16,line:21,anchor,fill:'#315862'});
    // A narrow paper halo keeps verbs opaque where a second route crosses.
    label=label.replace('<text ','<text stroke="#ffffff" stroke-width="6" stroke-linejoin="round" paint-order="stroke fill" ');
    return `<g class="guide-edge" data-edge-reference="${e.id}"><title>${esc(e.id+' '+e.label+' · '+e.evidence.join(', '))}</title><path d="${d}" fill="none" stroke="#527982" stroke-width="2" marker-end="url(#${prefix}-arrow)"${e.status==='observed'?'':' stroke-dasharray="5 4"'}/>${label}</g>`;
  };
  for(const e of same){
    const a=e.a,b=e.b,forward=a.col<b.col;
    const ay=a.y+nodeHeight/2, sx=forward?a.x+width:a.x,tx=forward?b.x:b.x+width;
    if(Math.abs(a.col-b.col)===1)svg+=route(e,`M${sx} ${ay}H${tx}`, (sx+tx)/2,ay-12,90);
    else {const upper=a.y-22;svg+=route(e,`M${a.x+width/2} ${a.y}V${upper}H${b.x+width/2}V${b.y}`,540,upper-10,280);}
  }
  for(let i=0;i<cross.length;i++){
    const e=cross[i],a=e.a,b=e.b,down=a.row<b.row,sx=a.x+width/2,tx=b.x+width/2;
    const sy=down?a.y+nodeHeight:a.y,ty=down?b.y:b.y+nodeHeight;
    const mid=(sy+ty)/2+(i-(cross.length-1)/2)*13;
    let lx=(sx+tx)/2,ly=mid-10,lw=250;
    if(a.col===b.col){lx=sx+(a.col===2?-142:142);ly=mid+6;lw=230;}
    else if(cross.length>2){lx=tx;ly=mid-8;lw=250;}
    svg+=route(e,`M${sx} ${sy}V${mid}H${tx}V${ty}`,lx,ly,lw);
  }
  for(const [id,n] of items){
    const [fill,stroke]=palette[n.kind];
    const source=model.sources.find(s=>s.id===n.evidence[0]);
    if(source)svg+=`<a href="${esc(source.url)}" target="_blank">`;
    svg+=`<g class="guide-node" data-node-reference="${id}"><title>${esc(n.label+' · '+n.note+' · '+n.evidence.join(', '))}</title><rect x="${n.x}" y="${n.y}" width="${width}" height="${nodeHeight}" fill="${fill}" stroke="${stroke}"${n.status==='observed'?'':' stroke-dasharray="5 4"'}/>`;
    svg+=text(n.x+14,n.y+23,`${nodeNames.get(id)}${n.status==='observed'?'':' · '+statusText[n.status]}`,{size:14,fill:'#526b70',role:'supporting'});
    svg+=text(n.x+14,n.y+51,n.labelLines,{size:18,line:23,weight:500});
    svg+=text(n.x+14,n.y+nodeHeight-13-(n.ownerLines.length-1)*19,n.ownerLines,{size:14,line:19,fill:'#526b70',role:'supporting'});
    svg+='</g>';
    if(source)svg+='</a>';
  }
  svg+=text(32,end+45,'完整结构与所有关系',{size:21,weight:600,role:'critical'});
  svg+=text(32,end+72,'以下按真实边界展开；相同 N / E 编号沿用上方导读。点击节点可查看固定版本的证据。',{size:16,fill:'#526b70'});
  svg+='</g>\n';
  return {svg,height:end+100};
};
