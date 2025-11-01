/** @odoo-module **/

import { Component, useState, xml } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class StickyNoteFormModal extends Component {
    static props = {
        close: Function,
    };
    static components = { Dialog };

    setup() {
        this.state = useState({
            title: "",
            description: "",
            color: "#fffc8a",
        });
    }

    confirm() {
        if (!this.state.title.trim()) {
            this.env.services.notification.add("Title is required!", { type: "warning" });
            return;
        }
        this.props({
            title: this.state.title,
            description: this.state.description,
            color: this.state.color,
        });
    }

    cancel() {
        this.props.close(false);
    }

    static template = xml`
        <Dialog title="'New Sticky Note'" size="'md'" modalRef="modalRef">
            <div class="mb-3">
                <label class="form-label">Title</label>
                <input type="text" class="form-control" t-model="state.title" placeholder="Note title"/>
            </div>
            <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea class="form-control" t-model="state.description" placeholder="Write your note here"></textarea>
            </div>
            <div class="mb-3">
                <label class="form-label">Color</label>
                <input type="color" class="form-control-color" t-model="state.color"/>
            </div>
            <t t-set-slot="footer">
                <button class="btn btn-primary" t-on-click="confirm">Save</button>
                <button class="btn btn-secondary" t-on-click="cancel">Cancel</button>
            </t>
        </Dialog>
    `;
}
