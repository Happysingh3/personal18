odoo.define("aebo_discuss_purge_all.DiscussPurgeDelegate", [], function (require) {
    "use strict";
    if (window.__aeboPurgeBound) return;
    window.__aeboPurgeBound = true;

    document.addEventListener("click", async (ev) => {
        const btn = ev.target.closest && ev.target.closest(".o_aebo_PurgeChat");
        if (!btn) return;
        const idStr = btn.getAttribute("data-thread-id");
        const channelId = idStr ? parseInt(idStr) : NaN;
        if (!channelId) return;

        if (!window.confirm("Delete this chat for everyone?\nAll messages and attachments will be permanently removed.")) return;

        try {
            const res = await fetch("/aebo_discuss/purge", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ channel_id: channelId }),
                credentials: "same-origin",
            });
            const data = await res.json();
            if (!res.ok || !data || !data.ok) {
                throw new Error((data && (data.error || data.message)) || "Server error");
            }
            const s = data.stats || {};
            alert(`Deleted: ${ (s.messages_deleted_per_channel||[]).reduce((a,b)=>a+b,0) } messages, ${s.attachments_deleted||0} attachments.`);
            // reload Discuss
            window.location.hash = "#action=mail.action_discuss";
            window.location.reload();
        } catch (e) {
            alert("Failed to delete chat: " + (e && e.message ? e.message : String(e)));
        }
    }, true);
});