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
    // difference: {
    //   marginTop: theme.spacing(2),
    //   display: 'flex',
    //   alignItems: 'center'
    // },
    // differenceIcon: {
    //   color: theme.palette.error.dark
    // },
    // differenceValue: {
    //   color: theme.palette.error.dark,
    //   marginRight: theme.spacing(1)
    // }
  }));

const ModelAccuracy = props => {
    const {className, ...rest} = props;
    const {accuracy, auc_score} = props;
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
                            gutterBottom
                            variant = 'body2'
                        >
                            MODEL ACCURACY
                        </Typography>
                        <Typography variant = 'h3'>
                          Score: {Math.round(accuracy * 1000) / 10}%
                        </Typography>
                        <Typography variant = 'h3'>
                          AUC: {Math.round(auc_score * 1000) / 10}%
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