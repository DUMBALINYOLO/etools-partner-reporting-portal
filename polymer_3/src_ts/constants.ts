
const PRP_ROLE = {
  ALL: 'ALL',
  IP_AUTHORIZED_OFFICER: 'IP_AUTHORIZED_OFFICER',
  IP_EDITOR: 'IP_EDITOR',
  IP_VIEWER: 'IP_VIEWER',
  IP_ADMIN: 'IP_ADMIN',
  CLUSTER_IMO: 'CLUSTER_IMO',
  CLUSTER_SYSTEM_ADMIN: 'CLUSTER_SYSTEM_ADMIN',
  CLUSTER_VIEWER: 'CLUSTER_VIEWER',
  CLUSTER_COORDINATOR: 'CLUSTER_COORDINATOR',
  CLUSTER_MEMBER: 'CLUSTER_MEMBER'
}

const App = {
  Constants: {
    SET_TOKEN: 'SET_TOKEN',
    RESET_TOKEN: 'RESET_TOKEN',

    SET_ACCOUNT_TYPE: 'SET_ACCOUNT_TYPE',
    ACCOUNT_TYPE_PARTNER: 'ACCOUNT_TYPE_PARTNER',
    ACCOUNT_TYPE_CLUSTER: 'ACCOUNT_TYPE_CLUSTER',

    USER_LOGIN: 'USER_LOGIN',
    USER_LOGOUT: 'USER_LOGOUT',
    SET_USER_PROFILE: 'SET_USER_PROFILE',

    SET_WORKSPACE: 'SET_WORKSPACE',
    SET_WORKSPACES: 'SET_WORKSPACES',

    SET_LOCATION: 'SET_LOCATION',

    SET_APP: 'SET_APP',

    SET_INDICATORS: 'SET_INDICATORS',
    SET_INDICATORS_COUNT: 'SET_INDICATORS_COUNT',
    INDICATORS_LOADING_START: 'INDICATORS_LOADING_START',
    INDICATORS_LOADING_STOP: 'INDICATORS_LOADING_STOP',
    SET_INDICATOR_DETAILS: 'SET_INDICATOR_DETAILS',
    INDICATOR_DETAILS_LOADING_START: 'INDICATOR_DETAILS_LOADING_START',
    INDICATOR_DETAILS_LOADING_STOP: 'INDICATOR_DETAILS_LOADING_STOP',

    SET_PARTNER: 'SET_PARTNER',

    SET_PARTNER_PROJECTS_LIST: 'SET_PARTNER_PROJECTS_LIST',
    SET_PARTNER_PROJECTS_COUNT: 'SET_PARTNER_PROJECTS_COUNT',
    PARTNER_PROJECTS_LOADING_START: 'PARTNER_PROJECTS_LOADING_START',
    PARTNER_PROJECTS_LOADING_STOP: 'PARTNER_PROJECTS_LOADING_STOP',
    SET_PARTNER_PROJECT_DETAILS: 'SET_PARTNER_PROJECT_DETAILS',
    PARTNER_PROJECT_DETAILS_LOADING_START: 'PARTNER_PROJECT_DETAILS_LOADING_START',
    PARTNER_PROJECT_DETAILS_LOADING_STOP: 'PARTNER_PROJECT_DETAILS_LOADING_STOP',

    SET_PARTNER_ACTIVITIES_LIST: 'SET_PARTNER_ACTIVITIES_LIST',
    SET_PARTNER_ACTIVITIES_COUNT: 'SET_PARTNER_ACTIVITIES_COUNT',
    PARTNER_ACTIVITIES_LOADING_START: 'PARTNER_ACTIVITIES_LOADING_START',
    PARTNER_ACTIVITIES_LOADING_STOP: 'PARTNER_ACTIVITIES_LOADING_STOP',

    SET_CLUSTER_OBJECTIVES_LIST: 'SET_CLUSTER_OBJECTIVES_LIST',
    SET_CLUSTER_OBJECTIVES_COUNT: 'SET_CLUSTER_OBJECTIVES_COUNT',
    CLUSTER_OBJECTIVES_LOADING_START: 'CLUSTER_OBJECTIVES_LOADING_START',
    CLUSTER_OBJECTIVES_LOADING_STOP: 'CLUSTER_OBJECTIVES_LOADING_STOP',

    SET_CLUSTER_ACTIVITIES_LIST: 'SET_CLUSTER_ACTIVITIES_LIST',
    SET_CLUSTER_ACTIVITIES_COUNT: 'SET_CLUSTER_ACTIVITIES_COUNT',
    CLUSTER_ACTIVITIES_LOADING_START: 'CLUSTER_ACTIVITIES_LOADING_START',
    CLUSTER_ACTIVITIES_LOADING_STOP: 'CLUSTER_ACTIVITIES_LOADING_STOP',

    SET_CLUSTER_DISAGGREGATIONS_LIST: 'SET_CLUSTER_DISAGGREGATIONS_LIST',
    CLUSTER_DISAGGREGATIONS_LOADING_START: 'CLUSTER_DISAGGREGATIONS_LOADING_START',
    CLUSTER_DISAGGREGATIONS_LOADING_STOP: 'CLUSTER_DISAGGREGATIONS_LOADING_STOP',
    SET_CLUSTER_DISAGGREGATIONS_COUNT: 'SET_CLUSTER_DISAGGREGATIONS_COUNT',

    SET_PROGRAMME_DOCUMENTS: 'SET_PROGRAMME_DOCUMENTS',
    SET_PROGRAMME_DOCUMENT_DETAILS: 'SET_PROGRAMME_DOCUMENT_DETAILS',
    SET_PROGRAMME_DOCUMENTS_COUNT: 'SET_PROGRAMME_DOCUMENTS_COUNT',
    PROGRAMME_DOCUMENTS_LOADING_START: 'PROGRAMME_DOCUMENTS_LOADING_START',
    PROGRAMME_DOCUMENTS_LOADING_STOP: 'PROGRAMME_DOCUMENTS_LOADING_STOP',

    SET_CURRENT_PD: 'SET_CURRENT_PD',

    SET_PD_REPORT: 'SET_PD_REPORT',
    SET_PD_REPORTS: 'SET_PD_REPORTS',
    SET_PD_REPORTS_COUNT: 'SET_PD_REPORTS_COUNT',
    SET_CURRENT_PD_REPORT: 'SET_CURRENT_PD_REPORT',
    PD_REPORT_LOADING_START: 'PD_REPORT_LOADING_START',
    PD_REPORT_LOADING_STOP: 'PD_REPORT_LOADING_STOP',
    UPDATE_PD_REPORT: 'UPDATE_PD_REPORT',
    AMEND_REPORTABLE: 'AMEND_REPORTABLE',

    SET_PD_REPORT_ATTACHMENT: 'SET_PD_REPORT_ATTACHMENT',
    PD_REPORT_ATTACHMENT_LOADING_START: 'PD_REPORT_ATTACHMENT_LOADING_START',
    PD_REPORT_ATTACHMENT_LOADING_STOP: 'PD_REPORT_ATTACHMENT_LOADING_STOP',

    SET_PD_INDICATORS: 'SET_PD_INDICATORS',
    SET_PD_INDICATORS_LOADING: 'SET_PD_INDICATORS_LOADING',

    SET_RESPONSE_PLANS: 'SET_RESPONSE_PLANS',
    SET_CURRENT_RESPONSE_PLAN_ID: 'SET_CURRENT_RESPONSE_PLAN_ID',
    SET_CURRENT_RESPONSE_PLAN: 'SET_CURRENT_RESPONSE_PLAN',
    ADD_RESPONSE_PLAN: 'ADD_RESPONSE_PLAN',

    SET_PROGRESS_REPORTS: 'SET_PROGRESS_REPORTS',
    SET_PROGRESS_REPORTS_COUNT: 'SET_PROGRESS_REPORTS_COUNT',
    PROGRESS_REPORTS_LOADING_START: 'PROGRESS_REPORTS_LOADING_START',
    PROGRESS_REPORTS_LOADING_STOP: 'PROGRESS_REPORTS_LOADING_STOP',

    SET_DISAGGREGATIONS: 'SET_DISAGGREGATIONS',
    SET_DISAGGREGATIONS_FOR_LOCATION: 'SET_DISAGGREGATIONS_FOR_LOCATION',
    SET_PROGRESS_FOR_LOCATION: 'SET_PROGRESS_FOR_LOCATION',

    SET_CLUSTER_INDICATOR_REPORTS: 'SET_CLUSTER_INDICATOR_REPORTS',
    SET_CLUSTER_INDICATOR_REPORTS_COUNT: 'SET_CLUSTER_INDICATOR_REPORTS_COUNT',
    UPDATE_CLUSTER_INDICATOR_REPORT: 'UPDATE_CLUSTER_INDICATOR_REPORT',
    CLUSTER_INDICATOR_REPORTS_LOADING_START: 'CLUSTER_INDICATOR_REPORTS_LOADING_START',
    CLUSTER_INDICATOR_REPORTS_LOADING_STOP: 'CLUSTER_INDICATOR_REPORTS_LOADING_STOP',

    SET_PARTNERS_BY_CLUSTER_ACTIVITY_ID: 'SET_PARTNERS_BY_CLUSTER_ACTIVITY_ID',
    SET_PARTNERS_BY_CLUSTER_ACTIVITY_ID_COUNT:
      'SET_PARTNERS_BY_CLUSTER_ACTIVITY_ID_COUNT',
    PARTNERS_BY_CLUSTER_ACTIVITY_ID_LOADING_START:
      'PARTNERS_BY_CLUSTER_ACTIVITY_ID_LOADING_START',
    PARTNERS_BY_CLUSTER_ACTIVITY_ID_LOADING_STOP:
      'PARTNERS_BY_CLUSTER_ACTIVITY_ID_LOADING_STOP',

    SET_ACTIVITIES_BY_PARTNER_PROJECT_ID: 'SET_ACTIVITIES_BY_PARTNER_PROJECT_ID',
    SET_ACTIVITIES_BY_PARTNER_PROJECT_ID_COUNT:
      'SET_ACTIVITIES_BY_PARTNER_PROJECT_ID_COUNT',
    ACTIVITIES_BY_PARTNER_PROJECT_ID_LOADING_START:
      'ACTIVITIES_BY_PARTNER_PROJECT_ID_LOADING_START',
    ACTIVITIES_BY_PARTNER_PROJECT_ID_LOADING_STOP:
      'ACTIVITIES_BY_PARTNER_PROJECT_ID_LOADING_STOP',

    SET_INDICATORS_BY_CLUSTER_OBJECTIVE_ID: 'SET_INDICATORS_BY_CLUSTER_OBJECTIVE_ID',
    SET_INDICATORS_BY_CLUSTER_OBJECTIVE_ID_COUNT:
      'SET_INDICATORS_BY_CLUSTER_OBJECTIVE_ID_COUNT',
    INDICATORS_BY_CLUSTER_OBJECTIVE_ID_LOADING_START:
      'INDICATORS_BY_CLUSTER_OBJECTIVE_ID_LOADING_START',
    INDICATORS_BY_CLUSTER_OBJECTIVE_ID_LOADING_STOP:
      'INDICATORS_BY_CLUSTER_OBJECTIVE_ID_LOADING_STOP',

    SET_INDICATORS_BY_CLUSTER_ACTIVITY_ID: 'SET_INDICATORS_BY_CLUSTER_ACTIVITY_ID',
    SET_INDICATORS_BY_CLUSTER_ACTIVITY_ID_COUNT:
      'SET_INDICATORS_BY_CLUSTER_ACTIVITY_ID_COUNT',
    INDICATORS_BY_CLUSTER_ACTIVITY_ID_LOADING_START:
      'INDICATORS_BY_CLUSTER_ACTIVITY_ID_LOADING_START',
    INDICATORS_BY_CLUSTER_ACTIVITY_ID_LOADING_STOP:
      'INDICATORS_BY_CLUSTER_ACTIVITY_ID_LOADING_STOP',

    SET_INDICATORS_BY_PARTNER_PROJECT_ID: 'SET_INDICATORS_BY_PARTNER_PROJECT_ID',
    SET_INDICATORS_BY_PARTNER_PROJECT_ID_COUNT:
      'SET_INDICATORS_BY_PARTNER_PROJECT_ID_COUNT',
    INDICATORS_BY_PARTNER_PROJECT_ID_LOADING_START:
      'INDICATORS_BY_PARTNER_PROJECT_ID_LOADING_START',
    INDICATORS_BY_PARTNER_PROJECT_ID_LOADING_STOP:
      'INDICATORS_BY_PARTNER_PROJECT_ID_LOADING_STOP',

    SET_INDICATORS_BY_PARTNER_ACTIVITY_ID: 'SET_INDICATORS_BY_PARTNER_ACTIVITY_ID',
    SET_INDICATORS_BY_PARTNER_ACTIVITY_ID_COUNT:
      'SET_INDICATORS_BY_PARTNER_ACTIVITY_ID_COUNT',
    INDICATORS_BY_PARTNER_ACTIVITY_ID_LOADING_START:
      'INDICATORS_BY_PARTNER_ACTIVITY_ID_LOADING_START',
    INDICATORS_BY_PARTNER_ACTIVITY_ID_LOADING_STOP:
      'INDICATORS_BY_PARTNER_ACTIVITY_ID_LOADING_STOP',

    RESET: 'RESET',

    CONFIRM_MODAL: 'CONFIRM_MODAL',
    CONFIRM_INLINE: 'CONFIRM_INLINE',

    THEME_PRIMARY_COLOR_IP: '#0099ff',
    THEME_PRIMARY_COLOR_CLUSTER: '#009d55',

    SET_CLUSTER_DASHBOARD_DATA: 'SET_CLUSTER_DASHBOARD_DATA',
    CLUSTER_DASHBOARD_DATA_LOADING_START: 'CLUSTER_DASHBOARD_DATA_LOADING_START',
    CLUSTER_DASHBOARD_DATA_LOADING_STOP: 'CLUSTER_DASHBOARD_DATA_LOADING_STOP',

    FORMAT_NUMBER_DEFAULT: '0,0.[00]',

    SET_LANGUAGE: 'SET_LANGUAGE',
    SET_L11N_RESOURCES: 'SET_L11N_RESOURCES',

    SET_CONFIG: 'SET_CONFIG',
    CONFIG_LOADING_START: 'CONFIG_LOADING_START,',
    CONFIG_LOADING_END: 'CONFIG_LOADING_END',

    OPERATIONAL_PRESENCE_DATA_LOADING_START: 'OPERATIONAL_PRESENCE_DATA_LOADING_START',
    OPERATIONAL_PRESENCE_DATA_LOADING_STOP: 'OPERATIONAL_PRESENCE_DATA_LOADING_STOP',
    SET_OPERATIONAL_PRESENCE_DATA: 'SET_OPERATIONAL_PRESENCE_DATA',

    OPERATIONAL_PRESENCE_MAP_LOADING_START: 'OPERATIONAL_PRESENCE_MAP_LOADING_START',
    OPERATIONAL_PRESENCE_MAP_LOADING_STOP: 'OPERATIONAL_PRESENCE_MAP_LOADING_STOP',
    SET_OPERATIONAL_PRESENCE_MAP: 'SET_OPERATIONAL_PRESENCE_MAP',

    ANALYSIS_INDICATORS_DATA_LOADING_START: 'ANALYSIS_INDICATORS_DATA_LOADING_START',
    ANALYSIS_INDICATORS_DATA_LOADING_STOP: 'ANALYSIS_INDICATORS_DATA_LOADING_STOP',
    SET_ANALYSIS_INDICATORS_DATA: 'SET_ANALYSIS_INDICATORS_DATA',
    ANALYSIS_INDICATOR_DATA_LOADING_START: 'ANALYSIS_INDICATOR_DATA_LOADING_START',
    ANALYSIS_INDICATOR_DATA_LOADING_STOP: 'ANALYSIS_INDICATOR_DATA_LOADING_STOP',
    SET_ANALYSIS_INDICATOR_DATA: 'SET_ANALYSIS_INDICATOR_DATA',

    PRP_ROLE: PRP_ROLE,

    PARTNER_ROLES: [
      PRP_ROLE.CLUSTER_VIEWER,
      PRP_ROLE.CLUSTER_COORDINATOR,
      PRP_ROLE.CLUSTER_MEMBER
    ],

    WORKSPACE_ROLES: [
      PRP_ROLE.IP_ADMIN,
      PRP_ROLE.IP_AUTHORIZED_OFFICER,
      PRP_ROLE.IP_EDITOR,
      PRP_ROLE.IP_VIEWER
    ]
  },
  Settings: {
    layout: {
      threshold: '(min-width: 600px)',
    },

    dateFormat: 'DD-MMM-YYYY',

    ip: {
      readOnlyStatuses: [
        'Sub',
        'Acc',
        'Rej',
      ],
    },

    cluster: {
      maxLocType: 5,
    }
  }
}

export default App;
