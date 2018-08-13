import {PRP_ROLE, PRP_ROLE_OPTIONS, USER_TYPE_OPTIONS} from "../constants";
import {api} from "../infrastructure/api";

export function hasAnyRole(user, roles) {
    const filtered = user.prp_roles.filter(item => roles.indexOf(item.role) > -1);

    return filtered.length > 0;
}

export function userRoleInWorkspace(user, workspace) {
    if (!workspace) return null;

    // eslint-disable-next-line
    const roles = user.prp_roles.filter(role => role.workspace == workspace);

    return roles.length ? roles[0].role : null;
}

export function getRoleLabel(role) {
    return getLabelFromOptions(PRP_ROLE_OPTIONS, role);
}

export function getUserTypeLabel(userType) {
    return getLabelFromOptions(USER_TYPE_OPTIONS, userType);
}

export function getLabelFromOptions(options, value) {
    // eslint-disable-next-line
    return options.filter(option => option.value == value)[0].label;
}

export function logout() {
    api.post("account/user-logout/").then(() => {
        window.location.href = "/";
    });
}

export function userRoleInCluster(user, cluster) {
    if (!cluster) return null;

    // eslint-disable-next-line
    const roles = user.prp_roles.filter(role => role.cluster == cluster || role.role === PRP_ROLE.CLUSTER_SYSTEM_ADMIN);

    return roles.length ? roles[0].role : null;
}

export function getUserRole(user, permission) {
    const userWorkspaceRole = permission.workspace && userRoleInWorkspace(user, permission.workspace.id);
    const userClusterRole = permission.cluster && userRoleInCluster(user, permission.cluster.id);
    return userClusterRole || userWorkspaceRole;
}

export function hasOnlyRoles(user, roles) {
    const filtered = user.prp_roles.filter(item => roles.indexOf(item.role) > -1);

    return filtered.length === user.prp_roles.length;
}

export function hasPartnersAccess(user) {
    return hasAnyRole(user, [PRP_ROLE.CLUSTER_IMO, PRP_ROLE.CLUSTER_SYSTEM_ADMIN])
}