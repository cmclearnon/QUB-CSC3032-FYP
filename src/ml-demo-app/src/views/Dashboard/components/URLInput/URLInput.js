import React, {useState} from 'react';
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

const useStyles = makeStyles(() => ({
    root: {
        height: 150,
        width: 350
    }
}));
  
const URLInput = (props) => {
    const { className, ...rest } = props;
    const {getprediction} = props;
    const classes = useStyles();
    const [url, setUrl] = useState('');
    const [emptyInput, setEmptyInput] = useState(false);

    const handleChange = (event) => {
        setUrl(event.target.value);
        setEmptyInput(false);
    };

    const invokePrediction = () => {
        if (url === "") {
            setEmptyInput(true);
            return;
        }
        props.getPrediction(url);
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
                        container
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