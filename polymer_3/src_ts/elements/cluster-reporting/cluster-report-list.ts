import {ReduxConnectedElement} from '../../ReduxConnectedElement';
import {html} from '@polymer/polymer';
import '@unicef-polymer/etools-loading/etools-loading';
import '@unicef-polymer/etools-data-table/etools-data-table';
import '@polymer/iron-location/iron-location';
import '@polymer/iron-location/iron-query-params';
import Constants from '../../constants';
import UtilsMixin from '../../mixins/utils-mixin';
import PaginationMixin from '../../mixins/pagination-mixin';
import DataTableMixin from '../../mixins/data-table-mixin';
import '../confirm-box';
import '../list-placeholder';
import './cluster-report-proxy';
import {property} from '@polymer/decorators/lib/decorators';
import {GenericObject} from '../../typings/globals.types';


/**
 * @polymer
 * @customElement
 * @appliesMixin UtilsMixin
 * @appliesMixin PaginationMixin
 * @appliesMixin DataTableMixin
 */
class ClusterReportList extends UtilsMixin(PaginationMixin(DataTableMixin(ReduxConnectedElement))){
  public static get template(){
    return html`
      <style>
        :host {
          display: block;
  
          --list-bg-color: transparent;
          --list-divider-color: transparent;
        }
  
        .wrapper {
          min-height: 120px;
          position: relative;
        }
  
        etools-data-table-row {
          display: block;
        }
  
        etools-data-table-row:not(:last-of-type) {
          margin-bottom: 2px;
        }
      </style>  
      
      <iron-location
        query="{{ query }}">
      </iron-location>
  
      <iron-query-params
        params-string="{{ query }}"
        params-object="{{ queryParams }}">
      </iron-query-params>
  
      <etools-data-table-footer
        page-size="[[pageSize]]"
        page-number="[[pageNumber]]"
        total-results="[[totalResults]]"
        on-page-size-changed="_pageSizeChanged"
        on-page-number-changed="_pageNumberChanged">
      </etools-data-table-footer>
      
      <div class="wrapper">
        <template
          is="dom-repeat"
          items="[[data]]"
          initial-count="[[pageSize]]">
          <etools-data-table-row no-collapse>
            <div slot="row-data">
              <cluster-report-proxy
                data="[[item]]"
                mode="[[mode]]">
              </cluster-report-proxy>
            </div>
          </etools-data-table-row>
        </template>
  
        <list-placeholder
          data="[[data]]"
          loading="[[loading]]">
        </list-placeholder>
  
        <etools-loading active="[[loading]]"></etools-loading>
      </div>
  
      <etools-data-table-footer
        page-size="[[pageSize]]"
        page-number="[[pageNumber]]"
        total-results="[[totalResults]]"
        on-page-size-changed="_pageSizeChanged"
        on-page-number-changed="_pageNumberChanged">
      </etools-data-table-footer>
  
      <confirm-box id="confirm"></confirm-box>
    `;
  }

  @property({type: String})
  mode!: string;

  @property({type: Boolean, computed: 'getReducStateValue(rootState.clusterIndicatorReports.loading)'})
  loading!: boolean;

  @property({type: Array })
  data!: GenericObject[];
    // statePath: Selectors.ClusterIndicatorReports.all,

  @property({type: Number, computed: 'getReducStateValue(rootState.clusterIndicatorReports.count)'})
  totalResults!: number;

  @property({type: Object, computed: 'getReducStateValue(rootState.userProfile.profile)'})
  profile!: GenericObject;

  @property({type: Boolean, computed: '_computeIsIMOClusters(profile)'})
  isIMO!: boolean;


  _computeIsIMOClusters(profile: GenericObject) {
    return profile.prp_roles ? profile.prp_roles.some(function (role) {
      return role.role === Constants.PRP_ROLE.CLUSTER_IMO;
    }) : [];
  }

  _onConfirm(e: CustomEvent) {
    e.stopPropagation();
    const result = e.detail;
    if (!this.isIMO) {
      this.$.confirm.run({
        body:
          'The IMO will be informed of this submission and you will ' +
          'not be able to make any changes on this report unless it ' +
          'is sent back to you. Are you sure you’d like to Submit this report?',
        result: result,
        maxWidth: '500px',
        mode: Constants.CONFIRM_MODAL,
      });
    } else if (this.isIMO) {
      this.$.confirm.run({
        body: 'Are you sure you’d like to Submit this report?',
        result: result,
        maxWidth: '500px',
        mode: Constants.CONFIRM_MODAL,
      });
    }
  }

  _onContentsChanged(e: CustomEvent) {
    let tail = this.totalResults % this.pageSize;
    let last = Math.ceil(this.totalResults / this.pageSize);

    if (tail === 1 && last !== 1 && this.pageNumber === last) {
      e.stopPropagation();

      this.set('queryParams.page', this.pageNumber - 1);
    } else {
      // Let the parent component handle the event
    }
  }

  _addEventListeners() {
    this._onConfirm = this._onConfirm.bind(this);
    this.addEventListener('report-submit-confirm', this._onConfirm);
    this._onContentsChanged = this._onContentsChanged.bind(this);
    this.addEventListener('report-submitted', this._onContentsChanged);
    this.addEventListener('report-reviewed', this._onContentsChanged);
  }

  _removeEventListeners() {
    this.removeEventListener('report-submit-confirm', this._onConfirm);
    this.removeEventListener('report-submitted', this._onContentsChanged);
    this.removeEventListener('report-reviewed', this._onContentsChanged);
  }

  connectedCallback() {
    super.connectedCallback();
    this._addEventListeners();
  }

  disconnectedCallback() {
    super.disconnectedCallback();
    this._removeEventListeners();
  }

}

window.customElements.define('cluster-report-list', ClusterReportList);
