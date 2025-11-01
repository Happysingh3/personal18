/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { onWillStart, useState, useRef, useEffect } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

function formatIndianCurrency(x) {
    if (x === null || x === undefined) return '0';
    x = x.toString();
    let afterPoint = '';
    if (x.indexOf('.') > 0) afterPoint = x.substring(x.indexOf('.'), x.length);
    x = Math.floor(x).toString();
    let lastThree = x.substring(x.length - 3);
    let otherNumbers = x.substring(0, x.length - 3);
    if (otherNumbers !== '') lastThree = ',' + lastThree;
    return otherNumbers.replace(/\B(?=(\d{2})+(?!\d))/g, ",") + lastThree + afterPoint;
}

export class CrmDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.Leadstage = useRef('leads_stage');
        this.LeadByMonth = useRef('leads_by_month');
        this.CrmActivities = useRef('crm_activities');
        this.LeadByCampaign = useRef('leads_campaign');
        this.LeadByMedium = useRef('leads_medium');
        this.LeadBySource = useRef('leads_source');
        this.LostLead = useRef('leads_lost');
        this.TotalRevenue = useRef('total_revenue');

        this.state = useState({
            period: 'month',
            leads: null,
            opportunities: null,
            exp_revenue: null,
            revenue: null,
            win_ratio: null,
            avg_close_time: null,
            opportunity_ratio: null,
            unassigned_leads: null,
            payment_received: '0',
            so_received: '0',
            payment_to_be_received: '0',
            tender_payment_received: '0',
            tender_so_received: '0',
            tender_delivery_done: '0',

            charts: [],
            upcoming_events: [],
            current_lang: [],
            top_sp_revenue: [],
            country_count: [],
            country_revenue: [],
            recent_activities: [],
        });

        onWillStart(async () => {
            await this.fetch_data();
            await this.UpcomingEvents();
            await this.TopSpRevenue();
            await this.TopCountryRevenue();
            await this.TopCountryCount();
            await this.RecentActivities();
        });

        useEffect(() => {
            if (this.state.charts.length > 0) {
                this.state.charts.forEach((c) => c.destroy());
            }
            if (this.state.period) {
                this.fetch_data();
                this.render_leads_by_stage();
                this.render_leads_by_month();
                this.render_crm_activities();
                this.render_lead_by_campaign();
                this.render_lead_by_medium();
                this.render_lead_by_source();
                this.render_lost_lead();
                this.render_total_revenue();
            }
        }, () => [this.state.period]);
    }

    async fetch_data() {
        const result = await this.orm.call('crm.lead', "get_data", [this.state.period]);
        this.state.leads = result['leads'];
        this.state.opportunities = result['opportunities'];
        this.state.exp_revenue = formatIndianCurrency(result['exp_revenue']);
        this.state.revenue = formatIndianCurrency(result['revenue']);
        this.state.win_ratio = result['win_ratio'];
        this.state.opportunity_ratio = result['opportunity_ratio'];
        this.state.avg_close_time = result['avg_close_time'];
        this.state.unassigned_leads = result['unassigned_leads'];

        // legacy total (not used for tiles now)
        const payAll = await this.orm.call('crm.lead', "get_total_closing_value", [this.state.period]);
        this.state.payment_received = formatIndianCurrency(payAll?.total_closing_value || 0);

        // stage-wise totals → tiles
        const stageTotals = await this.orm.call(
            'crm.lead',
            'get_stage_closing_totals',
            [this.state.period, ['SO Received', 'Delivery Done', 'Payment Received']]
        );
        this.state.so_received = formatIndianCurrency(stageTotals['SO Received'] || 0);
        this.state.payment_to_be_received = formatIndianCurrency(stageTotals['Delivery Done'] || 0);
        this.state.payment_received = formatIndianCurrency(stageTotals['Payment Received'] || 0);

        // NEW: Tender team → Payment Received
        const tenderTotal = await this.orm.call(
            'crm.lead',
            'get_team_stage_closing_total',
            [this.state.period, 'Tender', 'Payment Received']
        );
        this.state.tender_payment_received = formatIndianCurrency(tenderTotal || 0);

        // --- existing stageTotals + tender_payment_received code ke just baad ---
        // Tender – SO Received
        const t_so = await this.orm.call(
            'crm.lead',
            'get_team_stage_closing_total',
            [this.state.period, 'Tender', 'SO Received']
        );
        this.state.tender_so_received = formatIndianCurrency(t_so || 0);

        // Tender – Delivered Drone
        const t_dd = await this.orm.call(
            'crm.lead',
            'get_team_stage_closing_total',
            [this.state.period, 'Tender', 'Delivery Done']
        );
        this.state.tender_delivery_done = formatIndianCurrency(t_dd || 0);

    }

    // -------- your other methods remain as-is --------
    async UpcomingEvents() { /* your same code */ }
    async TopSpRevenue()   { /* your same code */ }
    async TopCountryCount(){ /* your same code */ }
    async TopCountryRevenue(){ /* your same code */ }
    async RecentActivities(){ /* your same code */ }

    SetPeriods() {
        const today = new Date();
        let start_date;
        if (this.state.period === 'year') {
            start_date = new Date(today.getFullYear(), 0, 1);
        } else if (this.state.period === 'quarter') {
            const startMonth = Math.floor(today.getMonth() / 3) * 3;
            start_date = new Date(today.getFullYear(), startMonth, 1);
        } else if (this.state.period === 'week') {
            const dayOfWeek = today.getDay();
            const diff = today.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1);
            start_date = new Date(today.setDate(diff));
        } else {
            start_date = new Date(today.getFullYear(), today.getMonth(), 1);
        }
        return `${start_date.getFullYear()}-${(start_date.getMonth()+1).toString().padStart(2,'0')}-${start_date.getDate().toString().padStart(2,'0')}`;
    }

    OnChangePeriods() {}

    onClickLeads() { /* your same code */ }
    onClickOpportunities() { /* your same code */ }
    onClickExpRevenue() { /* your same code */ }
    onClickRevenue() { /* your same code */ }
    onClickUnAssignedLeads() { /* your same code */ }

    onClickSOReceived() {
        const date = this.SetPeriods();
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "SO Received",
            res_model: 'crm.lead',
            views: [[false, "list"], [false, "form"]],
            target: "current",
            domain: [
                ['stage_id.name', '=', 'SO Received'],
                ['create_date', '>=', date],
                ['closing_value_num', '>', 0],
            ],
        });
    }

    onClickPaymentToBeReceived() {
        const date = this.SetPeriods();
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Delivery Done",
            res_model: 'crm.lead',
            views: [[false, "list"], [false, "form"]],
            target: "current",
            domain: [
                ['stage_id.name', '=', 'Delivery Done'],
                ['create_date', '>=', date],
                ['closing_value_num', '>', 0],
            ],
        });
    }

    onClickPaymentReceived() {
        const date = this.SetPeriods();
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Payment Received",
            res_model: 'crm.lead',
            views: [[false, "list"], [false, "form"]],
            target: "current",
            domain: [
                ['stage_id.name', '=', 'Payment Received'],
                ['create_date', '>=', date],
                ['closing_value_num', '>', 0],
            ],
        });
    }

    // NEW: open Tender team filtered list
    onClickTenderPaymentReceived() {
        const date = this.SetPeriods();
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Tender – Payment Received",
            res_model: 'crm.lead',
            views: [[false, "list"], [false, "form"]],
            target: "current",
            domain: [
                ['team_id.name', 'ilike', 'Tender'],
                ['stage_id.name', '=', 'Payment Received'],
                ['create_date', '>=', date],
                ['closing_value_num', '>', 0],
            ],
        });
    }

    onClickTenderSOReceived() {
    const date = this.SetPeriods();
    this.action.doAction({
        type: "ir.actions.act_window",
        name: "Tender – SO Received",
        res_model: 'crm.lead',
        views: [[false, "list"], [false, "form"]],
        target: "current",
        domain: [
            ['team_id.name', 'ilike', 'Tender'],
            ['stage_id.name', '=', 'SO Received'],
            ['create_date', '>=', date],
            ['closing_value_num', '>', 0],
        ],
    });
}

onClickTenderDeliveryDone() {
    const date = this.SetPeriods();
    this.action.doAction({
        type: "ir.actions.act_window",
        name: "Tender – Delivery Done",
        res_model: 'crm.lead',
        views: [[false, "list"], [false, "form"]],
        target: "current",
        domain: [
            ['team_id.name', 'ilike', 'Tender'],
            ['stage_id.name', '=', 'Delivery Done'],
            ['create_date', '>=', date],
            ['closing_value_num', '>', 0],
        ],
    });
}


    async render_leads_by_stage()   { /* your same code */ }
    async render_leads_by_month()   { /* your same code */ }
    async render_crm_activities()   { /* your same code */ }
    async render_lead_by_campaign() { /* your same code */ }
    async render_lead_by_medium()   { /* your same code */ }
    async render_lead_by_source()   { /* your same code */ }
    async render_lost_lead()        { /* your same code */ }
    async render_total_revenue()    { /* your same code */ }
}

CrmDashboard.template = 'CrmDashboard';
registry.category("actions").add("crm_dashboard", CrmDashboard);
