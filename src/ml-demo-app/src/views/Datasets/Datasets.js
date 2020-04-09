import React from 'react';
import clsx from 'clsx';
import { makeStyles } from '@material-ui/styles';
import PropTypes from 'prop-types';
import { Grid } from '@material-ui/core';
import {DatasetTable} from './components/DatasetTable';
import {FeatureSelector} from './components/FeatureSelector';

const useStyles = makeStyles((theme) => ({
    root: {
        padding: theme.spacing(4)
    },
    content: {
        flexGrow: 1
    }
}));

const Datasets = (props) => {
    const classes = useStyles();
    const {featureType, setFeatureType} = React.useState('host');

    const handleUpdate = (value) => {
        setFeatureType(value)
    }

    return (
        <div className = {classes.root}>
            <Grid
                className = {classes.content}
                container
                spacing={8}
            >
                {/* <div className={classes.row}>
                    <FeatureSelector handleUpdate={handleUpdate}/>
                </div> */}
                <DatasetTable/>
            </Grid>
        </div>
    );
}

// Datasets.propTypes = {
//     featureType: PropTypes.string
// }

export default Datasets;