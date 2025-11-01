/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { onMounted} from "@odoo/owl";

function getColorHex(color) {
    return {
        yellow: "#fff9c4",
        pink: "#f8bbd0",
        green: "#c8e6c9",
        blue: "#bbdefb",
    }[color] || "#fff";
}
export class StickyNoteSystray extends Component {
    static template = "note_sticky.StickyNoteSystray";
        static props = {};  // ✅ Add this line to declare no props
    async setup() {
        this.action = useService("action");
        this.notes = useState({
            showPopup: false,
            title: "",
            content: "",
            color: "",
            text_color:"",
        });

        this.notes.selectedUsers = [];
        this.notes.allUsers = [];

        onMounted(() => this.loadUsers());
    }


    toggleUser(userId) {
      const index = this.notes.selectedUsers.indexOf(userId);
      if (index > -1) {
        this.notes.selectedUsers.splice(index, 1);
      } else {
        this.notes.selectedUsers.push(userId);
      }
    }

    async loadUsers() {
        this.notes.allUsers = await this.env.services.orm.searchRead("res.users", [], ["id", "name"]);
    }


    openPopup() {
        this.notes.showPopup = true;
    }

    closePopup() {
        this.notes.showPopup = false;
        this.notes.title = "";
        this.notes.content = "";
        this.notes.color = '';
        this.notes.text_color = '';
    }

async submitNote(ev) {
    ev.preventDefault();
    const { title, content, color, text_color } = this.notes;
    const { resModel, resId } = this.action.currentController.props;

    if (!resModel || !resId) {
        alert("Open a form view first to attach the sticky note.");
        return;
    }

    // Save to backend
    await this.env.services.orm.create("note.sticky", [{
        res_model: resModel,
        res_id: resId,
        name: title,
        content: content,
        color: color,
        text_color:text_color,
        user_ids: [[6, 0, this.notes.selectedUsers]],

    }]);

    this.closePopup();

    // Inject into left sidebar
//    const sidebar = document.body.querySelector(".o_sticky_note_sidebar");
//    if (sidebar) {
//        const card = document.createElement("div");
//        card.className = "sticky-note-card";
//        card.style =
//            background-color: ${color};
//            border-radius: 12px;
//            padding: 12px 16px;
//            margin-bottom: 10px;
//            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
//            font-family: sans-serif;
//        ;
//        card.innerHTML =
//            <div style="display: flex; justify-content: space-between; align-items: center;">
//                <h5 contenteditable="true" style="margin: 0; font-size: 16px;">${title}</h5>
//                <div>
//                    <button class="btn btn-sm btn-outline-primary btn-edit" title="Edit"><i class="fa fa-edit"></i></button>
//                    <button class="btn btn-sm btn-outline-danger">🗑️</button>
//                </div>
//            </div>
//            <p contenteditable="true" style="margin: 6px 0 0;">${content}</p>
//        ;
//        sidebar.prepend(card);
//    } else {
//        console.warn("Sidebar not found to inject note");
//    }
    location.reload()
}
}

//StickyNoteSystray.template = "note_sticky.StickyNoteSystray";

registry.category("systray").add("StickyNoteSystray", { Component: StickyNoteSystray });