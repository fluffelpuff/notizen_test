function deleteMenuItemById(id) {
    const menu       = document.getElementById('menu');
    const emptyState = document.getElementById('empty-state');
    const detailView = document.getElementById('detail-view');
    const detailText = document.getElementById('detail-text');
    const header     = document.getElementById('detail-header');

    if (!menu || !id) return false;

    const safeId = (window.CSS && CSS.escape) ? CSS.escape(id) : id;
    const item = menu.querySelector(`.list-group-item[data-id="${safeId}"]`);
    if (!item) return false;

    const wasActive = item.classList.contains('active');
    item.remove();

    if (wasActive) {
        menu.querySelectorAll('.active').forEach(a => a.classList.remove('active'));
        if (detailText) detailText.textContent = '';
        if (detailView) detailView.classList.add('d-none');
        if (emptyState) emptyState.classList.remove('d-none');
        if (header) header.classList.add('d-none');
    }

    return true;
}

function deleteModal(id) {
    const modalEl = document.getElementById('deletenotice-modal');
    const confirmButton = document.getElementById("deletenotice-confirm");
    const modal = new bootstrap.Modal(modalEl);

    confirmButton.addEventListener("click", async() => {
        fetch('/delete_notice', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ "id":id })
        })
        .then(r => r.json())
        .then(() => {
            deleteMenuItemById(id);
            confirmButton.addEventListener("click", null);
            modal.hide()
        })
        .catch(console.error);
    });

    modal.show();
}

function updateNotice(id, newTitle, newText) {
    const menu = document.getElementById('menu');
    if (!menu || !id) return false;

    console.log(id, newTitle, newText)

    let item = null;
    for (const el of menu.getElementsByClassName('list-group-item')) {
        if ((el.dataset.id || '').trim() === String(id).trim()) { item = el; break; }
    }
    if (!item) return false;

    if (typeof newTitle === 'string') {
        item.dataset.title = newTitle;
        const h5 = item.querySelector('h5');
        if (h5) h5.textContent = newTitle;
    }
    if (typeof newText === 'string') {
        item.dataset.text = newText;
    }

    if (item.classList.contains('active')) {
        const titleEl = document.getElementById('detail-title');
        const textEl  = document.getElementById('detail-text');
        if (titleEl && typeof newTitle === 'string') titleEl.textContent = newTitle;
        if (textEl  && typeof newText  === 'string') textEl.textContent  = newText;
    }

    return true;
}

function editModal(id) {
    const modalEl = document.getElementById('editnotice-modal');
    const submitButton = document.getElementById('editnotice-submit');
    const noticeTitel = document.getElementById('editnotice-title');
    const noticeText  = document.getElementById('editnotice-text');
    const modal = bootstrap.Modal.getOrCreateInstance(modalEl);

    const sel = document.querySelector(`#menu .list-group-item[data-id="${(window.CSS&&CSS.escape)?CSS.escape(id):id}"]`);
    const currentTitle = sel?.dataset.title ?? '';
    const currentText  = sel?.dataset.text  ?? '';
    noticeTitel.value = currentTitle;
    noticeText.value  = currentText;

    const onSubmit = async () => {
        const newTitle = noticeTitel.value.trim();
        const newText  = noticeText.value.trim();

        await fetch('/edit_notice', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ id, title: newTitle, text: newText })
        }).catch(console.error);

        updateNotice(id, newTitle, newText);
        modal.hide();
    };

    submitButton.addEventListener('click', onSubmit, { once: true });
    modal.show();
}

function newModal() {
    const modalEl = document.getElementById('newnotice-modal');
    const modal = new bootstrap.Modal(modalEl);
    modal.show();
}

function addMenuItem(id, title, text, timestamp) {
  const menu = document.getElementById('menu');
  if (!menu) return;

  const placeholder = menu.querySelector('li');
  if (placeholder) placeholder.remove();

  const a = document.createElement('a');
  a.href = '#';
  a.className = 'list-group-item list-group-item-action';
  a.setAttribute('aria-current', 'true');

  a.dataset.id = id || '';
  a.dataset.title = title || '';
  a.dataset.text = text || '';
  a.dataset.time = timestamp || '';

  a.innerHTML = `
    <div class="d-flex w-100 justify-content-between">
      <h5 class="mb-1">${title || ''}</h5>
      <small>${timestamp || ''}</small>
    </div>
  `;

  menu.prepend(a);
}

document.addEventListener('DOMContentLoaded', () => {
    const menu       = document.getElementById('menu');
    const header     = document.getElementById('detail-header');
    const emptyState = document.getElementById('empty-state');
    const detailView = document.getElementById('detail-view');
    const titleEl    = document.getElementById('detail-title');
    const timeEl     = document.getElementById('detail-time');
    const textEl     = document.getElementById('detail-text');
    const newnoticeText = document.getElementById('newnotice-text');
    const newnoticeTitel = document.getElementById('newnotice-title');
    const newnoticeSubmit = document.getElementById('newnotice-submit');
    const newNoticeModalEl = document.getElementById('newnotice-modal');
    const editNoticeButton = document.getElementById('edit-notice-button');
    const deleteNoticeButton = document.getElementById('del-notice-button');
    const newNoticeModal = new bootstrap.Modal(newNoticeModalEl);

    menu.addEventListener('click', (e) => {
        const el = e.target.closest('.list-group-item');
        if (!el) return;
        e.preventDefault();

        menu.querySelectorAll('.active').forEach(a => a.classList.remove('active'));
        el.classList.add('active');

        const id    = el.dataset.id   || '';
        const title = el.dataset.title || el.querySelector('h5')?.textContent.trim()   || '';
        const time  = el.dataset.time  || el.querySelector('small')?.textContent.trim()|| '';
        const text  = el.dataset.text  || el.querySelector('p')?.textContent.trim()    || '';

        titleEl.textContent = title;
        timeEl.textContent  = time;
        textEl.textContent  = text;

        deleteNoticeButton.onclick = () => deleteModal(id);
        editNoticeButton.onclick = () => editModal(id);

        header.classList.remove('d-none');
        emptyState.classList.add('d-none');
        detailView.classList.remove('d-none');

        console.log('Ausgewählt:', id);
    });

    newnoticeSubmit.addEventListener('click', async (e) => {
        e.preventDefault();

        const title = (newnoticeTitel.value || '').trim();
        const text  = (newnoticeText.value  || '').trim();
        if (!title || !text) return;

        try {
            const response = await fetch('/add_notice', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title, text })
            });

            if (!response.ok) {
                console.error('Fehlerstatus:', response.status);
                return;
            }

            const data = await response.json();
            const noticeid  = data?.noticeid;
            const timestamp = data?.timestamp ?? '';

            if (!noticeid) {
                console.error('Kein noticeid in Response:', data);
                return;
            }

            addMenuItem(noticeid, title, text, timestamp);

            newnoticeTitel.value = '';
            newnoticeText.value  = '';
            newNoticeModal.hide();
        } catch (err) {
            console.error('Request fehlgeschlagen:', err);
        }
    });
});
