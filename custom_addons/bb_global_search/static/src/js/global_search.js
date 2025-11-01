import { Component, useState, useRef, useEffect } from "@odoo/owl";

import { useDiscussSystray } from "@mail/utils/common/hooks";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { useDropdownState } from "@web/core/dropdown/dropdown_hooks";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Domain } from "@web/core/domain";
import { user } from "@web/core/user";
import { rpc } from "@web/core/network/rpc"
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { debounce } from "@web/core/utils/timing";

export class GlobalSearch extends Component{
    static components = { Dropdown, DropdownItem };
    static props = [];
    static template = "global_search.GlobalSearchMenu";

    setup() {
        super.setup()
        this.inputRef = useRef("searchInput");
        this.state = useState({search_results : []})
        this.orm = useService("orm");
        this.models = [];
        this.onSearchInput = debounce((ev) => this.onSearchInputKeydown(ev), 200);
        }

    async getSelectedModels(){
        this.models = await rpc("/company/get_search_models");
    }

    async get_records(value){
         var result = [];
         var id_cnt = 1;
         for(let i=0;i<this.models.length;i++){
                var model = this.models[i].model;
                await this.orm.call(model, "name_search", [], {
                        name: value,
                        operator: "ilike"
                    }).then((records)=>{

                      for(let j=0;j<records.length;j++){

                        var record = records[j];
                        result.push({id:id_cnt,
                                name:record[1],
                                rec_id:record[0],
                                model:model,
                                resModel:this.models[i].name})
                        id_cnt++;


                }
                    });
         }
         return result;

    }

    async performSearch(value){

        console.log(">>>>>>>.",value);
        await this.getSelectedModels();
        this.state.search_results = await this.get_records(value);

    }

    onSearchInputKeydown(ev){
        if(ev && ev.target.value != ''){
        const value = ev.target.value;
        this.performSearch(value);
        }

    }

    async openRecord(resModel,resId){
      this.env.services.action.doAction({
            type: "ir.actions.act_window",
            res_model: resModel,
            views: [[false, "form"]],
            res_id: parseInt(resId),
        });

    }


}


registry
    .category("systray")
    .add("bb_global_search.global_search", { Component: GlobalSearch }, { sequence: 1 });