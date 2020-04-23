import React, {useState} from 'react';
import clsx from 'clsx';
import { makeStyles } from '@material-ui/styles';
import {
  Card,
  CardContent,
  CardHeader,
  Divider,
  Typography
} from '@material-ui/core';
import PropTypes from 'prop-types';

const useStyles = makeStyles((theme) => ({
    root: {
        height: '100%',
        width: 700
    },
    urlField: {
        position: 'relative',
        height: '100px'
    },
    stats: {
        marginTop: theme.spacing(2),
        display: 'flex',
        justifyContent: 'center'
    },
    feature: {
        textAlign: 'center',
        padding: theme.spacing(1)
      },
}));
  
const Features = (props) => {
    const { className, ...rest } = props;
    const classes = useStyles();
    const {url, features} = props;

    return (
        <Card
        {...rest}
        className={clsx(classes.root, className)}
      >
        <CardHeader
          title="Features Extracted"
        />
        <Divider />
        <CardContent>
          <div className={classes.urlField}>
            <Typography variant="body1">URL Processed: {url}</Typography>
          </div>
          {Object.entries(features).map(([key, value]) => (
            console.log(features),
              <div
                className={classes.feature}
                key={key}
              >
                <Typography variant="body1">{key}</Typography>
                <Typography variant="h2">
                  {value}
                </Typography>
                <Divider />
              </div>
            ))
          }
        </CardContent>
      </Card>
    );
};

Features.propTypes = {
    className: PropTypes.string
};

export default Features;