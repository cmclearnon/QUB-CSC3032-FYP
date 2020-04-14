import React from 'react';
import { makeStyles } from '@material-ui/styles';
import { Grid } from '@material-ui/core';
import { ModelAccuracy } from './components/ModelAccuracy';
import { PredictionsMetrics } from './components/PredictionMetrics';
import { SingleClassification } from './components/SingleClassification';
import { URLInput } from './components/URLInput';

const useStyles = makeStyles(theme => ({
    root: {
      padding: theme.spacing(4)
    },
    content: {
        flexGrow: 1,
    }
}));

class Dashboard extends React.Component {
// const Dashboard = () => {
    // classes = useStyles()
    classes = makeStyles(theme => ({
        root: {
          padding: theme.spacing(4)
        },
        content: {
            flexGrow: 1,
        }
    }));
    
    state = {
        url: "",
        prediction: null,
        probability: [0, 0],
        metrics: [],
        error: null,
        accuracy: null,
        tpr: null,
        fnr: null,
        auc_score: null
    };

    componentWillMount() {
        this.getMetrics()
    }

    getPrediction = (url) => {
        return fetch(`http://localhost:5000/single_prediction?url=${url}`)
          .then(apiResponse => apiResponse.json())
          .then(predictionResults =>
            this.setState({
              url: url,
              prediction: predictionResults.prediction,
              probability: predictionResults.probability[0]
            })
          )
          .catch(error =>
            this.setState({
              error,
            })
          );
    }

    getMetrics = () => {
        return fetch(`http://localhost:5000/model_accuracy`)
          .then(apiResponse => apiResponse.json())
          .then(metricsResults =>
            this.setState({
              accuracy: metricsResults.accuracy,
              tpr: metricsResults.tpr,
              fnr: metricsResults.fnr,
              auc_score: metricsResults.auc_score
            })
          )
          .catch(error =>
            this.setState({
              error,
            })
          );
    }

    render() {
        return (
            <div className = {this.classes.root}>
                <Grid
                    className = {this.classes.content}
                    container
                    spacing={8}
                >
                    <Grid
                        item
                        lg = {3}
                        sm = {6}
                        xs = {12}
                        zl = {3}
                    >
                        <URLInput getPrediction={this.getPrediction}/>
                    </Grid>
                    <Grid
                        item
                        lg = {3}
                        sm = {6}
                        xs = {12}
                        zl = {3}
                    >
                        <ModelAccuracy accuracy={this.state.accuracy} auc_score={this.state.auc_score}/>
                    </Grid>
                    <Grid
                        item
                        lg = {4}
                        sm = {6}
                        xs = {12}
                        zl = {3}
                    >
                        <SingleClassification probability={this.state.probability} classification={this.state.prediction}/>
                    </Grid>
                </Grid>
                <Grid
                    className = {this.classes.content}
                    container
                    spacing={10}
                >
                    <Grid
                        item
                        lg={4}
                        md={6}
                        xl={3}
                        xs={12}
                    >
                        <PredictionsMetrics tpr={this.state.tpr} fnr={this.state.fnr}/>
                    </Grid>
                </Grid>
            </div>
        );
    };
};
export default Dashboard;