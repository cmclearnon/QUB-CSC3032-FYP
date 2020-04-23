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
        padding: theme.spacing(1),
        flexGrow: 1
    },
    table: {
        padding: theme.spacing(5)
    }
}));

class Datasets extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
          featureType: "domain",
        }
        this.handleUpdate = this.handleUpdate.bind(this);
    }

    classes = makeStyles((theme) => ({
        root: {
            padding: theme.spacing(4)
        },
        content: {
            padding: theme.spacing(1),
            flexGrow: 1
        }
    }));

    handleUpdate = (value) => {
        console.log('CHanging featureType: ' + value);
        this.setState({
            featureType: value
        })
    }

    render() {
        return (
            <div className = {this.classes.root}>
                    <Grid className = {this.classes.content} container spacing={8}>
                        <Grid item lg = {4} sm = {6} xs = {12} zl = {3}>
                            <FeatureSelector handleUpdate={this.handleUpdate}/>
                        </Grid>
                    </Grid>
                    <Grid className = {this.classes.content} container spacing={8}>
                        <Grid item lg = {12} sm = {6} xs = {12} zl = {3}>
                            <DatasetTable featureType={this.state.featureType}/>
                        </Grid>
                    </Grid>
            </div>
        );
    }


}

// const Datasets = (props) => {
//     const classes = useStyles();
//     const {featureType, setFeatureType} = React.useState('domain');

//     const handleUpdate = (value) => {
//         setFeatureType(value)
//     }

//     return (
//         <div className = {classes.root}>
//             <div className = {classes.root}>
//                 <Grid
//                     className = {classes.content}
//                     container
//                     spacing={8}
//                 >
//                     <FeatureSelector handleupdate={handleUpdate}/>
//                 </Grid>
//             </div>
//             <div className = {classes.content}>
//                 <DatasetTable/>
//             </div>
//             {/* <Grid
//                 className = {classes.content}
//                 container
//                 spacing={8}
//             >
//                 <DatasetTable/>
//             </Grid> */}
//         </div>
//     );
// }

// Datasets.propTypes = {
//     featureType: PropTypes.string
// }

export default Datasets;