import React from 'react';
import { makeStyles } from '@material-ui/styles';
import { Grid } from '@material-ui/core';
import {
    ModelAccuracy
} from './components/ModelAccuracy';
import { PredictionsMetrics } from './components/PredictionMetrics';

const useStyles = makeStyles(theme => ({
    root: {
      padding: theme.spacing(4)
    },
    content: {
        flexGrow: 1,
      }
  }));

const Dashboard = () => {
    const classes = useStyles()

    return (
        <div className = {classes.root}>
            <Grid
                className = {classes.content}
                container
                spacing={8}
            >
                <Grid
                    item
                    lg = {3}
                    sm = {6}
                    xs = {12}
                    zl = {3}
                >
                    <ModelAccuracy/>
                </Grid>
                <Grid
                    item
                    lg = {3}
                    sm = {6}
                    xs = {12}
                    zl = {3}
                >
                    <ModelAccuracy/>
                </Grid>
                <Grid
                    item
                    lg = {3}
                    sm = {6}
                    xs = {12}
                    zl = {3}
                >
                    <ModelAccuracy/>
                </Grid>
            </Grid>
            <Grid
                className = {classes.content}
                container
                spacing={10}
            >
                <Grid
                    item
                    lg={4}
                    md={6}
                    xl={3}
                    xs={12}
                >
                    <PredictionsMetrics/>
                </Grid>
            </Grid>
        </div>
    );
};

export default Dashboard;