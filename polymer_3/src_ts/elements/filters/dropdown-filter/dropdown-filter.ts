import {ReduxConnectedElement} from '../../../ReduxConnectedElement';
import {html} from '@polymer/polymer';
import {property} from '@polymer/decorators';
import '../dropdown-filter/searchable-dropdown-filter';
import '@polymer/paper-item/paper-item';
import '@polymer/paper-dropdown-menu/paper-dropdown-menu';
import '@polymer/paper-listbox/paper-listbox';
import FilterMixin from '../../../mixins/filter-mixin';
import LocalizeMixin from '../../../mixins/localize-mixin';
import {fireEvent} from '../../../utils/fire-custom-event';
import '@polymer/polymer/lib/elements/dom-repeat';
import {DomRepeat} from '@polymer/polymer/lib/elements/dom-repeat';

/**
 * @polymer
 * @customElement
 * @appliesMixin FilterMixin
 * @appliesMixin LocalizeMixin
 */
class DropdownFilter extends LocalizeMixin(FilterMixin(ReduxConnectedElement)) {
  static get template() {
    return html`
    <style>
      :host {
        display: block;
      }

      paper-dropdown-menu {
        width: 100%;
      }

      paper-listbox paper-item {
        height: 48px;
        cursor: pointer;
        padding: 0 16px;
        white-space: nowrap;
      }
    </style>

    <paper-dropdown-menu
        id="field"
        label="[[label]]"
        disabled="[[disabled]]"
        always-float-label>
      <paper-listbox
          slot="dropdown-content"
          class="dropdown-content"
          selected="[[selected]]"
          on-iron-select="_handleFilterChange">
        <template
            id="repeat"
            is="dom-repeat"
            items="[[data]]">
          <paper-item>[[item.title]]</paper-item>
        </template>
      </paper-listbox>
    </paper-dropdown-menu>
  `;
  }


  @property({type: Boolean})
  disabled!: boolean;

  @property({type: Number})
  selected!: number;

  @property({type: String})
  value = '';

  @property({type: Array, observer: '_handleData'})
  data = [];


  public static get observers() {
    return [
      '_updateSelected(value, data)',
    ]
  }

  _handleFilterChange(e: CustomEvent) {
    const newValue = (this.$.repeat as DomRepeat).itemForElement(e.detail.item).id;

    fireEvent(this, 'filter-changed', {
      name: this.name,
      value: String(newValue),
    });
  };

  _updateSelected(value: String, data: any) {
    setTimeout(() => {
      const selectedIndex = data.findIndex(function(item: any) {
        return String(item.id) === String(value)
      });

      if (selectedIndex !== this.selected) {
        this.set('selected', selectedIndex);
      }
    });
  }

  _handleData(data: any) {
    if (data.length) {
      this._filterReady();
    }
  }

}

window.customElements.define('dropdown-filter', DropdownFilter);