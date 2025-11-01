/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { FormRenderer } from "@web/views/form/form_renderer";
import {onMounted, useEffect, useState} from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";

// Simple confirm dialog utility
async function showConfirmDialog(dialogService, { title, body, confirmLabel, cancelLabel }) {
    return new Promise((resolve) => {
        dialogService.add(Dialog, {
            title: title || "Confirm",
            body: body || "Are you sure?",
            buttons: [
                {
                    label: confirmLabel || "Yes",
                    class: "btn-primary",
                    onClick: () => resolve(true),
                },
                {
                    label: cancelLabel || "Cancel",
                    onClick: () => resolve(false),
                },
            ],
        });
    });
}



patch(FormRenderer.prototype, {
    setup() {
        super.setup?.();
            this.notes = useState({
            showPopup: false,
            title: "",
            content: "",
            color: "",
            text_color:"",
        });
        this.dialog = useService("dialog");

        this.notes.selectedUsers = [];
        this.notes.allUsers = [];
        onMounted(async () => {
            await this.loadUsers();
            await this._injectStickyNotesSidebar();
        });


        useEffect(
            () => {
                this._removeStickyNotes();
                this._injectStickyNotesSidebar();
            },
            () => [this.env.model.config.resId]
        );


        },


    toggleUser(userId) {
        const index = this.notes.selectedUsers.indexOf(userId);
        if (index > -1) {
            this.notes.selectedUsers.splice(index, 1);
        } else {
            this.notes.selectedUsers.push(userId);
        }
    },

    async loadUsers() {
        var all_users = await this.env.services.orm.searchRead("res.users", [], ["id", "name"]);
        this.notes.allUsers = all_users
    },

    _removeStickyNotes() {
        const oldSidebar = document.querySelector(".o_sticky_note_sidebar");
        if (oldSidebar) {
            oldSidebar.remove();
        }
        document.querySelector(".o_form_sheet_bg")?.classList.remove("has-sticky-notes");
    },
    async _injectStickyNotesSidebar() {
        const resModel = this.env.model.config.resModel;
        const resId = this.env.model.config.resId;
        const oldSidebar = document.querySelector(".o_sticky_note_sidebar");
        if (oldSidebar) {
            oldSidebar.remove();
        }
        const notes = await this.env.services.orm.searchRead("note.sticky", [
            ["res_model", "=", resModel],
            ["res_id", "=", resId],
            '|',
            ["create_uid", "=",this.env.model.config.context.uid],
                ["user_ids", "in", [this.env.model.config.context.uid]], // 🔒 Only visible to current user

        ], ["id", "name", "content", "color",'text_color']);
        if (notes.length > 0) {
            document.querySelector(".o_form_sheet_bg")?.classList.add("has-sticky-notes");

            const container = document.querySelector(".o_form_sheet_bg");;
//            if (!container || container.querySelector(".o_sticky_note_sidebar")) return;

            const sidebar = document.createElement("div");
            sidebar.className = "o_sticky_note_sidebar";

            notes.forEach(note => {
                const card = document.createElement("div");
                card.className = "sticky-note-card";
                card.style.backgroundColor = note.color;
                card.style.color = note.text_color;

                card.innerHTML =
                    `<div class="sticky-note-header">
                        <h4 class="sticky-note-title" style="color: ${note.text_color || '#000'}">${note.name}</h4>
                        <div class="sticky-note-buttons">
                            <button class="btn btn-sm btn-outline-primary btn-edit" data-id="${note.id}" title="Edit"><i class="fa fa-edit"></i></button>
                            <button class="btn btn-sm btn-outline-danger btn-delete" data-id="${note.id}" title="Delete"><i class="fa fa-trash"></i></button>
                        </div>
                    </div>
                    <p class="sticky-note-content" style="color: ${note.text_color || '#000'}">${note.content}</p>`
                ;
                card.querySelector(".btn-delete").addEventListener("click", async (e) => {
                    const noteId = parseInt(e.currentTarget.dataset.id);
                
                    const modal = document.createElement("div");
                    modal.className = "modal d-block";
                    modal.innerHTML = `
                        <div class="modal-dialog">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title text-danger">Delete Confirmation</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                                </div>
                                <div class="modal-body">
                                    <p>Are you sure you want to delete this sticky note?</p>
                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-danger btn-confirm-delete">Delete</button>
                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                                </div>
                            </div>
                        </div>`;

                    document.body.prepend(modal);
                    
                    // Attach event listeners
                    modal.querySelector(".btn-confirm-delete").addEventListener("click", async () => {
                        await this.env.services.orm.unlink("note.sticky", [noteId]);
                        card.remove();
                        modal.remove();
                    });
                    
                    modal.querySelector(".btn-close").addEventListener("click", () => modal.remove());
                    modal.querySelector(".btn-secondary").addEventListener("click", () => modal.remove());

                });



                card.querySelector(".btn-edit").addEventListener("click", async (e) => {
    const noteId = parseInt(e.currentTarget.dataset.id);
    const result = await this.env.services.orm.read("note.sticky", [noteId], ["name", "content", "color", "text_color", "user_ids"]);
    const note = result[0];

    // Set selected users for this note
    this.notes.selectedUsers.splice(0, this.notes.selectedUsers.length, ...note.user_ids);

    // Build user list HTML manually
    let userOptions = "";
    this.notes.allUsers.forEach(user => {
        const isChecked = this.notes.selectedUsers.includes(user.id) ? "checked" : "";
        userOptions += `
            <li>
              <label class="dropdown-item d-flex align-items-center gap-2">
                <input type="checkbox" class="form-check-input user-checkbox" data-user-id="${user.id}" ${isChecked} />
                ${user.name}
              </label>
            </li>`;
    });

    const modal = document.createElement("div");
    modal.className = "modal d-block";
    modal.innerHTML = `
        <div class="modal-dialog">
            <form class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Edit Sticky Note</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <input class="form-control mb-2" type="text" name="title" value="${note.name}" required/>
                    <textarea class="form-control mb-2" name="content" rows="3">${note.content}</textarea>
                    <input type="color" name="color" class="form-control form-control-color mb-2" value="${note.color}" title="Background Color" />
                    <input type="color" name="text_color" class="form-control form-control-color mb-3" value="${note.text_color || '#000000'}" title="Text Color" />

                    <label class="form-label fw-bold mb-1">Share with:</label>
                    <div class="dropdown">
                        <button class="btn btn-light border w-100 text-start dropdown-toggle" type="button"
                                data-bs-toggle="dropdown" aria-expanded="false">
                            ${this.notes.selectedUsers.length ? this.notes.selectedUsers.map(uid => {
                                const u = this.notes.allUsers.find(u => u.id === uid);
                                return `<span class="badge bg-secondary me-1">${u?.name || 'Unknown'}</span>`;
                            }).join('') : '<span class="text-muted">Select Users</span>'}
                        </button>
                        <ul class="dropdown-menu w-100 px-2" style="max-height: 200px; overflow-y: auto;">
                            ${userOptions}
                        </ul>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="submit" class="btn btn-primary">Save</button>
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                </div>
            </form>
        </div>`;

    document.body.prepend(modal);

    // Checkbox logic
    modal.querySelectorAll(".user-checkbox").forEach((checkbox) => {
        checkbox.addEventListener("change", (e) => {
            const userId = parseInt(e.target.dataset.userId);
            if (e.target.checked) {
                if (!this.notes.selectedUsers.includes(userId)) {
                    this.notes.selectedUsers.push(userId);
                }
            } else {
                const index = this.notes.selectedUsers.indexOf(userId);
                if (index > -1) {
                    this.notes.selectedUsers.splice(index, 1);
                }
            }
        });
    });

    // Save logic
    modal.querySelector("form").addEventListener("submit", async (e) => {
        e.preventDefault();
        const form = e.target;
        const newTitle = form.title.value;
        const newContent = form.content.value;
        const newColor = form.color.value;
        const newTextColor = form.text_color.value;

        await this.env.services.orm.write("note.sticky", [noteId], {
            name: newTitle,
            content: newContent,
            color: newColor,
            text_color: newTextColor,
            user_ids: [[6, 0, this.notes.selectedUsers]],
        });

        modal.remove();
        location.reload();
    });

    modal.querySelector(".btn-close, .btn-secondary").addEventListener("click", () => {
        modal.remove();
    });
});

                sidebar.prepend(card);
            });

            container.prepend(sidebar);
        }
    },

});