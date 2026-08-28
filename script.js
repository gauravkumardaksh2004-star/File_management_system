const fs = {}; // virtual filesystem: name -> content string
let opCount = 0;
let updateMode = 'rename';

function renderFiles(){
  const list = document.getElementById('fileList');
  const names = Object.keys(fs);
  document.getElementById('fileCount').textContent = names.length;
  if(names.length === 0){
    list.innerHTML = '<div style="font-family:var(--mono);font-size:11.5px;color:var(--text-dim);padding:8px 2px;">No files yet — create one to get started.</div>';
    return;
  }
  list.innerHTML = names.map(n => `
    <div class="file-row" onclick="quickSelect('${n.replace(/'/g,"\\'")}')">
      <span class="dot"></span>
      <span class="fname">${escapeHtml(n)}</span>
      <span class="fsize">${fs[n].length}B</span>
    </div>
  `).join('');
}

function escapeHtml(s){
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function quickSelect(name){
  const activeTab = document.querySelector('.tab.active').dataset.tab;
  const map = {create:'create-name', read:'read-name', update:'update-name', delete:'delete-name'};
  const input = document.getElementById(map[activeTab]);
  if(input) input.value = name;
}

function log(kind, text){
  const body = document.getElementById('termBody');
  const line = document.createElement('div');
  line.className = 'term-line';
  if(kind === 'cmd'){
    line.innerHTML = `<span class="term-prompt">user@fileforge</span><span class="term-path">:~$</span> ${escapeHtml(text)}`;
  } else if(kind === 'ok'){
    line.innerHTML = `<span class="term-ok">✓ ${escapeHtml(text)}</span>`;
  } else if(kind === 'err'){
    line.innerHTML = `<span class="term-err">✗ ${escapeHtml(text)}</span>`;
  } else {
    line.innerHTML = `<span class="term-info">${escapeHtml(text)}</span>`;
  }
  body.appendChild(line);
  body.scrollTop = body.scrollHeight;
  opCount++;
  document.getElementById('opCount').textContent = opCount;
}

// Tabs
document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tabpanel').forEach(p => p.style.display = 'none');
    tab.classList.add('active');
    document.querySelector(`.tabpanel[data-panel="${tab.dataset.tab}"]`).style.display = 'block';
  });
});

function setUpdateMode(mode){
  updateMode = mode;
  document.querySelectorAll('.mode-chip').forEach(c => c.classList.toggle('active', c.dataset.mode === mode));
  document.getElementById('update-newname-field').style.display = mode === 'rename' ? 'block' : 'none';
  document.getElementById('update-data-field').style.display = mode === 'rename' ? 'none' : 'block';
}

function showOut(id, text){
  const el = document.getElementById(id);
  el.textContent = text;
  el.classList.add('show');
}

// CREATE
function opCreate(){
  const name = document.getElementById('create-name').value.trim();
  if(!name){ showOut('create-out','Enter a file name first.'); return; }
  log('cmd', `create ${name}`);
  if(fs.hasOwnProperty(name)){
    log('err', `file ${name} already exists`);
    showOut('create-out', `File "${name}" already exists.`);
  } else {
    fs[name] = '';
    log('ok', `file ${name} created`);
    showOut('create-out', `Your file "${name}" is created.`);
    renderFiles();
  }
}

// READ
function opRead(){
  const name = document.getElementById('read-name').value.trim();
  if(!name){ showOut('read-out','Enter a file name first.'); return; }
  log('cmd', `read ${name}`);
  if(fs.hasOwnProperty(name)){
    log('ok', `read ${fs[name].length} bytes from ${name}`);
    showOut('read-out', fs[name].length ? fs[name] : '(file is empty)');
  } else {
    log('err', `file not found: ${name}`);
    showOut('read-out', 'File not found.');
  }
}

// UPDATE
function opUpdate(){
  const name = document.getElementById('update-name').value.trim();
  if(!name){ showOut('update-out','Enter a file name first.'); return; }

  if(updateMode === 'rename'){
    const newname = document.getElementById('update-newname').value.trim();
    log('cmd', `rename ${name} -> ${newname}`);
    if(!fs.hasOwnProperty(name)){
      log('err', `file not found: ${name}`);
      showOut('update-out', 'File not found.');
      return;
    }
    if(fs.hasOwnProperty(newname)){
      log('err', `${newname} already exists`);
      showOut('update-out', 'A file with the new name already exists.');
      return;
    }
    fs[newname] = fs[name];
    delete fs[name];
    log('ok', `renamed to ${newname}`);
    showOut('update-out', 'File name successfully changed.');
    renderFiles();

  } else if(updateMode === 'append'){
    const data = document.getElementById('update-data').value;
    log('cmd', `append -> ${name}`);
    if(!fs.hasOwnProperty(name)){
      log('err', `file not found: ${name}`);
      showOut('update-out', 'File not found.');
      return;
    }
    fs[name] += '\n' + data;
    log('ok', `appended ${data.length} chars to ${name}`);
    showOut('update-out', `Data added to "${name}".`);
    renderFiles();

  } else { // overwrite / create
    const data = document.getElementById('update-data').value;
    log('cmd', `overwrite ${name}`);
    fs[name] = '\n' + data;
    log('ok', `${name} written (${fs[name].length} bytes)`);
    showOut('update-out', `File "${name}" updated.`);
    renderFiles();
  }
}

// DELETE
function opDelete(){
  const name = document.getElementById('delete-name').value.trim();
  if(!name){ showOut('delete-out','Enter a file name first.'); return; }
  log('cmd', `delete ${name}`);
  if(fs.hasOwnProperty(name)){
    delete fs[name];
    log('ok', `deleted ${name}`);
    showOut('delete-out', 'File successfully deleted.');
    renderFiles();
  } else {
    log('err', `file not found: ${name}`);
    showOut('delete-out', 'File not found.');
  }
}

renderFiles();
