import {html} from '@polymer/polymer';
import {ReduxConnectedElement} from '../../../../../ReduxConnectedElement';
import {property} from '@polymer/decorators/lib/decorators';
import LocalizeMixin from '../../../../../mixins/localize-mixin';
import UtilsMixin from '../../../../../mixins/utils-mixin';
import '@polymer/polymer/lib/elements/dom-if';
import '@polymer/iron-flex-layout/iron-flex-layout';
import '@polymer/iron-location/iron-location';
import '@polymer/iron-location/iron-query-params';
import '../../../../etools-prp-ajax';
import '../../../../etools-prp-permissions';
import '../../../../page-body';
import '../../../indicator-modal';
import {IndicatorModalEl} from '../../../indicator-modal';
import '../../../../list-view-indicators';
import Endpoints from '../../../../../endpoints';
import {clusterActivitiesIndicatorsFetch} from '../../../../../redux/actions/clusterActivities';
import {EtoolsPrpAjaxEl} from '../../../../etools-prp-ajax';
import {buttonsStyles} from '../../../../../styles/buttons-styles';
import {tableStyles} from '../../../../../styles/table-styles';
import {GenericObject} from '../../../../../typings/globals.types';

/**
 * @polymer
 * @customElement
 * @appliesMixin LocalizeMixin
 * @appliesMixin UtilsMixin
 */
class Indicators extends LocalizeMixin(UtilsMixin(ReduxConnectedElement)) {
  public static get template() {
    // language=HTML
    return html`
    ${buttonsStyles} ${tableStyles}
    <style include="iron-flex data-table-styles">
      :host {
        display: block;
      }

      div#action {
        margin: 25px 0;
        @apply --layout-horizontal;
        @apply --layout-end-justified;
      }
    </style>

    <etools-prp-permissions
        permissions="{{permissions}}">
    </etools-prp-permissions>

    <iron-location query="{{query}}"></iron-location>

    <iron-query-params
        params-string="{{query}}"
        params-object="{{queryParams}}">
    </iron-query-params>

    <etools-prp-ajax
        id="indicators"
        url="[[url]]"
        params="[[queryParams]]">
    </etools-prp-ajax>

    <page-body>
      <template
          is="dom-if"
          if="[[canAddIndicator]]"
          restamp="true">
        <div id="action">
          <paper-button id="add" on-tap="_openModal" class="btn-primary" raised>
            [[localize('add_cluster_activity_indicator')]]
          </paper-button>
        </div>
      </template>

      <indicator-modal
        id="indicatorModal"
        object="[[activityData]]"
        object-id="[[activityId]]"
        object-type="cluster.clusteractivity"
        modal-title="Add Cluster Activity Indicator">
      </indicator-modal>

      <list-view-indicators
          data="[[data]]"
          total-results="[[totalResults]]"
          type="ca"
          can-edit="[[canAddIndicator]]">
      </list-view-indicators>
    </page-body>
    `;
  }

  @property({type: Object})
  permissions!: GenericObject;

  @property({type: Object})
  queryParams!: GenericObject;

  @property({type: Object})
  activityData!: GenericObject;

  @property({type: Number})
  activityId!: number;

  @property({type: Number})
  clusterId!: number;

  @property({type: Array, computed: '_computeCurrentIndicators(activityId, allIndicators)'})
  data!: any[];

  @property({type: Number, computed: '_computeCurrentIndicatorsCount(activityId, allIndicatorsCount)'})
  totalResults!: number;

  @property({type: String, computed: '_computeUrl(activityId, queryParams)'})
  url!: string;

  @property({type: Object, computed: 'getReduxStateObject(rootState.clusterActivities.indicators)'})
  allIndicators!: GenericObject;

  @property({type: Number, computed: 'getReduxStateValue(rootState.clusterActivities.indicatorsCount)'})
  allIndicatorsCount!: number;

  @property({type: Boolean, computed: '_computeCanAddIndicator(permissions, clusterId)'})
  canAddIndicator!: boolean;

  static get observers() {
    return [
      '_clusterActivityIndicatorsAjax(queryParams, activityId)',
    ];
  }

  _openModal() {
    (this.$.indicatorModal as IndicatorModalEl).open();
  }

  _onSuccess() {
    this._clusterActivityIndicatorsAjax();
  }

  _computeCurrentIndicators(activityId: number, allIndicators: GenericObject) {
    return allIndicators[activityId];
  }

  _computeCurrentIndicatorsCount(activityId: number, allIndicatorsCount: number) {
    return allIndicatorsCount[activityId];
  }

  _computeUrl() {
    //Make sure the queryParams are updated before the thunk is created:
    this.set('queryParams.object_id', this.activityId);

    return Endpoints.indicators('ca');
  }

  _clusterActivityIndicatorsAjax() {
    const thunk = (this.$.indicators as EtoolsPrpAjaxEl).thunk();
    (this.$.indicators as EtoolsPrpAjaxEl).abort();

    this.reduxStore.dispatch(clusterActivitiesIndicatorsFetch(thunk, String(this.activityId)))
      // @ts-ignore
      .catch(function(err) {
        // TODO: error handling.
      });
  }

  _computeCanAddIndicator(permissions: GenericObject, clusterId: number) {
    return permissions && permissions.createClusterEntities &&
      permissions.createClusterEntitiesForCluster(clusterId);
  }


  _addEventListeners() {
    this._onSuccess = this._onSuccess.bind(this);
    this.addEventListener('indicatorModal.indicator-added', this._onSuccess);
    this.addEventListener('indicator-edited', this._onSuccess);
  }

  _removeEventListeners() {
    this.removeEventListener('indicatorModal.indicator-added', this._onSuccess);
    this.removeEventListener('indicator-edited', this._onSuccess);
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

window.customElements.define('rp-clusters-activity-indicators', Indicators);

export {Indicators as RpClusterActivityIndicatorsEl};