import React from 'react';
import clsx from 'clsx';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/styles';
import {
    Card,
    CardContent,
    Grid,
    Typography,
    Avatar
} from '@material-ui/core';
import SpeedIcon from '@material-ui/icons/Speed';
import { colors } from '@material-ui/core';

const useStyles = makeStyles(theme => ({
    root: {
      height: 150,
      width: 250
    },
    content: {
      alignItems: 'center',
      display: 'flex'
    },
    title: {
      fontWeight: 700
    },
    avatar: {
      backgroundColor: theme.palette.error.main,
      height: 56,
      width: 56
    },
    icon: {
      height: 32,
      width: 32
    },
    difference: {
      marginTop: theme.spacing(2),
      display: 'flex',
      alignItems: 'center'
    },
    differenceIcon: {
      color: theme.palette.error.dark
    },
    differenceValue: {
      color: theme.palette.error.dark,
      marginRight: theme.spacing(1)
    }
  }));

const ModelAccuracy = props => {
    const {className, ...rest} = props;
    const classes = useStyles();

    // Component Card
    return (
        <Card
            {...rest}
            className = {clsx(classes.root, className)}
        >
            <CardContent>
                <Grid
                    container
                    justify = "space-between"
                >
                    <Grid item>
                        <Typography
                            className = {classes.title}
                            color = 'textSecondary'
                            variant = 'body2'
                        >
                            Model Accuracy
                        </Typography>
                        <Typography variant = 'h3'>
                            0.988
                        </Typography>
                    </Grid>
                    <Grid item>
                        <Avatar className = {classes.avatar}>
                            <SpeedIcon className = {classes.icon}/>
                        </Avatar>
                    </Grid>
                </Grid>
            </CardContent>
        </Card>
    )
}

ModelAccuracy.propTypes = {
    className: PropTypes.string
  };
  
export default ModelAccuracy;