/** @odoo-module **/
(function () {
  const SELECTOR = '#aebo-mm-clear-btn, .o-aebo-clear-all';

  async function callClear() {
    const csrf = (window.odoo && window.odoo.csrf_token) ||
                 (document.querySelector('meta[name="csrf_token"]') || {}).content || "";
    const res = await fetch("/aebo_messaging_menu/clear_all", {
      method: "POST",
      credentials: "same-origin",
      headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
      body: "{}",
    });
    try { return await res.json(); } catch (_) { return {status:"ok"}; }
  }

  function refreshMessagingMenu() {
    const tgl = document.querySelector(".o-mail-SystrayItem button, .o_MessagingMenu_toggler, .o-mail-SystrayItem__toggle");
    if (tgl) { try { tgl.click(); setTimeout(() => tgl.click(), 180); return; } catch(e){} }
    setTimeout(() => window.location.reload(), 300);
  }

  document.addEventListener("click", async (ev) => {
    const btn = ev.target.closest(SELECTOR);
    if (!btn) return;
    ev.preventDefault();
    ev.stopPropagation();
    const old = btn.textContent;
    btn.disabled = true;
    btn.textContent = "Clearing…";
    try {
      const r = await callClear();
      const parts = [];
      if (r?.notifications) parts.push(`N:${r.notifications.before}→${r.notifications.after}`);
      if (typeof r?.channels_touched === "number") parts.push(`C:${r.channels_touched}`);
      btn.textContent = "Cleared ✓" + (parts.length ? ` (${parts.join(", ")})` : "");
      refreshMessagingMenu();
    } catch (e) {
      console.error("[Aebo MarkAll v6.1] failed", e);
      btn.textContent = "Retry";
    } finally {
      setTimeout(() => { btn.textContent = old; btn.disabled = false; }, 1000);
    }
  }, true);
})();