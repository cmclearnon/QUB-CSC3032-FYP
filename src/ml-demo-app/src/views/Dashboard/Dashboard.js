import React from 'react';
import { makeStyles } from '@material-ui/styles';
import { Grid } from '@material-ui/core';
import { ModelAccuracy } from './components/ModelAccuracy';
import { PredictionsMetrics } from './components/PredictionMetrics';
import { SingleClassification } from './components/SingleClassification';
import { Features } from './components/FeatureExtraction';
import { URLInput } from './components/URLInput';

// const useStyles = makeStyles(theme => ({
//     root: {
//       padding: theme.spacing(4)
//     },
//     content: {
//         flexGrow: 1,
//     }
// }));

class Dashboard extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
          url: "",
          model: "",
          prediction: -1,
          probabilityList: [0, 0],
          metrics: [],
          error: false,
          message: "",
          accuracy: null,
          tpr: null,
          fnr: null,
          auc_score: null,
          features: []
        }
        this.getPrediction = this.getPrediction.bind(this);
    }
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

    componentDidMount() {
        this.getMetrics()
    }

    getPrediction = (url, model) => {
      console.log('Model: ' + model)
        return fetch(`http://localhost:5000/single_prediction?model=${model}&url=${url}`)
          .then(apiResponse => apiResponse.json())
          .then(predictionResults =>
            this.setState({
              url: url,
              prediction: predictionResults.prediction,
              probabilityList: predictionResults.probability[0],
              features: predictionResults.original_features
            }),
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
                <Grid className = {this.classes.content} container spacing={8}>
                    <Grid item lg = {4} sm = {6} xs = {12} zl = {3}>
                        <URLInput getPrediction={this.getPrediction}/>
                    </Grid>
                    <Grid item lg = {3} sm = {6} xs = {12} zl = {3}>
                        <ModelAccuracy accuracy={this.state.accuracy} auc_score={this.state.auc_score}/>
                    </Grid>
                    <Grid item lg = {4} sm = {6} xs = {12} zl = {3}>
                        <SingleClassification probabilityList={this.state.probabilityList} classification={this.state.prediction}/>
                    </Grid>
                </Grid>
                <Grid className = {this.classes.content} container spacing={10}>
                    <Grid item lg={4} md={6} xl={3} xs={12}>
                        <PredictionsMetrics tpr={this.state.tpr} fnr={this.state.fnr}/>
                    </Grid>
                    <Grid item lg={5} md={6} xl={3} xs={12}>
                        <Features url={this.state.url} features={{...this.state.features[0]}}/>
                    </Grid>
                </Grid>
            </div>
        );
    };
};
export default Dashboard;