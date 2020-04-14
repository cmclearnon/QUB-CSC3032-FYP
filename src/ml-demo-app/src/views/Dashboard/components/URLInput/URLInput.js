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
        width: 250
    }
}));
  
const URLInput = (props) => {
    const { className, ...rest } = props;
    const {getPrediction} = props;
    const classes = useStyles();
    const [url, setUrl] = useState('');

    const handleChange = (event) => {
        setUrl(event.target.value);
    };

    const invokePrediction = () => {
        getPrediction(url);
    }

    return (
        <Card
        {...rest}
        className={clsx(classes.root, className)}
        >
            <form
                autoComplete="off"
                noValidate
            >
                <CardContent>
                    <Grid
                        container
                        spacing={3}
                    >
                        <Grid
                        item
                        md={6}
                        xs={12}
                        >
                            <TextField
                                fullWidth
                                label="URL"
                                margin="dense"
                                name="url"
                                onChange={handleChange}
                                required
                                value={url}
                                variant="outlined"
                            />
                        </Grid>
                    </Grid>
                </CardContent>
                <Divider />
                <CardActions>
                    <Button
                        color="primary"
                        variant="contained"
                        onClick={invokePrediction}
                    >
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