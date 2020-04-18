import React, { useEffect } from 'react';
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
    backgroundColor: theme.palette.secondary.main,
    color: theme.palette.primary.contrastText,
    height: 56,
    width: 56
  },
  icon: {
    height: 32,
    width: 32,
  },
  progress: {
    marginTop: theme.spacing(3),
    color: theme.palette.secondary.main
  }
}));

const SingleClassification = (props) => {
  const { className, ...rest } = props;
  const {classification, probabilityList} = props;
  const classes = useStyles();
  var classif;
  var predictionValue;

  if (classification === 0) {
    classif = 'Benign';
  } else if (classification === 1) {
    classif = 'Malicious';
  } else if (classification === -1){
    classif = 'No Prediciton'
  }

  if ((classification === 0) || (classification === 1)) {
    predictionValue = Math.round(probabilityList[classification] * 1000) / 10
  } else {
    console.log('Classification value: ' + classification)
    predictionValue = 0
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
            <Typography 
              variant="h3">{classif}: {predictionValue}%
            </Typography>
          </Grid>
          <Grid item>
            <Avatar className={classes.avatar}>
              <AssessmentIcon className={classes.icon}/>
            </Avatar>
          </Grid>
        </Grid>
        <LinearProgress
          className={classes.progress}
          value={predictionValue}
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