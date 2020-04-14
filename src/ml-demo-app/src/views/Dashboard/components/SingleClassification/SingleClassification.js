import React from 'react';
import clsx from 'clsx';
import { makeStyles } from '@material-ui/styles';
import AssessmentIcon from '@material-ui/icons/Assessment';
import {
  Card,
  CardContent,
  Grid,
  Typography,
  Avatar,
  LinearProgress
} from '@material-ui/core';
import PropTypes from 'prop-types';

const useStyles = makeStyles(theme => ({
  root: {
    height: '100%'
  },
  content: {
    alignItems: 'center',
    display: 'flex'
  },
  title: {
    fontWeight: 700
  },
  avatar: {
    backgroundColor: theme.palette.primary.main,
    color: theme.palette.primary.contrastText,
    height: 56,
    width: 56
  },
  icon: {
    height: 32,
    width: 32
  },
  progress: {
    marginTop: theme.spacing(3)
  }
}));

const SingleClassification = (props) => {
  const { className, ...rest } = props;
  const {classification, probability} = props;
  const classes = useStyles();
  if (classification === 0) {
    var classif = 'Benign';
  } else {
      var classif = 'Malicious';
  }

  return (
    <Card
      {...rest}
      className={clsx(classes.root, className)}
    >
      <CardContent>
        <Grid
          container
          justify="space-between"
        >
          <Grid item>
            <Typography
              className={classes.title}
              color="textSecondary"
              gutterBottom
              variant="body2"
            >
              CLASSIFICATION CONFIDENCE
            </Typography>
            <Typography variant="h3">{classif}: {Math.round(probability[classification] * 1000) / 10}%</Typography>
          </Grid>
          <Grid item>
            <Avatar className={classes.avatar}>
              <AssessmentIcon className={classes.icon} />
            </Avatar>
          </Grid>
        </Grid>
        <LinearProgress
          className={classes.progress}
          value={Math.round(probability[classification] * 1000) / 10}
          variant="determinate"
        />
      </CardContent>
    </Card>
  );
};

SingleClassification.propTypes = {
  className: PropTypes.string
};

export default SingleClassification;