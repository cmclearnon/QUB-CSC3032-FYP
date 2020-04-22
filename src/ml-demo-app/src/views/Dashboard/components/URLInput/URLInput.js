import React, {useState, useEffect} from 'react';
import clsx from 'clsx';
import { makeStyles } from '@material-ui/styles';
import {
  Card,
  CardContent,
  CardActions,
  Grid,
  Button,
  TextField,
  Divider
} from '@material-ui/core';
import PropTypes from 'prop-types';
import ModelSelector from './components/ModelSelector';
import {FeatureSelector} from '../../../FeatureSelector';

const useStyles = makeStyles((theme) => ({
    root: {
        height: 150,
        width: 1000
    },
    errorMessage: {
        backgroundcolor: theme.palette.error.main,
        color: theme.palette.error.contrastText,
    }
}));
  
const URLInput = (props) => {
    const { className, ...rest } = props;
    const {getprediction} = props;
    const classes = useStyles();
    const [url, setUrl] = useState('');
    const [emptyInput, setEmptyInput] = useState(false);
    const [model, setModel] = useState('');
    const [feature, setFeature] = useState('domain');

    useEffect(() => {
        console.log('URLInput: Model - ' + model);
        console.log('Feature Type - ' + feature);
    });

    const handleChange = (event) => {
        setUrl(event.target.value);
        setEmptyInput(false);
    };

    const invokePrediction = () => {
        if (url === "") {
            setEmptyInput(true);
            return;
        }
        props.getPrediction(url, model, feature);
    }

    const handleModelChange = (value) => {
        setModel(value);
    }; 

    const handleFeatureChange = (value) => {
        setFeature(value);
    }

    return (
        <Card
        {...rest}
        className={clsx(classes.root, className)}
        >
            <form autoComplete="off" noValidate>
                <CardContent>
                    <Grid
                        container
                        spacing={3}
                        justify="space-between"
                    >
                        <Grid item md={6} xs={12}>
                            <TextField
                                error={emptyInput}
                                helperText={emptyInput ? 'Empty Input!' : ' '}
                                fullWidth
                                label="URL"
                                margin="normal"
                                name="url"
                                onChange={handleChange}
                                style={{ margin: 8 }}
                                value={url}
                                variant="standard"
                            />
                        </Grid>
                        <Grid container md={6} xs={12}>
                            <Grid item md={6} xs={12}>
                                <ModelSelector handleModelChange={handleModelChange}/>
                            </Grid>
                            <Grid item md={6} xs={12}>
                                <FeatureSelector handleFeatureChange={handleFeatureChange}/>
                            </Grid>
                        </Grid>
                    </Grid>
                </CardContent>
                <Divider />
                <CardActions>
                    <Button color="secondary" variant="contained" onClick={invokePrediction}>
                        Predict
                    </Button>
                </CardActions>
            </form>
        </Card>
    );
};

URLInput.propTypes = {
    className: PropTypes.string
};

export default URLInput;