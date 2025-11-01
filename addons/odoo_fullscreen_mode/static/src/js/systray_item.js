/* @odoo-module */

import { Component, useState, useExternalListener } from "@odoo/owl";
import { browser } from "@web/core/browser/browser";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class Fullscreen extends Component {
    static props = [];
    static template = "odoo_fullscreen_mode.Fullscreen";

    setup() {
        this.state = useState({isFullscreen: false});
        useExternalListener(browser, "fullscreenchange", this.onFullScreenChange);
    }

    async toggleFullscreen() {
        if (!this.state.isFullscreen) {
            const el = document.documentElement;
            try {
                if (el.requestFullscreen) {
                    await el.requestFullscreen();
                } else if (el.mozRequestFullScreen) {
                    await el.mozRequestFullScreen();
                } else if (el.webkitRequestFullscreen) {
                    await el.webkitRequestFullscreen();
                }
            } catch {
                console.error("The Fullscreen mode was denied by the browser");
            }
        } else {
            if (document.exitFullscreen) {
                await document.exitFullscreen();
            } else if (document.mozCancelFullScreen) {
                await document.mozCancelFullScreen();
            } else if (document.webkitCancelFullScreen) {
                await document.webkitCancelFullScreen();
            }
        }
    }

    onFullScreenChange() {
        this.state.isFullscreen = Boolean(
            document.fullscreenElement || document.mozFullScreenElement || document.webkitFullscreenElement || document.msFullscreenElement
        );
    }
}

registry.category("systray").add("odoo_fullscreen_mode.Fullscreen", { Component: Fullscreen }, { sequence: 100 });
