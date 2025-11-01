/* @odoo-module */

import { Component, useState } from "@odoo/owl";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { useDropdownState } from "@web/core/dropdown/dropdown_hooks";
import { deserializeDateTime } from "@web/core/l10n/dates";
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { isIosApp } from "@web/core/browser/feature_detection";
const { DateTime } = luxon;

export class ActivityMenu extends Component {
    static components = { Dropdown, DropdownItem };
    static props = [];
    static template = "hr_attendance.attendance_menu";

    setup() {
        this.ui = useState(useService("ui"));
        this.employee = false;

        // ✅ labels added here
        this.state = useState({
            checkedIn: false,
            isDisplayed: false,
            breakInLabel: false,
            breakOutLabel: false,
            canBreakIn: false,
            canBreakOut: false,
            canCheckOut: false,
        });

        this.date_formatter = registry.category("formatters").get("float_time");
        this.dropdown = useDropdownState();
        this.searchReadEmployee();
    }

    async searchReadEmployee() {
        const result = await rpc("/hr_attendance/attendance_user_data");
        this.employee = result || {};
        if (this.employee.id) {
            this.hoursToday = this.date_formatter(this.employee.hours_today);
            this.hoursPreviouslyToday = this.date_formatter(this.employee.hours_previously_today);
            this.lastAttendanceWorkedHours = this.date_formatter(this.employee.last_attendance_worked_hours);
            this.lastCheckIn = deserializeDateTime(this.employee.last_check_in).toLocaleString(DateTime.TIME_SIMPLE);

            this.state.checkedIn = this.employee.attendance_state === "checked_in";
            this.isFirstAttendance = this.employee.hours_previously_today === 0;
            this.state.isDisplayed = this.employee.display_systray;

            // ✅ get labels from server (fallback false)
            this.state.breakInLabel = this.employee.break_in_label || false;
            this.state.breakOutLabel = this.employee.break_out_label || false;
            this.state.canBreakIn = !!this.employee.can_break_in;
            this.state.canBreakOut = !!this.employee.can_break_out;
            this.state.canCheckOut = !!this.employee.can_check_out;
        } else {
            this.state.isDisplayed = false;
        }
    }

    async signInOut() {
        this.dropdown.close();
        const doRpc = async (latitude, longitude) => {
            await rpc("/hr_attendance/systray_check_in_out", latitude != null ? { latitude, longitude } : {});
            await this.searchReadEmployee(); // refresh all, includes labels if server sets them
        };
        if (!isIosApp()) {
            navigator.geolocation.getCurrentPosition(
                ({ coords: { latitude, longitude } }) => doRpc(latitude, longitude),
                () => doRpc(),
                { enableHighAccuracy: true }
            );
        } else {
            await doRpc();
        }
    }

    async breakIn() {
        // ✅ hard UI guard
        if (!this.state.checkedIn || !this.state.canBreakIn) return;

        // temporary lock to avoid double-clicks until server answers
        this.state.canBreakIn = false;

        const doRpc = async (latitude, longitude) => {
            const res = await rpc("/hr_attendance/systray_break_in", latitude != null ? { latitude, longitude } : {});
            if (res) {
                this.state.breakInLabel  = res.break_in_label  ?? this.state.breakInLabel;
                this.state.breakOutLabel = res.break_out_label ?? this.state.breakOutLabel;
                // ✅ also refresh flags after break-in
                this.state.canBreakIn    = !!res.can_break_in;
                this.state.canBreakOut   = !!res.can_break_out;
                this.state.canCheckOut   = !!res.can_check_out;
                 this.state.canCheckOut   = !!res.can_check_out; 
                if (typeof res.attendance_state === "string") {
                    this.state.checkedIn = res.attendance_state === "checked_in";
                }
            }
            await this.searchReadEmployee();
        };

        if (!isIosApp()) {
            navigator.geolocation.getCurrentPosition(
                ({ coords: { latitude, longitude } }) => doRpc(latitude, longitude),
                () => doRpc(),
                { enableHighAccuracy: true }
            );
        } else {
            await doRpc();
        }
    }

    async breakOut() {
        // ✅ hard UI guard
        if (!this.state.checkedIn || !this.state.canBreakOut) return;

        // temporary lock during RPC
        this.state.canBreakOut = false;

        const doRpc = async (latitude, longitude) => {
            const res = await rpc("/hr_attendance/systray_break_out", latitude != null ? { latitude, longitude } : {});
            if (res) {
                this.state.breakInLabel  = res.break_in_label  ?? this.state.breakInLabel;
                this.state.breakOutLabel = res.break_out_label ?? this.state.breakOutLabel;
                this.state.canBreakIn    = !!res.can_break_in;
                this.state.canBreakOut   = !!res.can_break_out;
                this.state.canCheckOut   = !!res.can_check_out;
                if (typeof res.attendance_state === "string") {
                    this.state.checkedIn = res.attendance_state === "checked_in";
                }
            }
            await this.searchReadEmployee();
        };

        if (!isIosApp()) {
            navigator.geolocation.getCurrentPosition(
                ({ coords: { latitude, longitude } }) => doRpc(latitude, longitude),
                () => doRpc(),
                { enableHighAccuracy: true }
            );
        } else {
            await doRpc();
        }
    }
}


export const systrayAttendance = { Component: ActivityMenu };
registry.category("systray").add("hr_attendance.attendance_menu", systrayAttendance, { sequence: 101 });