import React from 'react';
import { Route } from 'react-router-dom';
import PropTypes from 'prop-types';

const LayoutRoute = (props) => {
    const {
        layout: Layout,
        component: Component,
        ...rest
    } = props;

    return (
        <Route
            {...rest}
            render = {matchProps => (
                <Layout>
                    <Component {...matchProps}/>
                </Layout>
            )}
        />
    );
};

LayoutRoute.propTypes = {
    layout: PropTypes.any.isRequired,
    component: PropTypes.any.isRequired,
    path: PropTypes.string
};

export default LayoutRoute;