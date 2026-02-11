function qs(sel, el=document){ return el.querySelector(sel); }
function qsa(sel, el=document){ return Array.from(el.querySelectorAll(sel)); }
const STORE_KEY = (window.BOARD_KEY || "meso-kanban") + ":" + (window.GRADE_KEY||"all");
function loadState(){
  try{ return JSON.parse(localStorage.getItem(STORE_KEY) || "{}"); }catch(e){ return {}; }
}
function saveState(state){
  localStorage.setItem(STORE_KEY, JSON.stringify(state));
}
function defaultState(cards){
  const s=loadState();
  s.columns = s.columns || {};
  s.checks = s.checks || {};
  s.hidden = s.hidden || {};
  for(const c of cards){
    if(!s.columns[c.id]) s.columns[c.id] = "intake";
    if(!s.checks[c.id]) s.checks[c.id] = {};
  }
  return s;
}

const COLUMNS = [
  {id:"intake", name:"Intake & Normalize"},
  {id:"chunk", name:"Chunk to Lesson Units"},
  {id:"artifactQA", name:"Artifact Spec QA"},
  {id:"assets", name:"Assets & Rights"},
  {id:"build", name:"Build (JSON/HTML)"},
  {id:"qa", name:"QA & Publish"},
];

const CHECKLIST = [
  {id:"md_ok", label:"Normalize MD (headings + section IDs)"},
  {id:"artifact_map", label:"Map artifacts to master CSV (or add new row)"},
  {id:"images", label:"Acquire/create images + captions + attribution"},
  {id:"alt", label:"Write alt text + accessibility check"},
  {id:"render", label:"Render in shell + spot-check nav"},
  {id:"review", label:"Peer/content review + fix notes"},
];

function renderBoard(cards){
  const state = defaultState(cards);
  const grid = qs("#board");
  grid.innerHTML = "";
  for(const col of COLUMNS){
    const colEl = document.createElement("section");
    colEl.className = "column";
    colEl.dataset.col = col.id;
    colEl.innerHTML = `
      <h3><span>${col.name}</span><span class="count" id="count-${col.id}">0</span></h3>
      <div class="dropzone" data-drop="${col.id}"></div>
    `;
    grid.appendChild(colEl);
  }

  function cardMatchesFilter(card){
    const q = (qs("#q").value || "").trim().toLowerCase();
    const week = (qs("#week").value || "");
    const day  = (qs("#day").value || "");
    if(week && card.week !== week) return false;
    if(day && card.day !== day) return false;
    if(!q) return true;
    const hay = (card.week + " " + card.day + " " + card.section + " " + card.items.join(" ")).toLowerCase();
    return hay.includes(q);
  }

  function renderCards(){
    qsa(".dropzone").forEach(z => z.innerHTML = "");
    const colCounts = Object.fromEntries(COLUMNS.map(c => [c.id,0]));

    for(const card of cards){
      if(!cardMatchesFilter(card)) continue;
      const colId = state.columns[card.id] || "intake";
      const zone = qs(`.dropzone[data-drop="${colId}"]`);
      if(!zone) continue;

      const el = document.createElement("article");
      el.className = "card";
      el.draggable = true;
      el.dataset.id = card.id;

      const checks = state.checks[card.id] || {};
      const itemsHtml = card.items.length
        ? ("<ul class='small' style='margin:6px 0 6px 18px; padding:0'>" +
           card.items.map(it => `<li>${escapeHtml(it)}</li>`).join("") +
           "</ul>")
        : `<div class="small">(artifact block exists, but parsing didn't find bullet items)</div>`;

      el.innerHTML = `
        <div class="meta">
          <span class="tag">${escapeHtml(card.grade)}</span>
          <span class="tag">${escapeHtml(card.day||"")}</span>
        </div>
        <div class="name">${escapeHtml(card.week || "Week ?")} - ${escapeHtml(card.section || "Section ?")}</div>
        <details>
          <summary class="small">Artifact details</summary>
          <div class="details">${itemsHtml}<div class="small" style="margin-top:6px">Raw preview: ${escapeHtml(card.raw_preview)}</div></div>
        </details>
        <div class="checks">
          ${CHECKLIST.map(ch => `
            <label>
              <input type="checkbox" data-check="${ch.id}" ${checks[ch.id] ? "checked" : ""}>
              <span>${escapeHtml(ch.label)}</span>
            </label>
          `).join("")}
        </div>
        <div class="small" style="margin-top:10px; display:flex; justify-content:space-between; gap:10px; flex-wrap:wrap;">
          <span>Move: 
            <select data-move>
              ${COLUMNS.map(c => `<option value="${c.id}" ${c.id===colId ? "selected":""}>${escapeHtml(c.name)}</option>`).join("")}
            </select>
          </span>
          <span class="tag">id: ${escapeHtml(card.id.slice(0,28))}</span>
        </div>
      `;

      el.addEventListener("dragstart", (ev)=>{
        el.classList.add("dragging");
        ev.dataTransfer.setData("text/plain", card.id);
      });
      el.addEventListener("dragend", ()=>{
        el.classList.remove("dragging");
      });

      el.addEventListener("change", (ev)=>{
        const t = ev.target;
        if(t && t.matches("input[data-check]")){
          const key = t.dataset.check;
          state.checks[card.id] = state.checks[card.id] || {};
          state.checks[card.id][key] = t.checked;
          saveState(state);
        }
        if(t && t.matches("select[data-move]")){
          state.columns[card.id] = t.value;
          saveState(state);
          renderCards();
        }
      });

      zone.appendChild(el);
      colCounts[colId] += 1;
    }

    for(const col of COLUMNS){
      qs(`#count-${col.id}`).textContent = String(colCounts[col.id] || 0);
    }
  }

  qsa(".dropzone").forEach(zone=>{
    zone.addEventListener("dragover", (ev)=>{ ev.preventDefault(); });
    zone.addEventListener("drop", (ev)=>{
      ev.preventDefault();
      const id = ev.dataTransfer.getData("text/plain");
      const col = zone.dataset.drop;
      if(id && col){
        state.columns[id] = col;
        saveState(state);
        renderCards();
      }
    });
  });

  qs("#q").addEventListener("input", renderCards);
  qs("#week").addEventListener("change", renderCards);
  qs("#day").addEventListener("change", renderCards);
  qs("#reset").addEventListener("click", ()=>{
    localStorage.removeItem(STORE_KEY);
    location.reload();
  });

  const weeks = Array.from(new Set(cards.map(c=>c.week).filter(Boolean))).sort();
  const days  = Array.from(new Set(cards.map(c=>c.day).filter(Boolean))).sort();

  qs("#week").innerHTML = `<option value="">All weeks</option>` + weeks.map(w=>`<option value="${escapeAttr(w)}">${escapeHtml(w)}</option>`).join("");
  qs("#day").innerHTML  = `<option value="">All days</option>` + days.map(d=>`<option value="${escapeAttr(d)}">${escapeHtml(d)}</option>`).join("");

  renderCards();
}

function escapeHtml(s){
  return (s||"").replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;");
}
function escapeAttr(s){ return escapeHtml(s).replaceAll("'","&#39;"); }
