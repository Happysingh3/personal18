
/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class AeboBreakSystray extends Component {
    setup() {
        this.rpc = useService("rpc");
        this.user = useService("user");
        this.state = { breakOn: false, checkedIn: false };
        this._refresh();
    }
    async _refresh() {
        try {
            const data = await this.rpc("/hr_attendance/aebo_break_state", {});
            this.state.checkedIn = !!data.checked_in;
            this.state.breakOn = data.current_break_state === "on";
            this.render();
        } catch {}
    }
    async breakIn(ev) {
        ev.preventDefault();
        await this.rpc("/hr_attendance/break_in", { mode: "systray" });
        await this._refresh();
    }
    async breakOut(ev) {
        ev.preventDefault();
        await this.rpc("/hr_attendance/break_out", { mode: "systray" });
        await this._refresh();
    }
}
AeboBreakSystray.template = "aebo_hr_breaks_safe.SystrayBreaks";
registry.category("systray").add("aebo_hr_breaks_safe.systray", { Component: AeboBreakSystray }, { sequence: 16 });
