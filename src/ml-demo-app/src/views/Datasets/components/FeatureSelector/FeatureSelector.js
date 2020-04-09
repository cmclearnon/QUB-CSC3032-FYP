import React from 'react';
import PropTypes from 'prop-types';
import clsx from 'clsx';
import { makeStyles } from '@material-ui/styles';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import Button from '@material-ui/core/Button';

const useStyles = makeStyles(theme => ({
    root: {},
    row: {
      height: '42px',
      display: 'flex',
      alignItems: 'center',
      marginTop: theme.spacing(1)
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
    },
    formControl: {
        margin: theme.spacing(1),
        minWidth: 120,
    },
  }));


const FeatureSelector = (props) => {
    const {className, ...rest} = props;
    const classes = useStyles();
    const featureType = React.useState('');
    const [open, setOpen] = React.useState(false);
    
    const updateFeature = (value) => {
        this.props.handleUpdate(value)
    };    

    const handleClose = () => {
        setOpen(false);
    };

    const handleOpen = () => {
        setOpen(true);
    };

    return (
        <div
            {...rest}
            className={clsx(classes.root, className)}
        >
            <div className={classes.row}>
                <Button className={classes.button} onClick={handleOpen}>
                    Choose Feature Type
                </Button>
                <FormControl className={classes.formControl}>
                    <InputLabel id="select-feature-id">Feature</InputLabel>
                    <Select
                        labelId="select-feature-label"
                        id="select-feature"
                        open={open}
                        onClose={handleClose}
                        onOpen={handleOpen}
                        value={featureType}
                        onChange={(event) => {updateFeature(event.target.value)}}
                    >
                        <MenuItem value="">
                            <em>None</em>
                        </MenuItem>
                        <MenuItem value={'host'}>Host</MenuItem>
                        <MenuItem value={'lexical'}>Lexical</MenuItem>
                    </Select>
                </FormControl>
            </div>
        </div>
  
    )
}

export default FeatureSelector;