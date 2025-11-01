
odoo.define("aebo_force_logout_on_close.AutoLogout", [], function (require) {
    "use strict";

    const KEY = "aebo_open_tabs";
    const TAB_ID = (Math.random().toString(36).slice(2) + Date.now().toString(36));

    function getList() {
        try { return JSON.parse(localStorage.getItem(KEY) || "[]"); }
        catch (e) { return []; }
    }
    function setList(arr) {
        try { localStorage.setItem(KEY, JSON.stringify(arr)); } catch (e) {}
    }
    function addTab() {
        const arr = getList();
        if (!arr.includes(TAB_ID)) {
            arr.push(TAB_ID);
            setList(arr);
        }
    }
    function removeTab() {
        const arr = getList().filter((x) => x !== TAB_ID);
        setList(arr);
        return arr.length;
    }

    addTab();

    function onClose() {
        const remaining = removeTab();
        if (remaining === 0) {
            try {
                if (navigator.sendBeacon) {
                    const blob = new Blob([JSON.stringify({})], { type: "application/json" });
                    navigator.sendBeacon("/aebo_force_logout/logout", blob);
                } else {
                    const xhr = new XMLHttpRequest();
                    xhr.open("POST", "/aebo_force_logout/logout", false);
                    xhr.setRequestHeader("Content-Type", "application/json");
                    xhr.send("{}");
                }
            } catch (e) {}
        }
    }

    window.addEventListener("pagehide", onClose, { capture: true });
    window.addEventListener("beforeunload", onClose, { capture: true });
    document.addEventListener("visibilitychange", function () {
        if (document.visibilityState === "hidden") onClose();
    }, { capture: true });
});
