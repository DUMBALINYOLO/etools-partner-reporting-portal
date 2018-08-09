import React, {Component} from "react";
import PropTypes from 'prop-types';
import {PORTALS} from "../../actions";
import UserRowExpandedText from "./UserRowExpandedText";
import withProps from "../hoc/withProps";
import {portal} from "../../helpers/props";

class UserRoleControl extends Component {
    render() {
        const {role, actions, portal} = this.props;

        let text = "";

        switch (portal) {
            case PORTALS.IP:
                text += role.workspace ? `${role.workspace.title} / ` : '';
                break;
            default:
                text += role.cluster ? `${role.cluster.full_title} / ` : '';
                break;
        }

        text += role.role_display;

        return (
            <div>
                <UserRowExpandedText>{text}</UserRowExpandedText>
                {actions}
            </div>
        );
    }
}

UserRoleControl.propTypes = {
    role: PropTypes.object.isRequired
};

export default withProps(portal)(UserRoleControl);
