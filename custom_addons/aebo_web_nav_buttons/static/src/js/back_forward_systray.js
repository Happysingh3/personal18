/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, onMounted, onWillUnmount } from "@odoo/owl";

export class AeboNavButtons extends Component {
    setup() {
        this._keydown = (ev) => {
            // Keyboard shortcuts like a browser
            if (ev.altKey && ev.key === "ArrowLeft") {
                ev.preventDefault();
                this.goBack();
            } else if (ev.altKey && ev.key === "ArrowRight") {
                ev.preventDefault();
                this.goForward();
            }
        };
        onMounted(() => document.addEventListener("keydown", this._keydown));
        onWillUnmount(() => document.removeEventListener("keydown", this._keydown));
    }

    goBack() {
        // Will behave like browser back inside Odoo SPA
        window.history.back();
    }

    goForward() {
        window.history.forward();
    }
}
AeboNavButtons.template = "aebo.NavButtons";

// Add to topbar systray
registry.category("systray").add("aebo_nav_buttons", { Component: AeboNavButtons }, { sequence: 1 });