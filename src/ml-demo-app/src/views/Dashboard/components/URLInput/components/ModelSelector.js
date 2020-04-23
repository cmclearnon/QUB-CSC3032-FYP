import React from 'react';
import PropTypes from 'prop-types';
import clsx from 'clsx';
import { makeStyles } from '@material-ui/styles';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';

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
    formControl: {
        margin: theme.spacing(1),
        minWidth: 120,
    },
  }));


const ModelSelector = (props) => {
    const {className, ...rest} = props;
    const classes = useStyles();
    const [modelType, setModelType]= React.useState('');
    const [open, setOpen] = React.useState(false);
    
    const handleChange = (event) => {
        setModelType(event.target.value);
        props.handleModelChange(event.target.value);
    };    

    const handleClose = () => {
        setOpen(false);
    };

    const handleOpen = () => {
        setOpen(true);
    };

    const getModelType = () => {
        return modelType;
    };

    return (
        <div {...rest} className={clsx(classes.root, className)}>
            <FormControl className={classes.formControl}>
                <InputLabel id="select-model-id">Model</InputLabel>
                <Select
                    labelId="select-model-label"
                    id="select-model"
                    open={open}
                    onClose={handleClose}
                    onOpen={handleOpen}
                    value={modelType}
                    onChange={handleChange}
                >
                    <MenuItem value="">
                        <em>None</em>
                    </MenuItem>
                    <MenuItem value={'SVC'}>SVC</MenuItem>
                    <MenuItem value={'KNN'}>KNN</MenuItem>
                </Select>
            </FormControl>
        </div>
  
    )
}

ModelSelector.propTypes = {
    className: PropTypes.string,
  };

export default ModelSelector;