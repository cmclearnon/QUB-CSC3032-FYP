import React from 'react';
import PropTypes from 'prop-types';
import clsx from 'clsx';
import { makeStyles } from '@material-ui/styles';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import Button from '@material-ui/core/Button';
import { Paper } from '@material-ui/core';

const useStyles = makeStyles(theme => ({
    root: {},
        row: {
        height: '42px',
        display: 'flex',
        alignItems: 'center',
        marginTop: theme.spacing(1)
    },
    dropdown: {
        borderRadius: '4px',
        alignItems: 'center',
        padding: theme.spacing(1),
        display: 'flex',
        flexBasis: 420
    },
    spacer: {
        flexGrow: 1
    },
    featureSelector: {
        marginRight: theme.spacing(1)
    },
    button: {
        display: 'block',
        marginTop: theme.spacing(2),
        color: 'secondary',
        marginRight: theme.spacing(2),
        marginLeft: theme.spacing(3)
    },
    formControl: {
        margin: theme.spacing(1),
        minWidth: 120,
    },
  }));


const FeatureSelector = (props) => {
    const {className, ...rest} = props;
    const classes = useStyles();
    const [ featureType, setFeatureType ]= React.useState('');
    const [open, setOpen] = React.useState(false);
    
    const updateFeature = (event) => {
        setFeatureType(event.target.value);
    };    

    const handleClose = () => {
        setOpen(false);
    };

    const handleOpen = () => {
        setOpen(true);
    };

    const triggerDatasetSearch = () => {
        props.handleUpdate(featureType);
    };

    const getFeatureType = () => {
        return featureType;
    };

    return (
        <div {...rest} className={clsx(classes.root, className)}>
            <Paper {...rest} className={clsx(classes.dropdown, className)}>
                <FormControl className={classes.formControl}>
                    <InputLabel id="select-feature-id">Feature</InputLabel>
                    <Select
                        labelId="select-feature-label"
                        id="select-feature"
                        open={open}
                        onClose={handleClose}
                        onOpen={handleOpen}
                        value={featureType}
                        onChange={updateFeature}
                    >
                        <MenuItem value={'domain'}>Domain</MenuItem>
                        <MenuItem value={'lexical'}>Lexical</MenuItem>
                    </Select>
                </FormControl>
                <Button className={classes.button} variant="contained" onClick={triggerDatasetSearch} color="secondary">
                    Search
                </Button>
            </Paper>
        </div>
  
    )
}

FeatureSelector.propTypes = {
    className: PropTypes.string,
  };

export default FeatureSelector;