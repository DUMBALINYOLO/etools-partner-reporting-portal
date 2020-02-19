import {html} from '@polymer/polymer';
import Endpoints from "../../endpoints";
import UtilsMixin from "../../mixins/utils-mixin";
import NotificationsMixin from "../../mixins/notifications-mixin";
import LocalizeMixin from "../../mixins/localize-mixin";
// <link rel="import" href="../../../bower_components/etools-file/etools-file.html">
// <link rel="import" href="../../redux/actions/localize.html">
// <link rel="import" href="../../redux/store.html">
// <link rel="import" href="../../redux/actions/pdReportsAttachments.html">
// <link rel="import" href="../../redux/selectors/programmeDocumentReportsAttachments.html">
import '../etools-prp-ajax';
import {ReduxConnectedElement} from "../../ReduxConnectedElement";
import '@polymer/polymer/lib/elements/dom-if';
import {property} from "@polymer/decorators/lib/decorators";
import {programmeDocumentReportsAttachmentsCurrent} from "../../redux/selectors/programmeDocumentReportsAttachments";
import {programmeDocumentReportsAttachmentsPending} from "../../redux/selectors/programmeDocumentReportsAttachments";
import {GenericObject} from "../../typings/globals.types";
import {pdReportsAttachmentsSync} from "../../redux/actions/pdReportsAttachments";
import {Debouncer} from "@polymer/polymer/lib/utils/debounce";
import {timeOut} from "@polymer/polymer/lib/utils/async";


/**
 * @polymer
 * @customElement
 * @appliesMixin UtilsMixin
 * @appliesMixin NotificationsMixin
 * @appliesMixin LocalizeMixin
 */
class ReportAttachments extends UtilsMixin(NotificationsMixin(LocalizeMixin(ReduxConnectedElement))){
  public static get template(){
    return html`
      <style>
        :host {
          display: block;
        }
        
        #face-container, #other-one-container, #other-two-container {
          display: flex;
          justify-content: space-between;
          align-items: center;
          flex-direction: row;
        }
      </style>  
      
      <etools-prp-ajax
          id="upload"
          method="post"
          loading="{{loading}}"
          url="[[attachmentsListUrl]]">
      </etools-prp-ajax>
  
      <etools-prp-ajax
          id="replace"
          method="put"
          url="[[attachmentDeleteUrl]]">
      </etools-prp-ajax>
  
      <etools-prp-ajax
          id="download"
          method="get"
          url="[[attachmentsListUrl]]">
      </etools-prp-ajax>
  
      <etools-prp-ajax
          id="delete"
          method="delete"
          url="[[attachmentDeleteUrl]]">
      </etools-prp-ajax>
      
      <div id="face-container">
        <etools-file
            id="faceAttachmentComponent"
            files="{{faceAttachment}}"
            label="[[localize('face')]]"
            disabled="[[pending]]"
            readonly="[[readonly]]"
            use-delete-events>
        </etools-file>
  
        <template is="dom-if" if="{{faceLoading}}">
          <paper-spinner active></paper-spinner>
        </template>
      </div>
      
      <div id="other-one-container">
        <etools-file
            id="otherOneAttachmentComponent"
            files="{{otherOneAttachment}}"
            label="[[localize('other')]] #1"
            disabled="[[pending]]"
            readonly="[[readonly]]"
            use-delete-events>
        </etools-file>
  
        <template is="dom-if" if="{{otherOneLoading}}">
          <paper-spinner active></paper-spinner>
        </template>
      </div>
      
      <div id="other-two-container">
        <etools-file
            id="otherTwoAttachmentComponent"
            files="{{otherTwoAttachment}}"
            label="[[localize('other')]] #2"
            disabled="[[pending]]"
            readonly="[[readonly]]"
            use-delete-events>
        </etools-file>
  
        <template is="dom-if" if="{{otherTwoLoading}}">
          <paper-spinner active></paper-spinner>
        </template>
      </div>
      
      
    `;
  }

  @property({type: Boolean})
  readonly!: boolean;

  @property({type: Array})
  faceAttachment!: any[];

  @property({type: Array})
  otherOneAttachment!: any[];

  @property({type: Array})
  otherTwoAttachment!: any[];

  @property({type: Boolean})
  faceLoading!: boolean;

  @property({type: Boolean})
  otherOneLoading!: boolean;

  @property({type: Boolean})
  otherTwoLoading!: boolean;

  @property({type: Boolean, computed: 'programmeDocumentReportsAttachmentsPending(state)'})
  pending!: boolean;

  @property({type: Array, computed: 'programmeDocumentReportsAttachmentsCurrent(state)', observer: '_setFiles'})
  attachments!: GenericObject[];

  @property({type: String, computed: '_computeListUrl(locationId, reportId)'})
  attachmentsListUrl!: string;

  @property({type: String})
  attachmentDeleteUrl!: string;

  @property({type: String, computed: 'getReduxStateValue(rootState.location.id)'})
  locationId!: string;

  @property({type: String, computed: 'getReduxStateValue(rootState.programmeDocumentReports.current.id)'})
  reportId!: string;

  filesChanged: Debouncer | null;

  static get observers(){
    return [
      '_filesChanged(faceAttachment.*)',
      '_filesChanged(otherOneAttachment.*)',
      '_filesChanged(otherTwoAttachment.*)'
    ];
  }

  _computeListUrl(locationId: string, reportId: string) {
    return ReportAttachmentsUtils.computeListUrl(locationId, reportId);
  }

  _setFiles(attachments: GenericObject[]) {
    let self = this;
    this.set('faceAttachment', []);
    this.set('otherOneAttachment', []);
    this.set('otherTwoAttachment', []);

    ReportAttachmentsUtils.setFiles(this.attachments)
      .forEach(function (attachment: GenericObject) {
        if (attachment.type === 'Other' && self.get('otherOneAttachment').length === 1) {
          self.set('otherTwoAttachment', [attachment]);
        } else if (attachment.type === 'Other') {
          self.set('otherOneAttachment', [attachment]);
        } else {
          self.set('faceAttachment', [attachment]);
        }
      });
  }

  _getDeleteUrl(locationId: string, reportId: string, attachmentId) {
    return ReportAttachmentsUtils.getDeleteUrl(locationId, reportId, attachmentId);
  }

  _onDeleteFile(e: CustomEvent) {
    let self = this;
    let deleteThunk;
    let deleteUrl = self._getDeleteUrl(self.locationId, self.reportId, e.detail.file.id);

    this.set('attachmentDeleteUrl', deleteUrl);

    e.stopPropagation();

    deleteThunk = this.shadowRoot!.querySelector('#delete').thunk();

    this.shadowRoot!.querySelector('#delete').abort();

    return this.reduxStore.dispatch(
      pdReportsAttachmentsSync(deleteThunk, this.reportId)
    ).then(function () {
      self._notifyFileDeleted();
      self.set('attachmentDeleteUrl', undefined);

      if (self.get('faceAttachment').length !== 0 && e.detail.file.id === self.get('faceAttachment')[0].id) {
        self.$.faceAttachmentComponent.fileInput.value = null;
        self.$.faceAttachmentComponent.set('files', []);
      } else if (self.get('otherOneAttachment').length !== 0
        && e.detail.file.id === self.get('otherOneAttachment')[0].id) {
        self.$.otherOneAttachmentComponent.fileInput.value = null;
        self.$.otherOneAttachmentComponent.set('files', []);
      } else if (self.get('otherTwoAttachment').length !== 0
        && e.detail.file.id === self.get('otherTwoAttachment')[0].id) {
        self.$.otherTwoAttachmentComponent.fileInput.value = null;
        self.$.otherTwoAttachmentComponent.set('files', []);
      }
    })
      .catch(function (err) { // jshint ignore:line
        // TODO: error handling
      });
  }

  _filesChanged(change: GenericObject) {
    let attachmentPropertyName = change.path.replace('.length', '');
    let isEmpty = change.value === 0 ? true : false;
    let attachment = isEmpty ? undefined : change.base[0];
    let self = this;

    if (attachment === undefined) {
      return;
    }

    let files = isEmpty ? [] : change.base;

    files.findIndex(function (file: GenericObject) {
      if (/[^a-zA-Z0-9-_\.]+/.test(file.file_name)) {
        file.file_name = file.file_name.replace(/[^a-zA-Z0-9-_\.]+/g, '_');
      }
    });

    let attachmentType = attachmentPropertyName.toLowerCase().indexOf('face') !== -1 ? 'FACE' : 'Other';

    if (isEmpty || (!isEmpty && attachment.path !== null)) {
      return;
    }


    this.filesChanged = Debouncer.debounce(this.filesChanged, timeOut.after(100), () =>{
      let thunk;
      let data;

      if (change.path.split('.').length < 2 || !files.length) {
        return;
      }

      data = new FormData();

      files.forEach(function(file) {
        data.append('path', file.raw, file.file_name);
        data.append('type', attachmentType);
      });

      if (attachment.id === null) {
        thunk = this.shadowRoot!.querySelector('#upload').thunk();
        this.this.shadowRoot!.querySelector('#upload').abort();
        this.this.shadowRoot!.querySelector('#upload').body = data;

        if (attachmentPropertyName === 'faceAttachment') {
          this.set('faceLoading', true);
        } else if (attachmentPropertyName === 'otherOneAttachment') {
          this.set('otherOneLoading', true);
        } else if (attachmentPropertyName === 'otherTwoAttachment') {
          this.set('otherTwoLoading', true);
        }
      } else {
        let replaceUrl = self._getDeleteUrl(self.locationId, self.reportId, attachment.id);
        this.set('attachmentDeleteUrl', replaceUrl);

        thunk = this.shadorRoot!.querySelector('#replace').thunk();
        this.shadorRoot!.querySelector('#replace').abort();
        this.shadorRoot!.querySelector('#replace').body = data;

        attachmentPropertyName = attachmentPropertyName.split('.')[0];
      }

      this.reduxStore.dispatch(
        pdReportsAttachmentsSync(thunk, this.reportId)
      )
        .then(function () {
          self._notifyFileUploaded();

          self.set('faceLoading', false);
          self.set('otherOneLoading', false);
          self.set('otherTwoLoading', false);

          let attachments = self.get('attachments');

          attachments.forEach(function(item) {
            if (attachment.id !== null && item.id === attachment.id) {
              self.set(attachmentPropertyName, [item]);
              return;
            }
          });

          if (attachment.id === null) {
            let duplicates = attachments.filter(function(item) {
              let tokens = attachment.file_name.split('.');
              if (tokens.length === 0) {
                return item.file_name.indexOf(attachment.file_name) !== -1;
              } else {
                return item.file_name.indexOf(tokens[0]) !== -1 && item.file_name.indexOf(tokens[1]) !== -1;
              }
            });

            if (duplicates.length === 1) {
              self.set(attachmentPropertyName, [duplicates[0]]);
            } else {
              let correctedItem;

              duplicates.forEach(function(item) {
                if (item.file_name !== attachment.file_name) {
                  correctedItem = item;
                  return;
                }
              });

              self.set(attachmentPropertyName, [correctedItem]);
            }
          }

          self.set('attachmentDeleteUrl', undefined);
        })
        .catch(function (err) { // jshint ignore:line
          console.error(err);
          // TODO: error handling
        });
    });

  }

  _addEventListeners() {
    this._onDeleteFile = this._onDeleteFile.bind(this);
    this.addEventListener('delete-file', this._onDeleteFile);
    // TODO(dci): NOT FOUND !!!
    // this._onProgressChanged = this._onProgressChanged.bind(this);
    // this.addEventListener('prp-file-progress-changed', this._onProgressChanged);
  }

  _removeEventListeners() {
    this.removeEventListener('delete-file', this._onDeleteFile);
    // this.removeEventListener('prp-file-progress-changed', this._onProgressChanged);
  }

  connectedCallback() {
    super.connectedCallback();
    this._addEventListeners();
    let downloadThunk = this.shadowRoot!.querySelector('#download').thunk();

    this.shadowRoot!.querySelector('#download').abort();

    this.reduxStore.dispatch(
      pdReportsAttachmentsSync(downloadThunk, this.reportId)
    )
      .catch(function (err) { // jshint ignore:line
        // TODO: error handling
      });
  }

  disconnectedCallback() {
    super.disconnectedCallback();
    this._removeEventListeners();
    [
      this.shadowRoot!.querySelector('#download'),
      this.shadowRoot!.querySelector('#upload'),
      this.shadowRoot!.querySelector('#delete'),
    ].forEach(function (req) {
      req.abort();
    });

    if (this.filesChanged && this.filesChanged.isActive()) {
      this.filesChanged.cancel();
    }
  }

}

window.customElements.define('report-attachments', ReportAttachments);
