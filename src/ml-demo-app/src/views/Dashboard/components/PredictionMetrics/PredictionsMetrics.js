import React from 'react';
import clsx from 'clsx';
import PropTypes from 'prop-types';
import { makeStyles, useTheme } from '@material-ui/styles';
import {
    Card,
    CardHeader,
    CardContent,
    Divider,
    Typography
} from '@material-ui/core';
import { colors } from '@material-ui/core';
import { Doughnut } from 'react-chartjs-2';

const useStyles = makeStyles((theme) => ({
    root: {
        height: '100%',
        maxHeight: 500
    },
    chartContainer: {
        position: 'relative',
        height: '300px'
    },
    stats: {
        marginTop: theme.spacing(2),
        display: 'flex',
        justifyContent: 'center'
    },
    metric: {
        textAlign: 'center',
        padding: theme.spacing(1)
      },
}));

const PredictionsMetrics = (props) => {
    const {className, ...rest} = props;
    const {tpr, fnr} = props;
    const classes = useStyles();
    const theme = useTheme();

    const predictionData = {
        datasets: [
            {
              data: [Math.round(tpr * 1000) / 10, Math.round(fnr * 1000) / 10],
              backgroundColor: [
                theme.palette.secondary.main,
                theme.palette.error.main,
                theme.palette.warning.main
              ],
              borderWidth: 8,
              borderColor: theme.palette.white,
              hoverBorderColor: theme.palette.white
            }
          ],
          labels: ['True Positive', 'False Positive']
    };

    const options = {
        legend: {
          display: false
        },
        responsive: true,
        maintainAspectRatio: false,
        animation: false,
        cutoutPercentage: 80,
        layout: { padding: 0 },
        tooltips: {
          enabled: true,
          mode: 'index',
          intersect: false,
          borderWidth: 1,
          borderColor: theme.palette.divider,
          backgroundColor: theme.palette.white,
          titleFontColor: theme.palette.text.primary,
          bodyFontColor: theme.palette.text.secondary,
          footerFontColor: theme.palette.text.secondary
        }
    };

    const metrics = [
        {
            'name': 'True Positive',
            'value': Math.round(tpr * 1000) / 10,
            color: theme.palette.secondary.main
        },
        {
            'name': 'False Positive',
            'value': Math.round(fnr * 1000) / 10,
            color: theme.palette.secondary.main
        }
    ];

    return (
        <Card
          {...rest}
          className={clsx(classes.root, className)}
        >
          <CardHeader
            title="Prediction Metrics"
          />
          <Divider />
          <CardContent>
            <div className={classes.chartContainer}>
              <Doughnut
                data={predictionData}
                options={options}
              />
            </div>
            <div className={classes.stats}>
              {metrics.map(metric => (
                <div
                  className={classes.metric}
                  key={metric.name}
                >
                  <Typography variant="body1">{metric.name} Rate</Typography>
                  <Typography
                    style={{ color: metric.color }}
                    variant="h2"
                  >
                    {metric.value}%
                  </Typography>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      );
    
}

export default PredictionsMetrics;