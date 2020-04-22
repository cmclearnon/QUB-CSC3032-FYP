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
    // spacer: {
    //     flexGrow: 1
    // },
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
        props.handleFeatureChange(event.target.value);
    };    

    const handleClose = () => {
        setOpen(false);
    };

    const handleOpen = () => {
        setOpen(true);
    };

    return (
        <div {...rest} className={clsx(classes.root, className)}>
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
                    <MenuItem value="">
                        <em>None</em>
                    </MenuItem>
                    <MenuItem value={'domain'}>Domain</MenuItem>
                    <MenuItem value={'lexical'}>Lexical</MenuItem>
                </Select>
            </FormControl>
        </div>
  
    )
}

FeatureSelector.propTypes = {
    className: PropTypes.string,
  };

export default FeatureSelector;