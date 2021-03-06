import React from 'react';
import {shallow} from 'enzyme';
import toJSON from 'enzyme-to-json';
import PageContent from '../PageContent';

describe('PageContent component', () => {
    const children = <div></div>;
    const classes = {};

    it('renders properly', () => {
        const wrapper = shallow(<PageContent
            children={children}
            classes={classes}
        />);

        expect(wrapper.dive().length).toBe(1);
        expect(toJSON(wrapper)).toMatchSnapshot();
    });
});