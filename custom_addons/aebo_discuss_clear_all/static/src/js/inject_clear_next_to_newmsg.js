/** @odoo-module **/
// Final minimal solution: no imports, no template extend.
// Robustly place a "Clear" button *right next to* the "New Message" link.
// Works across minor DOM variations; zero boot-time risk.

(function () {
  const BTN_ID = "AEBO_MM_CLEAR_BTN";
  const SELECTORS = {
    menu: ".o_MessagingMenu",
    header: ".o_MessagingMenu_header",
    actions: ".o_MessagingMenu_headerActions",
  };

  function findNewMessageNode(root) {
    // Prefer explicit "New Message" link if present
    const candidates = Array.from(root.querySelectorAll("a,button,span,div"))
      .filter((el) => {
        const t = (el.textContent || "").trim().toLowerCase();
        return t === "new message" || t === "new messages" || t === "new";
      });
    if (candidates.length) return candidates[0];

    // Fallback: search icon + sibling text
    const possible = root.querySelector('[title*="New Message" i]');
    if (possible) return possible;

    // Last fallback: use actions container itself
    return root.querySelector(SELECTORS.actions) || root;
  }

  async function callClearRoute(btn) {
    const csrf =
      (window.odoo && window.odoo.csrf_token) ||
      (document.querySelector('meta[name="csrf_token"]') || {}).content ||
      "";
    btn.disabled = true;
    const old = btn.textContent;
    btn.textContent = "Clearing…";
    try {
      const r = await fetch("/aebo_discuss/clear_all", {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrf,
        },
        body: JSON.stringify({}),
      });
      await r.json(); // ignore payload; controller returns {"status":"ok"}
      btn.textContent = "Cleared ✓";
      setTimeout(() => { btn.textContent = old; btn.disabled = false; }, 800);
    } catch (e) {
      console.error("[AEBO] clear_all failed", e);
      btn.textContent = "Retry";
      setTimeout(() => { btn.textContent = old; btn.disabled = false; }, 1200);
    }
  }

  function inject() {
    const menu = document.querySelector(SELECTORS.menu);
    if (!menu) return;
    const header = menu.querySelector(SELECTORS.header) || menu;
    const actions = header.querySelector(SELECTORS.actions) || header;
    // Placement anchor
    const anchor = findNewMessageNode(actions);
    if (!anchor) return;

    // Already added?
    if (actions.querySelector("#" + BTN_ID)) return;

    const btn = document.createElement("button");
    btn.id = BTN_ID;
    btn.className = "btn btn-link btn-sm";
    btn.textContent = "Clear";
    btn.style.marginLeft = "8px";
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      callClearRoute(btn);
    });

    // Put exactly after the New Message anchor if found
    if (anchor && anchor.parentNode) {
      anchor.insertAdjacentElement("afterend", btn);
    } else {
      actions.appendChild(btn);
    }
  }

  // Observe UI re-renders; inject stays idempotent
  const obs = new MutationObserver(() => inject());
  function start() {
    try {
      obs.observe(document.body, { childList: true, subtree: true });
    } catch (e) {
      console.warn("[AEBO] MutationObserver failed", e);
    }
    // Immediate attempt
    inject();
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();