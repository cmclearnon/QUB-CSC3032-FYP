import React from 'react';
import {Switch, Redirect} from 'react-router-dom';
import { LayoutRoute } from './components/LayoutRoute';

import {Dashboard} from './views/Dashboard';
// import {default as DatasetTable} from './views/Datasets/DatasetTable';
import {default as Datasets} from './views/Datasets/Datasets'


import {MainLayout} from './layout/MainLayout';

const Routes = () => {
    return (
        <Switch>
            <Redirect
                exact
                from = "/"
                to = "/dashboard"
            />
            <LayoutRoute
                component = {Dashboard}
                exact
                layout = {MainLayout}
                path = "/dashboard"
            />
            <LayoutRoute
                component = {Datasets}
                exact
                layout = {MainLayout}
                path = "/datasets"
            />
            <Redirect to="/not-found" />
        </Switch>
    );
};

export default Routes;